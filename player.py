import pygame
from constants import ZONES


class Player:
    def __init__(self, is_computer=False):
        self.hand = []
        self.score = 0
        self.gold = 0
        self.augments = [] #tracking the more wacky Balatroized part
        self.moves = [] #tracking the sets placed down
        self.selected_cards = [] # Cards currently selected for placing down
        self.is_computer = is_computer

    def add_card_to_hand(self, card):
        self.hand.append(card)
        self.arrange_hand()

    def arrange_hand(self):
        if self.is_computer:
            # Computer hand at top - face down
            start_pos = ZONES["computer_hand"]
            spacing = 40
            start_y = start_pos[1]
            
            for i, card in enumerate(self.hand):
                card.rect.x = start_pos[0] + (i * spacing)
                card.rect.y = start_y
                card.is_face_up = False
        else:
            # Sort player hand for better organization
            self.sort_hand()
            
            # Position sorted cards
            start_pos = ZONES["player_hand"]
            spacing = 80
            hand_width = len(self.hand) * spacing
            start_x = (1200 - hand_width) // 2
            
            for i, card in enumerate(self.hand):
                card.rect.x = start_x + (i * spacing)
                card.rect.y = start_pos[1]
                card.is_face_up = True

    def sort_hand(self):
        """Sort hand by suit first, then by value"""
        # Sort by suit, then by value within each suit
        self.hand.sort(key=lambda card: (card.suit, card.value))

    def select_card(self, card):
        if card in self.hand and card not in self.selected_cards:
            self.selected_cards.append(card)
            card.rect.y -= 20 #the visual feedback of selecting
            return True
        return False
    
    def deselect_card(self, card):
        if card in self.selected_cards:
            self.selected_cards.remove(card)
            card.rect.y += 20
            return True
        return False
    
    def toggle_card_selection(self, card):
        if card in self.selected_cards:
            self.deselect_card(card)
        else:
            self.select_card(card)

    def remove_cards_from_hand(self, cards_to_remove):
        for card in cards_to_remove:
            if card in self.hand:
                self.hand.remove(card)
            if card in self.selected_cards:
                self.selected_cards.remove(card)
        self.arrange_hand()

    def draw_hand(self, screen):
        for card in self.hand:
            card.draw(screen)

        for card in self.selected_cards:
            pygame.draw.rect(screen, (255, 255, 0), card.rect, 3)
        