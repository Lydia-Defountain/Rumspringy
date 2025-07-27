import random
import pygame
from constants import REG_RANKS, REG_SUITS, ALT_RANKS, ALT_SUITS, JOKER_RANKS, ZONES


#Added card class to have sprite for cards themselves being tracked within the deck
class Card:
    def __init__(self, rank, suit, type="REG", x=0, y=0):
        self.rank = rank
        self.suit = suit
        self.deck_type = type
        self.value = self.get_card_value(rank, type)
        self.is_wild = self.check_if_wild(suit)
        self.rect = pygame.Rect(x, y, 71, 96)

        #for loading the card image based on rank and suit
        self.image = self.load_card_image(rank, suit)
        self.is_face_up = True
        self.is_clickable = True

    def load_card_image(self, rank, suit):
        filename = f"{rank.lower()}_{suit.lower()}.png"
        try:
            image = pygame.image.load(f"Game_Assets/cards/{filename}")
            return pygame.transform.scale(image, (71, 96))
        except:
            # Fallback with colored backgrounds
            surface = pygame.Surface((71, 96))
            
            # Color-code by suit
            suit_colors = {
                'hearts': (255, 200, 200),    # Light red
                'diamonds': (255, 220, 150),  # Light orange
                'clubs': (200, 255, 200),     # Light green
                'spades': (200, 200, 255),    # Light blue
                'stars': (255, 255, 150),     # Light yellow
                'joker': (255, 150, 255)      # Light purple
            }
            
            color = suit_colors.get(suit.lower(), (255, 255, 255))
            surface.fill(color)
            
            font = pygame.font.Font(None, 20)
            
            # Just show rank clearly
            rank_text = rank.upper()
            if len(rank_text) > 4:  # For longer names like "SQUIRE"
                rank_text = rank_text[:4]
            
            text = font.render(rank_text, True, (0, 0, 0))
            text_rect = text.get_rect(center=(35, 30))
            surface.blit(text, text_rect)
            
            # Show suit name
            suit_text = font.render(suit.upper()[:4], True, (0, 0, 0))
            suit_rect = suit_text.get_rect(center=(35, 60))
            surface.blit(suit_text, suit_rect)
            
            # Add border
            pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 2)
            return surface
        
    
    def draw(self, screen):
        if self.is_face_up:
            screen.blit(self.image, self.rect)
        else:
            # Draw card back
            pygame.draw.rect(screen, (0, 0, 100), self.rect)

        
    def handle_click(self, pos):
        if self.is_clickable and self.rect.collidepoint(pos):
            return True
        return False
    
    def check_if_wild(self, suit):
        """Check if this card is a wild card"""
        return suit.lower() == "joker"
    
    def get_card_value(self, rank, type):
        """Convert rank to numerical value"""
        if type == "REG":
            rank_values = {
                'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                '8': 8, '9': 9, '10': 10, "jack": 11, "queen": 12, "king": 13
            }
        elif type == "ALT":
            rank_values = {
                'ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                '8': 8, '9': 9, '10': 10, "squire": 11, "knight": 12, "jack": 13, "queen": 14, "king": 15
            }
        return rank_values.get(rank.lower(), 0)



class RummyDeck:
    def __init__(self, type="REG"):
        self.__cards = []
        self.__discard = []
        self.type = type
        self.create_deck(self.type)
        

        deck_pos = ZONES["deck"]
        discard_pos = ZONES["discard"]

        self.deck_rect = pygame.Rect(deck_pos[0], deck_pos[1], 71, 96)
        self.discard_rect = pygame.Rect(discard_pos[0], discard_pos[1], 71, 96)
        
        self.deck_back_image = self.load_deck_back()


    def create_deck(self, type):
        if type == "REG":
            ranks = REG_RANKS
            suits = REG_SUITS
        elif type == "ALT":
            ranks = ALT_RANKS
            suits = ALT_SUITS
        
        #Create Regular cards
        for suit in suits:
            for rank in ranks:
                card = Card(rank, suit, type)
                self.__cards.append(card)

        #add jokers
        if type == "ALT":
            for joker_rank in JOKER_RANKS:
                joker = Card(joker_rank, "joker", type)
                self.__cards.append(joker)


    def add_card(self, rank, suit):
        """Add a card to current deck"""
        # Add to current deck
        new_card = Card(rank, suit, self.type)
        self.__cards.append(new_card)
        self.shuffle_deck()
        return new_card
        
    
    
    def shuffle_deck(self):
        random.shuffle(self.__cards)

    def load_deck_back(self):
        try:
            image = pygame.image.load("Game_Assets/cards/card_back.png")
            return pygame.transform.scale(image, (71, 96))
        except:
            # Fallback: blue rectangle
            surface = pygame.Surface((71, 96))
            surface.fill((0, 0, 150))
            font = pygame.font.Font(None, 24)
            text = font.render("DECK", True, (255, 255, 255))
            text_rect = text.get_rect(center=(35, 48))
            surface.blit(text, text_rect)
            return surface
        
    def draw_card(self):
        """Draw a card from the top of the deck"""
        if len(self.__cards) > 0:
            card = self.__cards.pop()  # Remove from top of deck
            return card
        return None  # Deck is empty
    
    def is_empty(self):
        """Check if deck is empty"""
        return len(self.__cards) == 0
    
    def cards_remaining(self):
        """Get number of cards left in deck"""
        return len(self.__cards)
        
    def draw_deck(self, screen):
        """Draw the deck on the screen"""
        if len(self.__cards) > 0:
            screen.blit(self.deck_back_image, self.deck_rect)
            font = pygame.font.Font(None, 20)
            count_text = font.render(str(len(self.__cards)), True, (255, 255, 255))
            screen.blit(count_text, (self.deck_rect.x + 5, self.deck_rect.y - 20))
        else:
            pygame.draw.rect(screen, (100, 100, 100), self.deck_rect, 2)
            font = pygame.font.Font(None, 16)
            text = font.render("EMPTY", True, (100, 100, 100))
            text_rect = text.get_rect(center=self.deck_rect.center)
            screen.blit(text, text_rect)
        
        # Draw the discard pile
        self.draw_discard_pile(screen)

    def handle_deck_click(self, pos):
        """Check if the deck was clicked and return True if it was"""
        if self.deck_rect.collidepoint(pos) and len(self.__cards) > 0:
            return True
        return False

    def discard_card(self, card):
        """Add a card to the discard pile"""
        self.__discard.append(card)
        # Position the card at discard pile location
        card.rect.x = self.discard_rect.x
        card.rect.y = self.discard_rect.y
        card.is_face_up = True  # Discard pile is face up

    def draw_from_discard(self):
        """Draw the top card from discard pile"""
        if len(self.__discard) > 0:
            card = self.__discard.pop()  # Remove top card
            return card
        return None

    def peek_discard_top(self):
        """Look at top discard card without removing it"""
        if len(self.__discard) > 0:
            return self.__discard[-1]
        return None
    
    def handle_discard_click(self, pos):
        """Check if discard pile was clicked"""
        if self.discard_rect.collidepoint(pos) and len(self.__discard) > 0:
            return True
        return False
    
    def draw_discard_pile(self, screen):
        """Draw the discard pile"""
        if len(self.__discard) > 0:
            # Draw the top card of discard pile
            top_card = self.__discard[-1]
            top_card.draw(screen)
            
            # Show discard pile count
            font = pygame.font.Font(None, 20)
            count_text = font.render(str(len(self.__discard)), True, (255, 255, 255))
            screen.blit(count_text, (self.discard_rect.x + 5, self.discard_rect.y - 20))
        else:
            # Empty discard pile
            pygame.draw.rect(screen, (50, 50, 50), self.discard_rect, 2)
            font = pygame.font.Font(None, 16)
            text = font.render("DISCARD", True, (100, 100, 100))
            text_rect = text.get_rect(center=self.discard_rect.center)
            screen.blit(text, text_rect)

    def create_game_copy(self):
        """Create a fresh copy of this deck for gameplay"""
        new_deck = RummyDeck(self.type)
        
        # Clear the new deck and copy cards
        new_deck._RummyDeck__cards = []
        for card in self.__cards:
            # Create fresh card objects 
            card_copy = Card(card.rank, card.suit, card.deck_type)
            new_deck._RummyDeck__cards.append(card_copy)
        
        # Reset discard pile
        new_deck._RummyDeck__discard = []
        
        return new_deck
        