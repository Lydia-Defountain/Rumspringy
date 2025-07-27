import pygame
from deck import RummyDeck
from player import Player

class GameMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_active = False
        self.menu_type = "pause"  # "pause" or "endgame"
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        
        # End game data
        self.winner = None
        self.player_score = 0
        self.computer_score = 0
        
        self.menu_background = self.create_menu_background()
        self.selected_option = 0


    def create_new_game(self, deck_type):
        """Create and return new game state"""
        deck = RummyDeck(deck_type)
        deck.shuffle_deck()
        
        player = Player(is_computer=False)
        computer = Player(is_computer=True)
        
        # Deal initial hands
        players_to_deal = [player, computer]
        for _ in range(7):
            for current_player in players_to_deal:
                card = deck.draw_card()
                if card:
                    current_player.add_card_to_hand(card)
        
        placed_sets = []
        set_owners = []
        
        return deck, player, computer, placed_sets, set_owners
    
    def handle_menu_action(self, action):
        """Handle menu actions and return appropriate response"""
        if action == "resume":
            self.is_active = False
            return {"type": "resume"}
        
        elif action == "new_game_reg":
            game_state = self.create_new_game("REG")
            self.is_active = False
            return {
                "type": "new_game",
                "deck_type": "REG",
                "game_state": game_state
            }
        
        elif action == "new_game_alt":
            game_state = self.create_new_game("ALT")
            self.is_active = False
            return {
                "type": "new_game", 
                "deck_type": "ALT",
                "game_state": game_state
            }
        
        elif action == "quit":
            return {"type": "quit"}
        
        return None
    
    def create_menu_background(self):
        """Create semi-transparent background for menu"""
        surface = pygame.Surface((self.screen_width, self.screen_height))
        surface.set_alpha(180)
        surface.fill((0, 0, 0))
        return surface
    
    def show_pause_menu(self):
        """Show pause menu"""
        self.menu_type = "pause"
        self.is_active = True
        self.selected_option = 0
        self.menu_options = [
            "Resume Game",
            "New Game - Regular Deck",
            "New Game - Alt Deck", 
            "Quit Game"
        ]
    
    def show_end_game_menu(self, winner, player_score, computer_score):
        """Show end game menu with results"""
        self.menu_type = "endgame"
        self.is_active = True
        self.winner = winner
        self.player_score = player_score
        self.computer_score = computer_score
        self.selected_option = 0
        self.menu_options = [
            "New Game - Regular Deck",
            "New Game - Alt Deck", 
            "Quit Game"
        ]
    
    def handle_input(self, event):
        """Handle menu navigation input"""
        if not self.is_active:
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.menu_type == "pause":
                self.is_active = False
                return "resume"
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.get_selected_action()
        return None
    
    def get_selected_action(self):
        """Return action based on selected menu option"""
        if self.menu_type == "pause":
            actions = {
                0: "resume",
                1: "new_game_reg",
                2: "new_game_alt",
                3: "quit"
            }
        else:  # endgame
            actions = {
                0: "new_game_reg",
                1: "new_game_alt",
                2: "quit"
            }
        return actions.get(self.selected_option)
    
    def draw(self, screen):
        """Draw the menu"""
        if not self.is_active:
            return
        
        # Draw semi-transparent background
        screen.blit(self.menu_background, (0, 0))
        
        if self.menu_type == "pause":
            self.draw_pause_menu(screen)
        else:
            self.draw_end_game_menu(screen)
    
    def draw_pause_menu(self, screen):
        """Draw pause menu"""
        # Title
        title_text = self.font_large.render("GAME PAUSED", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(title_text, title_rect)
        
        self.draw_menu_options(screen, 300)
    
    def draw_end_game_menu(self, screen):
        """Draw end game menu with results"""
        # Win message
        if self.winner == "player":
            title_text = self.font_large.render("YOU WIN!", True, (0, 255, 0))
        elif self.winner == "computer":
            title_text = self.font_large.render("COMPUTER WINS!", True, (255, 0, 0))
        else:
            title_text = self.font_large.render("TIE GAME!", True, (255, 255, 0))
        
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Scores
        player_score_text = self.font_medium.render(f"Your Score: {self.player_score}", True, (100, 255, 100))
        player_rect = player_score_text.get_rect(center=(self.screen_width // 2, 220))
        screen.blit(player_score_text, player_rect)
        
        computer_score_text = self.font_medium.render(f"Computer Score: {self.computer_score}", True, (255, 100, 100))
        computer_rect = computer_score_text.get_rect(center=(self.screen_width // 2, 260))
        screen.blit(computer_score_text, computer_rect)
        
        self.draw_menu_options(screen, 350)
    
    def draw_menu_options(self, screen, start_y):
        """Draw menu options"""
        option_spacing = 60
        
        for i, option in enumerate(self.menu_options):
            # Highlight selected option
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            
            option_text = self.font_medium.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.screen_width // 2, start_y + i * option_spacing))
            screen.blit(option_text, option_rect)
            
            # Draw selection indicator
            if i == self.selected_option:
                indicator = self.font_medium.render(">", True, (255, 255, 0))
                indicator_rect = indicator.get_rect(center=(option_rect.left - 30, option_rect.centery))
                screen.blit(indicator, indicator_rect)
        
        # Draw controls hint
        if self.menu_type == "pause":
            controls_text = "Use UP/DOWN arrows, ENTER to select, ESC to resume"
        else:
            controls_text = "Use UP/DOWN arrows, ENTER to select"
        
        controls_surface = self.font_medium.render(controls_text, True, (200, 200, 200))
        controls_rect = controls_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        screen.blit(controls_surface, controls_rect)