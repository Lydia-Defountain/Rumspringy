import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def main():
    #start the game initialization
    print("Starting Rumspringy!")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    #gameboard initialization and setting creation of the play items here
    background_image = pygame.image.load("Game_Assets/background.jpg")
    background_image = pygame.transform.scale(background_image, (1280, 720))


    #game loop and running
    running = True
    while running:
        #Ways to Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("See you again!")
                running = False


        screen.blit(background_image, (0, 0))

        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

            




if __name__ == "__main__":
    main()
