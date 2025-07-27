import random
from gameboard import is_valid_set, position_placed_sets

def computer_turn(computer, deck, placed_sets, set_owners):
    """Execute optimal computer turn"""
    messages = []

    # Step 1: Choose whether to draw from deck or discard
    drawn_card = choose_draw_source(computer, deck)
    if drawn_card:
        computer.add_card_to_hand(drawn_card)
        messages.append("Computer drew a card")

    # Step 2: Try to place optimal sets
    placed_something = try_place_sets(computer, placed_sets, set_owners)
    if placed_something:
        set_type = "group" if len(set([c.rank for c in placed_something if not c.is_wild])) == 1 else "run"
        messages.append(f"Computer placed a {set_type} ({len(placed_something)} cards)")
    elif try_add_to_existing_sets(computer, placed_sets, set_owners):
        messages.append("Computer added card to existing set")    

    
    # Step 4: Discard optimally
    discard_card = choose_optimal_discard(computer)
    if discard_card:
        computer.hand.remove(discard_card)
        deck.discard_card(discard_card)  # Add to discard pile
        messages.append(f"Computer discarded {discard_card.rank} of {discard_card.suit}")
    
    return " • ".join(messages) if messages else "Computer completed turn"

def choose_draw_source(computer, deck):
    """Decide whether to draw from deck or discard pile"""
    # Check what's on top of discard pile
    top_discard = deck.peek_discard_top()
    
    if top_discard is None:
        # No discard pile, must draw from deck
        return deck.draw_card()
    
    # Calculate if the discard card would be useful
    discard_value = calculate_card_value(top_discard, computer.hand)
    
    # If discard card is very valuable, take it
    if discard_value > 30:  # Threshold for taking discard
        return deck.draw_from_discard()
    else:
        # Otherwise draw from deck
        return deck.draw_card()

def try_place_sets(computer, placed_sets, set_owners):
    """Try to place the best possible sets"""
    best_sets = find_all_possible_sets(computer.hand)
    
    if best_sets:
        # Choose the largest set first (gets rid of most cards)
        best_set = max(best_sets, key=len)

        # Calculate score for this set
        set_value = sum(card.value for card in best_set)
        computer.score += set_value  # Update computer's score
        
        # Remove cards from hand
        for card in best_set:
            computer.hand.remove(card)
            card.is_face_up = True
        
        # Add to placed sets
        placed_sets.append(best_set)
        set_owners.append("computer")
        
        # Record the move
        computer.moves.append({
            "type": "place_set",
            "cards": [(card.rank, card.suit) for card in best_set],
            "set_index": len(placed_sets) - 1
        })
        
        # Position the cards
        position_placed_sets(placed_sets)
        computer.arrange_hand()
        
        return best_set
    
    return None

def find_all_possible_sets(hand):
    """Find all valid sets that can be made from hand"""
    possible_sets = []
    
    # Check all combinations of 3+ cards
    from itertools import combinations
    
    for size in range(3, len(hand) + 1):
        for combo in combinations(hand, size):
            if is_valid_set(list(combo)):
                possible_sets.append(list(combo))
    
    return possible_sets

def try_add_to_existing_sets(computer, placed_sets, set_owners):
    """Try to add cards to existing sets on the table"""
    for card in computer.hand[:]:  # Copy list to avoid modification issues
        for set_index, existing_set in enumerate(placed_sets):
            # Test if card can be added
            test_set = existing_set + [card]
            if is_valid_set(test_set):
                # Add the card
                placed_sets[set_index].append(card)
                computer.hand.remove(card)
                card.is_face_up = True
                
                # Record the move
                computer.moves.append({
                    "type": "add_to_set",
                    "card": (card.rank, card.suit),
                    "set_index": set_index
                })
                
                position_placed_sets(placed_sets)
                computer.arrange_hand()
                return True
    
    return False

def choose_optimal_discard(computer):
    """Choose the best card to discard - avoid helping the player"""
    if not computer.hand:
        return None
    
    card_scores = []
    
    for card in computer.hand:
        # Calculate value for keeping the card
        keep_value = calculate_card_value(card, computer.hand)
        
        # Penalty for high-value cards (don't want to give player good cards)
        discard_penalty = card.value * 2
        
        # Wild cards should rarely be discarded
        if card.is_wild:
            keep_value += 100
        
        total_score = keep_value - discard_penalty
        card_scores.append((card, total_score))
    
    # Discard the card with the lowest total score
    card_scores.sort(key=lambda x: x[1])
    return card_scores[0][0]

def calculate_card_value(card, hand):
    """Calculate how valuable a card is for forming sets"""
    value = 0
    other_cards = [c for c in hand if c != card]
    
    # Check potential for groups (same rank)
    same_rank_count = len([c for c in other_cards if c.rank == card.rank])
    value += same_rank_count * 10  # Groups are valuable
    
    # Check potential for runs (consecutive ranks, same suit)
    same_suit_cards = [c for c in other_cards if c.suit == card.suit]
    for other_card in same_suit_cards:
        rank_diff = abs(card.value - other_card.value)
        if rank_diff <= 2:  # Close in rank = potential run
            value += (3 - rank_diff) * 5
    
    # Wild cards are always valuable
    if card.is_wild:
        value += 50
    
    return value

def get_computer_hand_for_display(computer):
    """Return computer hand info for UI display"""
    return {
        "hand_size": len(computer.hand),
        "sets_placed": len([move for move in computer.moves if move["type"] == "place_set"]),
        "cards_added": len([move for move in computer.moves if move["type"] == "add_to_set"])
    }

def calculate_discard_usefulness(card, hand):
    """Calculate how useful the top discard card would be"""
    # Test adding the card to hand temporarily
    test_hand = hand + [card]
    
    # Check if it helps form any sets
    possible_sets = find_all_possible_sets(test_hand)
    current_sets = find_all_possible_sets(hand)
    
    # If adding this card creates new set possibilities, it's valuable
    if len(possible_sets) > len(current_sets):
        return 50  # Very valuable
    
    # Check if it helps with existing partial sets
    value = calculate_card_value(card, hand)
    return value