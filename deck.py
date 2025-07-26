import random
import pygame
from constants import REG_RANKS, REG_SUITS, ALT_RANKS, ALT_SUITS


#Added card class to have sprite for cards themselves being tracked within the deck
class Card:
    def __init__(self, rank, suit, x=0, y=0):
        self.rank = rank
        self.suit = suit
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
            # Fallback: create a simple colored rectangle with text
            surface = pygame.Surface((71, 96))
            surface.fill((255, 255, 255))
            font = pygame.font.Font(None, 24)
            rank_ab = f"{rank[0]}{rank[1]}"
            suit_ab = f"{suit[0]}{suit[1]}"
            text = font.render(f"{rank_ab}{suit_ab}", True, (0, 0, 0))
            surface.blit(text, (10, 10))
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




class RummyDeck:
    def __init__(self, type="REG"):
        self.__cards = []
        self.__discard = []
        self.type = type
        self.create_deck(self.type)

    def create_deck(self, type):
        if type == "REG":
            ranks = REG_RANKS
            suits = REG_SUITS
        elif type == "ALT":
            ranks = ALT_RANKS
            suits = ALT_SUITS
        
        for suit in suits:
            for rank in ranks:
                card = Card(rank, suit)
                self.__cards.append(card)


    def shuffle_deck(self):
        random.shuffle(self.__cards)




        
        