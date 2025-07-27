import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ZONES
from deck import RummyDeck
from menu import GameMenu
from toast import ToastManager
from gameboard import check_win_condition, calculate_final_scores, determine_winner
import gameboard
import computer_ai


def main():
    #start the game initialization
    print("Starting Rumspringy!")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # Game setup
    background_image = pygame.image.load("Game_Assets/background.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Menu system - start with main menu
    game_menu = GameMenu(SCREEN_WIDTH, SCREEN_HEIGHT, toast_manager=None)
    game_menu.show_main_menu()  # Show main menu immediately
    
    # Toast system
    toast_manager = ToastManager(max_toasts=4)
    
    def show_message(text, duration=None, toast_type="info"):
        """Show toast message - simple FIFO"""
        toast_manager.show_toast(text, duration, toast_type)
    
    # Game state - initialize as None until first game is created
    deck = None
    player = None
    computer = None
    placed_sets = []
    set_owners = []
    
    # Game state
    game_over = False
    is_player_turn = True
    player_has_drawn = False
    

    #game loop and running
    running = True
    while running:
        #Ways to Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("See you again!")
                running = False

            # Handle menu input (always check first)
            if game_menu.is_active:
                action = game_menu.handle_input(event)
                if action:
                    result = game_menu.handle_menu_action(action)
                    
                    if result["type"] == "resume":
                        continue
                    elif result["type"] == "new_game":
                        # Unpack new game state
                        deck, player, computer, placed_sets, set_owners = result["game_state"]
                        game_over = False
                        is_player_turn = True
                        player_has_drawn = False
                        show_message(f"New {result['deck_type']} game started!", toast_type="success")
                        show_message("Draw to start!")
                    elif result["type"] == "quit":
                        running = False
                    elif result["type"] == "show_screen":
                        continue  # Just showing a different screen
                    elif result["type"] == "continue_game":
                        # Unpack continued game state
                        deck, player, computer, placed_sets, set_owners = result["game_state"]
                        
                        # Reset ALL game state variables
                        game_over = False          # Critical - reset game over state
                        is_player_turn = True      # Reset to player's turn
                        player_has_drawn = False   # Reset draw state
                        
                        # Clear any selected cards
                        player.selected_cards.clear()
                        computer.selected_cards.clear()
                        
                        show_message(f"Continuing with preserved progress!", toast_type="success")
                continue

            elif deck is not None and not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and is_player_turn:
                    # Deck click - draw from deck
                    if deck.handle_deck_click(event.pos) and not player_has_drawn:
                        drawn_card = deck.draw_card()
                        if drawn_card:
                            player.add_card_to_hand(drawn_card)
                            player_has_drawn = True
                            show_message(f"Drew from deck: {drawn_card.rank} of {drawn_card.suit}")
                    
                    # Discard pile click - draw from discard
                    elif deck.handle_discard_click(event.pos) and not player_has_drawn:
                        drawn_card = deck.draw_from_discard()
                        if drawn_card:
                            player.add_card_to_hand(drawn_card)
                            player_has_drawn = True
                            show_message(f"Drew from discard: {drawn_card.rank} of {drawn_card.suit}")

                    # Hand card clicks
                    for card in player.hand:
                        if card.handle_click(event.pos):
                            player.toggle_card_selection(card)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and not game_over:
                        game_menu.show_pause_menu(player)
                    elif event.key == pygame.K_h and not game_over:  # H for Help/How to Play
                        game_menu.show_how_to_play()
                    elif not game_over and is_player_turn:
                        if event.key == pygame.K_SPACE:
                            if not player_has_drawn:
                                show_message("Must draw a card first before placing sets!")
                            else:
                                success, message = gameboard.place_player_cards(player, placed_sets, set_owners)
                                show_message(message)

                                if success and len(player.hand) == 0:
                                    calculate_final_scores(player, computer)
                                    winner = determine_winner(player, computer)
                                    game_menu.show_end_game_menu(winner, player, computer)
                                    game_over = True

                        elif event.key == pygame.K_d:
                            if player_has_drawn and len(player.selected_cards) == 1:
                                discarded_card = player.selected_cards[0]
                                player.remove_cards_from_hand([discarded_card])
                                deck.discard_card(discarded_card)
                                show_message(f"You discarded {discarded_card.rank} of {discarded_card.suit}", toast_type="info")
                                
                                # Check if game should end
                                if not game_over and not game_menu.is_active:
                                    if check_win_condition(player, computer, deck):
                                        calculate_final_scores(player, computer)
                                        winner = determine_winner(player, computer)
                                        game_menu.show_end_game_menu(winner, player, computer)
                                        game_over = True
                                    else:
                                        # Continue with computer turn
                                        is_player_turn = False
                                        player_has_drawn = False
                                        show_message("Computer's turn...")
                                        computer_ai.computer_turn(computer, deck, placed_sets, set_owners, toast_manager)
                                        
                                    
                                    # Check win condition after computer turn
                                    if check_win_condition(player, computer, deck):
                                        calculate_final_scores(player, computer)
                                        winner = determine_winner(player, computer)
                                        game_menu.show_end_game_menu(winner, player, computer)
                                        game_over = True
                                    else:
                                        is_player_turn = True
                                        show_message("Your turn! Click deck or discard to draw.", toast_type="turn")



        screen.blit(background_image, (0, 0))

        if deck is not None and not game_menu.is_active:
            deck.draw_deck(screen)
            player.draw_hand(screen)
            computer.draw_hand(screen)

            #turn indication
            turn_pos = ZONES["turn_indicator"]
            turn_text = "Your Turn" if is_player_turn else "Computer's Turn"
            font = pygame.font.Font(None, 36)
            text = font.render(turn_text, True, (255, 255, 0))
            text_rect = text.get_rect(center=(turn_pos[0], turn_pos[1]))
            screen.blit(text, text_rect)

            # Use gameboard functions
            gameboard.position_placed_sets(placed_sets)
            gameboard.draw_gameboard_sets(screen, placed_sets, set_owners)
            gameboard.draw_ui_info(screen, player, computer, placed_sets)

        game_menu.draw(screen)

        if not game_menu.is_active:
            toast_manager.update()
            toast_manager.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

            




if __name__ == "__main__":
    main()
