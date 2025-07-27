import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ZONES, MESSAGE_DURATION, PURPLE, OTHER_PURPLE
from deck import RummyDeck
from menu import GameMenu
from gameboard import check_win_condition, calculate_final_scores, determine_winner
import gameboard
import computer_ai


def main():
    #start the game initialization
    print("Starting Rumspringy!")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()


    # Message system
    current_message = ""
    message_timer = 0

    def show_message(text, duration=MESSAGE_DURATION):
        """Display a message in the game prompts zone"""
        nonlocal current_message, message_timer
        current_message = text
        message_timer = duration
    
    #gameboard initialization and setting creation of the play items here
    background_image = pygame.image.load("Game_Assets/background.jpg")
    background_image = pygame.transform.scale(background_image, (1280, 720))
    game_menu = GameMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
    deck = RummyDeck("REG")
    deck.shuffle_deck()

    # Initialize first game
    deck, player, computer, placed_sets, set_owners = game_menu.create_new_game("REG")

    #Game state
    is_player_turn = True
    player_has_drawn = False
    game_over = False
    
      

    #game loop and running
    running = True
    while running:
        #Ways to Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("See you again!")
                running = False

            # Handle pause menu input first
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
                        show_message(f"New {result['deck_type']} game started!")
                    elif result["type"] == "quit":
                        running = False
                continue

            elif not game_over:
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
                        game_menu.show_pause_menu()
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
                                    game_menu.show_end_game_menu(winner, player.score, computer.score)
                                    game_over = True

                        elif event.key == pygame.K_d:
                            if player_has_drawn and len(player.selected_cards) == 1:
                                discarded_card = player.selected_cards[0]
                                player.remove_cards_from_hand([discarded_card])
                                deck.discard_card(discarded_card)
                                
                                # Check if game should end
                                if not game_over and not game_menu.is_active:
                                    if check_win_condition(player, computer, deck):
                                        calculate_final_scores(player, computer)
                                        winner = determine_winner(player, computer)
                                        game_menu.show_end_game_menu(winner, player.score, computer.score)
                                        game_over = True
                                    else:
                                        # Continue with computer turn
                                        is_player_turn = False
                                        player_has_drawn = False
                                        show_message("Computer's turn...")
                                        
                                        computer_message = computer_ai.computer_turn(computer, deck, placed_sets, set_owners)
                                    
                                    # Check win condition after computer turn
                                    if check_win_condition(player, computer, deck):
                                        calculate_final_scores(player, computer)
                                        winner = determine_winner(player, computer)
                                        game_menu.show_end_game_menu(winner, player.score, computer.score)
                                        game_over = True
                                    else:
                                        is_player_turn = True
                                        show_message(computer_message + "Your turn! Click deck to draw.")

            
                       
        # Update message timer
        if message_timer > 0:
            message_timer -= 1


        screen.blit(background_image, (0, 0))

        if not game_menu.is_active:
            deck.draw_deck(screen)
            player.draw_hand(screen)
            computer.draw_hand(screen)

            #add instructions
            instructions_pos = ZONES["instructions"]
            font = pygame.font.Font(None, 24)
            instructions = [
                "Click cards to select them (yellow border)",
                "Press SPACE to place selected cards",
                "Press d to discard",
                "Press esc to Pause",
                f"Selected: {len(player.selected_cards)} cards",
                f"Sets on table: {len(placed_sets)}"
            ]
            
            for i, instruction in enumerate(instructions):
                text = font.render(instruction, True, (255, 255, 255))
                screen.blit(text, (instructions_pos[0], instructions_pos[1] + i * 25))


            #turn indication
            turn_pos = ZONES["turn_indicator"]
            turn_text = "Your Turn" if is_player_turn else "Computer's Turn"
            font = pygame.font.Font(None, 36)
            text = font.render(turn_text, True, (255, 255, 0))
            text_rect = text.get_rect(center=(turn_pos[0], turn_pos[1]))
            screen.blit(text, text_rect)

            # Draw game prompts/messages
            prompts_pos = ZONES["game_prompts"]
            font_medium = pygame.font.Font(None, 28)
            
            if message_timer > 0 and current_message:
                # Show current message in bright purple
                message_text = font_medium.render(current_message, True, PURPLE)
                message_rect = message_text.get_rect(center=(prompts_pos[0], prompts_pos[1]))
                screen.blit(message_text, message_rect)
            elif is_player_turn and not player_has_drawn:
                # Show draw prompt in other purple
                draw_prompt = font_medium.render("Click deck or discard pile to draw", True, OTHER_PURPLE)
                prompt_rect = draw_prompt.get_rect(center=(prompts_pos[0], prompts_pos[1]))
                screen.blit(draw_prompt, prompt_rect)

            # Use gameboard functions
            gameboard.position_placed_sets(placed_sets)
            gameboard.draw_gameboard_sets(screen, placed_sets, set_owners)
            gameboard.draw_ui_info(screen, player, computer, placed_sets)

        game_menu.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

            




if __name__ == "__main__":
    main()
