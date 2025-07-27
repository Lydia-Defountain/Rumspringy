import pygame
from deck import RummyDeck
from player import Player

class GameMenu:
    def __init__(self, screen_width, screen_height, toast_manager=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_active = False
        self.menu_type = "main"
        self.game_initialized = False 
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.store_items = self._initialize_store_items()

        # End game data
        self.winner = None
        self.player_data = None
        self.computer_data = None
        self.master_deck = None
        
        self.menu_background = self.create_menu_background()
        self.selected_option = 0
        self.toast_manager = toast_manager

    def show_main_menu(self):
        """Show main menu (initial screen)"""
        self.menu_type = "main"
        self.is_active = True
        self.selected_option = 0
        self.menu_options = [
            "New Game - Regular Deck",
            "New Game - Alt Deck",
            "How to Play",
            "Quit Game"
        ]


    def create_new_game(self, deck_type):
        """Create and return new game state"""
        self.master_deck = RummyDeck(deck_type)
        deck = self.master_deck.create_game_copy()

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

        if self.toast_manager:
            self.toast_manager.clear_all()
        
        return deck, player, computer, placed_sets, set_owners
    
    def handle_menu_action(self, action):
        """Handle menu actions and return appropriate response"""
        if action == "resume":
            self.is_active = False
            return {"type": "resume"}
        
        elif action == "how_to_play":
            self.show_how_to_play()
            return {"type": "show_screen"}
        
        elif action == "back_to_main":
            self.show_main_menu()
            return {"type": "show_screen"}
        
        elif action == "back_to_pause":
            self.show_pause_menu()
            return {"type": "show_screen"}
        
        elif action == "store":
            if self.player_data:
                self.show_store_menu(self.player_data)
                return {"type": "show_screen"}
            else:
                return {"type": "error", "message": "No player data available"}
        
        elif action == "back_to_pause":
            self.show_pause_menu()
            return {"type": "show_screen"}
        
        elif action and action.startswith("buy_"):
            # Handle store purchases
            item_index = int(action.split("_")[1])
            return self._handle_purchase(item_index)
        
        elif action == "new_game_reg":
            game_state = self.create_new_game("REG")
            self.is_active = False
            self.game_initialized = True
            return {
                "type": "new_game",
                "deck_type": "REG",
                "game_state": game_state
            }
        
        elif action == "new_game_alt":
            game_state = self.create_new_game("ALT")
            self.is_active = False
            self.game_initialized = True
            return {
                "type": "new_game", 
                "deck_type": "ALT",
                "game_state": game_state
            }
        
        elif action == "continue_game":
            game_state = self.create_new_game_continue()  
            self.is_active = False
            self.game_initialized = True
            return {
                "type": "continue_game",
                "deck_type": "REG",  
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
    
    def show_pause_menu(self, player):
        """Show pause menu"""
        self.menu_type = "pause"
        self.is_active = True
        self.selected_option = 0
        self.player_data = player
        self.menu_options = [
            "Resume Game",
            "Store",              
            "How to Play",
            "New Game - Regular Deck",
            "New Game - Alt Deck", 
            "Quit Game"
        ]

    def show_how_to_play(self):
        """Show how to play screen"""
        self.menu_type = "howtoplay"
        self.is_active = True
        self.selected_option = 0
        self.menu_options = [
            "Back to Menu"
        ]
    
    def show_end_game_menu(self, winner, player, computer):
        """Show end game menu with results"""
        self.menu_type = "endgame"
        self.is_active = True
        self.winner = winner
        self.player_data = player
        self.computer_data = computer
        
        self.selected_option = 0
        
        # Only show continue option if player won
        if winner == "player":
            self.menu_options = [
                "Continue Next Game",      
                "New Game - Regular Deck",
                "New Game - Alt Deck", 
                "Quit Game"
            ]
        else:
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
        if self.menu_type == "main":
            actions = {
                0: "new_game_reg",
                1: "new_game_alt",
                2: "how_to_play",
                3: "quit"
            }

        elif self.menu_type == "pause":
            actions = {
                0: "resume",
                1: "store",           
                2: "how_to_play",
                3: "new_game_reg",
                4: "new_game_alt",
                5: "quit"
            }

        elif self.menu_type == "store":
            actions = {}
            for i, item in enumerate(self.store_items):
                actions[i] = f"buy_{i}"  # buy_0, buy_1, etc.
            actions[len(self.store_items)] = "back_to_pause"
            return actions.get(self.selected_option)

        elif self.menu_type == "howtoplay":
            back_action = "back_to_pause" if self.game_initialized else "back_to_main"
            actions = {0: back_action}

        else:  # endgame
            if self.winner == "player":
                # Player won - continue option available
                actions = {
                    0: "continue_game",
                    1: "new_game_reg",
                    2: "new_game_alt",
                    3: "quit"
                }
            else:
                # Player lost/tied - no continue option
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
        
        if self.menu_type == "main":
            self.draw_main_menu(screen)
        elif self.menu_type == "pause":
            self.draw_pause_menu(screen)
        elif self.menu_type == "endgame":
            self.draw_end_game_menu(screen)
        elif self.menu_type == "howtoplay":
            self.draw_how_to_play(screen)

    def draw_main_menu(self, screen):
        """Draw main menu"""
        # Title
        title_text = self.font_large.render("RUMSPRINGY", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("A Rummy Card Game", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 200))
        screen.blit(subtitle_text, subtitle_rect)
        
        self.draw_menu_options(screen, 300)
    
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
        player_score_text = self.font_medium.render(f"Your Score: {self.player_data.score}", True, (100, 255, 100))
        player_rect = player_score_text.get_rect(center=(self.screen_width // 2, 220))
        screen.blit(player_score_text, player_rect)
        
        computer_score_text = self.font_medium.render(f"Computer Score: {self.computer_data.score}", True, (255, 100, 100))
        computer_rect = computer_score_text.get_rect(center=(self.screen_width // 2, 260))
        screen.blit(computer_score_text, computer_rect)

        if hasattr(self.player_data, 'gold'):
            gold_text = self.font_medium.render(f"Gold: {self.player_data.gold}", True, (255, 215, 0))
            gold_rect = gold_text.get_rect(center=(self.screen_width // 2, 300))
            screen.blit(gold_text, gold_rect)
        
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

    def draw_how_to_play(self, screen):
        """Draw how to play screen"""
        title_text = self.font_large.render("HOW TO PLAY", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 80))
        screen.blit(title_text, title_rect)
        
        # How to play content
        font_small = pygame.font.Font(None, 24)
        instructions = [
            "OBJECTIVE: Score more points than the computer",
            "",
            "TURN SEQUENCE:",
            "1. Draw a card (from deck or discard pile)",
            "2. Place sets (optional) - 3+ cards in groups or runs",
            "3. Discard a card to end your turn",
            "",
            "VALID SETS:",
            "• Groups: Same rank, different suits (3 Kings)",
            "• Runs: Consecutive ranks, same suit (5-6-7 Hearts)",
            "• Wild cards can substitute for any card",
            "",
            "CONTROLS:",
            "• Click cards to select/deselect",
            "• SPACE to place selected cards",
            "• D to discard selected card",
            "• ESC to pause",
            "",
            "SCORING:",
            "• Gain points for cards in placed sets",
            "• Lose points for cards left in hand at game end"
        ]
        
        start_y = 140
        for i, instruction in enumerate(instructions):
            if instruction:  # Skip empty lines
                color = (255, 255, 0) if instruction.isupper() and ":" in instruction else (255, 255, 255)
                text = font_small.render(instruction, True, color)
                screen.blit(text, (100, start_y + i * 25))
        
        # Back button
        self.draw_menu_options(screen, self.screen_height - 100)

    def create_new_game_continue(self):
        """Create new game preserving player progress"""
        deck = self.master_deck.create_game_copy()
        deck.shuffle_deck()
        
        # Create new players but preserve data from previous game
        player = Player(is_computer=False)
        computer = Player(is_computer=True)

        if self.player_data:
            player.score = self.player_data.score
            player.augments = self.player_data.augments.copy()
            player.gold = self.player_data.gold

        if self.computer_data:
            computer.score = self.computer_data.score
            computer.augments = self.computer_data.augments.copy()
            computer.gold = self.computer_data.gold

        # Deal initial hands
        players_to_deal = [player, computer]
        for _ in range(7):
            for current_player in players_to_deal:
                card = deck.draw_card()
                if card:
                    current_player.add_card_to_hand(card)
        
        placed_sets = []
        set_owners = []
        
        if self.toast_manager:
            self.toast_manager.clear_all()
        
        return deck, player, computer, placed_sets, set_owners
    

    def _initialize_store_items(self):
            """Initialize available store items"""
            return [
                {"name": "Extra Joker", "cost": 50, "description": "Add a joker to your deck", "type": "deck_card"},
                {"name": "Lucky Draw", "cost": 30, "description": "Draw 2 cards instead of 1", "type": "augment"},
                {"name": "Score Boost", "cost": 40, "description": "2x points for next set", "type": "augment"},
                
            ]

    def show_store_menu(self, player):
        """Show store menu with available items"""
        self.menu_type = "store"
        self.is_active = True
        self.selected_option = 0
        self.current_player = player  # Store reference for purchases
        
        # Build menu options from store items + back option
        self.menu_options = [item["name"] + f" ({item['cost']} gold)" for item in self.store_items]
        self.menu_options.append("Back to Menu")

    
    def _handle_purchase(self, item_index, current_deck=None):
        """Handle purchasing a store item"""
        if item_index >= len(self.store_items):
            return {"type": "show_screen"}
        
        item = self.store_items[item_index]
        player = self.current_player
        
        if player.gold >= item["cost"]:
            player.gold -= item["cost"]
            
            if item["type"] == "deck_card":
                # Add card to master deck
                if item["name"] == "Extra Joker":
                    joker_card = Card("joker_bought", "joker", "ALT")
                    self.master_deck.append(joker_card)

                    if current_deck:
                        current_deck.add_card_immediate("joker_bought", "joker")


            elif item["type"] == "augment":
                # Add augment to player
                player.augments.append(item["name"])
            
            return {
                "type": "purchase_success",
                "item": item["name"],
                "remaining_gold": player.gold
            }
        else:
            return {
                "type": "purchase_failed",
                "reason": "Not enough gold"
            }
        
    def add_card_to_deck(self):
        pass

    def draw_store_menu(self, screen):
        """Draw store menu with items and prices"""
        title_text = self.font_large.render("STORE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Show player's gold
        if hasattr(self, 'current_player'):
            gold_text = self.font_medium.render(f"Gold: {self.current_player.gold}", True, (255, 215, 0))
            gold_rect = gold_text.get_rect(center=(self.screen_width // 2, 140))
            screen.blit(gold_text, gold_rect)
        
        # Draw store items
        start_y = 200
        for i, item in enumerate(self.store_items):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            
            # Item name and cost
            item_text = f"{item['name']} - {item['cost']} gold"
            text_surface = self.font_medium.render(item_text, True, color)
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, start_y + i * 60))
            screen.blit(text_surface, text_rect)
            
            # Item description
            desc_surface = self.font_small.render(item['description'], True, (200, 200, 200))
            desc_rect = desc_surface.get_rect(center=(self.screen_width // 2, start_y + i * 60 + 25))
            screen.blit(desc_surface, desc_rect)
            
            # Selection indicator
            if i == self.selected_option:
                indicator = self.font_medium.render(">", True, (255, 255, 0))
                indicator_rect = indicator.get_rect(center=(text_rect.left - 30, text_rect.centery))
                screen.blit(indicator, indicator_rect)
        
        # Back option
        back_index = len(self.store_items)
        back_color = (255, 255, 0) if self.selected_option == back_index else (255, 255, 255)
        back_text = self.font_medium.render("Back to Menu", True, back_color)
        back_rect = back_text.get_rect(center=(self.screen_width // 2, start_y + back_index * 60))
        screen.blit(back_text, back_rect)