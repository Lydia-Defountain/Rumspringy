import pygame
from constants import ZONES


# === MAIN GAME LOGIC ===

def place_player_cards(player, placed_sets, set_owners):
    """Place player's selected cards"""
    
    selected_count = len(player.selected_cards)
    
    if selected_count >= 3:
        return _place_new_set(player, placed_sets, set_owners)
    elif selected_count == 1:
        return _add_to_existing_set(player, placed_sets, set_owners)
    else:
        return False, "Select 3+ cards for new set or 1 card to add to existing set"


def _place_new_set(player, placed_sets, set_owners):
    """Helper: Place a new set of 3+ cards"""
    if is_valid_set(player.selected_cards):
        new_set = player.selected_cards.copy()
        set_value = sum(card.value for card in new_set)
        
        # Update game state
        placed_sets.append(new_set)
        set_owners.append("player")
        player.score += set_value
        
        # Record move
        player.moves.append({
            "type": "place_set",
            "cards": [(card.rank, card.suit) for card in new_set],
            "set_index": len(placed_sets) - 1
        })
        
        # Clean up
        player.remove_cards_from_hand(new_set)
        player.selected_cards.clear()  
        position_placed_sets(placed_sets)
        
        return True, f"Placed {len(new_set)} cards! (+{set_value} points)"
    else:
        return False, "Invalid set! Check your cards."

def _add_to_existing_set(player, placed_sets, set_owners):
    """Helper: Add single card to existing set"""
    card_to_add = player.selected_cards[0]
    
    for set_index, existing_set in enumerate(placed_sets):
        if can_add_card_to_existing_set(card_to_add, existing_set):
            # Update game state
            placed_sets[set_index].append(card_to_add)
            player.score += card_to_add.value
            
            # Record move
            player.moves.append({
                "type": "add_to_set",
                "card": (card_to_add.rank, card_to_add.suit),
                "set_index": set_index
            })
            
            # Clean up
            player.remove_cards_from_hand([card_to_add])
            position_placed_sets(placed_sets)
            
            return True, f"Added {card_to_add.rank} of {card_to_add.suit} to set {set_index + 1} (+{card_to_add.value} points)"
    
    return False, "Cannot add card to any existing set"

# === VALIDATION FUNCTIONS ===

def can_add_card_to_existing_set(new_card, existing_set):
    """Check if a card can be added to make a valid set"""
    test_set = existing_set + [new_card]
    return is_valid_set(test_set)

def is_valid_set(cards):
    """Validate any set (with or without wilds)"""
    if len(cards) < 3:
        return False
    
    deck_type = cards[0].deck_type
    wild_cards = [card for card in cards if card.is_wild]
    regular_cards = [card for card in cards if not card.is_wild]
    
    return (is_valid_group(regular_cards, len(wild_cards), deck_type) or 
            is_valid_run(regular_cards, len(wild_cards)))

def is_valid_group(regular_cards, wild_count, deck_type):
    """Check if cards can form a group (same rank, different suits)"""
    total_cards = len(regular_cards) + wild_count
    max_suits = 5 if deck_type == "ALT" else 4
    
    if total_cards > max_suits or not regular_cards:
        return total_cards <= max_suits and not regular_cards  # All wilds case
    
    # All regular cards must have same rank, different suits
    ranks = [card.rank for card in regular_cards]
    suits = [card.suit for card in regular_cards]
    
    return len(set(ranks)) == 1 and len(set(suits)) == len(suits)

def is_valid_run(regular_cards, wild_count):
    """Check if cards can form a run (consecutive ranks, same suit)"""
    if not regular_cards:
        return True  # All wilds
    
    # All regular cards must have same suit
    suits = [card.suit for card in regular_cards]
    if len(set(suits)) != 1:
        return False
    
    # Check if regular cards + wilds can form consecutive sequence
    values = sorted([card.value for card in regular_cards])
    min_val, max_val = values[0], values[-1]
    cards_needed_for_range = max_val - min_val + 1
    total_cards = len(regular_cards) + wild_count
    
    return total_cards >= cards_needed_for_range

# === DISPLAY FUNCTIONS ===

def position_placed_sets(placed_sets):
    """Position sets in compact grid layout"""
    table_pos = ZONES["table_sets"]
    sets_per_row = 4
    set_width = 200
    set_height = 130
    
    for set_index, card_set in enumerate(placed_sets):
        row = set_index // sets_per_row
        col = set_index % sets_per_row
        
        set_start_x = table_pos[0] + (col * set_width)
        set_start_y = table_pos[1] + (row * set_height)
        
        # Position cards with overlap
        for card_index, card in enumerate(card_set):
            card.rect.x = set_start_x + (card_index * 35)
            card.rect.y = set_start_y
            card.is_face_up = True

def draw_ui_info(screen, player, computer, placed_sets):
    """Draw game information panel"""
    ui_pos = ZONES["ui_info"]
    font = pygame.font.Font(None, 28)
    
    info_data = [
        (f"Your Score: {player.score}", (100, 255, 100)),
        (f"Computer Score: {computer.score}", (255, 100, 100)),
        ("", None),
        (f"Cards in hand: {len(player.hand)}", (200, 100, 255)),
        (f"Selected: {len(player.selected_cards)}", (200, 100, 255)),
        (f"Sets on table: {len(placed_sets)}", (200, 100, 255)),
        ("", None),
        ("ESC = Menu  |  H = Help", (255, 255, 150)),
    ]
    
    for i, (line, color) in enumerate(info_data):
        if line and color:
            text = font.render(line, True, color)
            screen.blit(text, (ui_pos[0], ui_pos[1] + i * 30))

def draw_gameboard_sets(screen, placed_sets, set_owners):
    """Draw all placed sets with descriptive labels"""
    # Draw cards
    for card_set in placed_sets:
        for card in card_set:
            card.draw(screen)
    
    # Draw labels
    _draw_set_labels(screen, placed_sets, set_owners)

def _draw_set_labels(screen, placed_sets, set_owners):
    """Helper: Draw descriptive labels under sets"""
    table_pos = ZONES["table_sets"]
    font = pygame.font.Font(None, 20)
    sets_per_row = 4
    set_width = 200
    set_height = 130
    
    for set_index, card_set in enumerate(placed_sets):
        if not card_set:  # Skip empty sets
            continue
            
        row = set_index // sets_per_row
        col = set_index % sets_per_row
        
        label_x = table_pos[0] + (col * set_width) + 10
        label_y = table_pos[1] + (row * set_height) + 100
        
        # Generate descriptive text and get owner
        set_description = describe_set(card_set)
        owner = set_owners[set_index] if set_index < len(set_owners) else "?"
        
        # Color code by owner
        text_color = (100, 255, 100) if owner == "player" else (255, 100, 100)
        
        # Draw the description
        desc_text = font.render(set_description, True, text_color)
        screen.blit(desc_text, (label_x, label_y))

# === SET DESCRIPTION FUNCTIONS ===

def describe_set(card_set):
    """Generate a readable description of the set"""
    if not card_set:
        return "Empty"
    
    regular_cards = [card for card in card_set if not card.is_wild]
    wild_cards = [card for card in card_set if card.is_wild]
    
    if not regular_cards:
        return f"{len(wild_cards)} Wilds"
    
    ranks = [card.rank for card in regular_cards]
    suits = [card.suit for card in regular_cards]
    
    if len(set(ranks)) == 1:
        # It's a group
        return _format_group_description(ranks[0], len(wild_cards))
    elif len(set(suits)) == 1:
        # It's a run
        return _format_run_description(regular_cards, suits[0], len(wild_cards))
    else:
        return f"Mixed ({len(card_set)})"

def _format_group_description(rank, wild_count):
    """Format description for a group (same rank)"""
    rank_name = format_rank_name(rank)
    wild_text = f" +{wild_count}W" if wild_count else ""
    return f"{rank_name}s{wild_text}"

def _format_run_description(regular_cards, suit, wild_count):
    """Format description for a run (consecutive ranks)"""
    values = sorted([card.value for card in regular_cards])
    deck_type = regular_cards[0].deck_type
    
    start_rank = format_rank_name(get_rank_from_value(values[0], deck_type))
    end_rank = format_rank_name(get_rank_from_value(values[-1], deck_type))
    suit_name = format_suit_name(suit)
    wild_text = f" +{wild_count}W" if wild_count else ""
    
    return f"{start_rank}-{end_rank} {suit_name}{wild_text}"

# === UTILITY FUNCTIONS ===

def format_rank_name(rank):
    """Convert rank to short display name"""
    rank_names = {
        'ace': 'A', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7',
        '8': '8', '9': '9', '10': '10', 'squire': 'Sq', 'knight': 'Kn',
        'jack': 'J', 'queen': 'Q', 'king': 'K',
        'joker_low': 'JL', 'joker_mid': 'JM', 'joker_high': 'JH'
    }
    return rank_names.get(rank.lower(), rank[:2])

def format_suit_name(suit):
    """Convert suit to short display name"""
    suit_names = {
        'hearts': 'H', 'diamonds': 'D', 'clubs': 'C', 'spades': 'S',
        'stars': 'St', 'joker': 'W'
    }
    return suit_names.get(suit.lower(), suit[:2])

def get_rank_from_value(value, deck_type):
    """Convert numerical value back to rank name based on deck type"""
    value_mappings = {
        "REG": {
            1: 'ace', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
            8: '8', 9: '9', 10: '10', 11: 'jack', 12: 'queen', 13: 'king'
        },
        "ALT": {
            1: 'ace', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
            8: '8', 9: '9', 10: '10', 11: 'squire', 12: 'knight', 
            13: 'jack', 14: 'queen', 15: 'king'
        }
    }
    
    return value_mappings.get(deck_type, {}).get(value, str(value))


def check_win_condition(player, computer, deck):
    """Check if game should end based on no moves available"""
    # Game ends when deck is empty and no one can make moves
    if deck.is_empty() and len(deck._RummyDeck__discard) == 0:
        return True
    
    # Or when a player runs out of cards (traditional rummy)
    if len(player.hand) == 0 or len(computer.hand) == 0:
        return True
    
    return False

def determine_winner(player, computer):
    """Determine winner based on scores in Player class"""
    if player.score > computer.score:
        return "player"
    elif computer.score > player.score:
        return "computer"
    else:
        return "tie"

def calculate_final_scores(player, computer):
    """Calculate final scores by applying hand penalties to current scores"""
    # Use current scores from gameplay
    player_current = player.score
    computer_current = computer.score
    
    # Calculate penalties for remaining cards
    player_penalty = sum(card.value for card in player.hand)
    computer_penalty = sum(card.value for card in computer.hand)
    
    # Apply penalties to get final scores
    player_final = player_current - player_penalty
    computer_final = computer_current - computer_penalty
    
    # Update the Player class scores with final values
    player.score = player_final
    computer.score = computer_final
    
    return player_final, computer_final









    