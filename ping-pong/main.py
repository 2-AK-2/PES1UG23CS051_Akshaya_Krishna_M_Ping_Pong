# main.py
import pygame
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()
pygame.mixer.init() # Initialize the mixer for sound

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)

# Clock
clock = pygame.time.Clock()
FPS = 60

def main():
    engine = GameEngine(WIDTH, HEIGHT)
    running = True
    game_state = "START_MENU"  # Start with the menu!
    winner = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle input for the start menu
            if game_state == "START_MENU" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "PLAYING"

            # --- THIS IS THE CORRECTED SECTION ---
            # Handle input for replay
            if game_state == "GAME_OVER" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    engine.reset_game(3)
                    game_state = "PLAYING"
                elif event.key == pygame.K_5:
                    engine.reset_game(5)
                    game_state = "PLAYING"
                elif event.key == pygame.K_7:
                    engine.reset_game(7)
                    game_state = "PLAYING"
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Make sure this is outside the event loop
        SCREEN.fill(GRAY)

        if game_state == "START_MENU":
            engine.display_start_menu(SCREEN)
        
        elif game_state == "PLAYING":
            engine.handle_input()
            winner = engine.update()
            engine.render(SCREEN)
            if winner:
                game_state = "GAME_OVER"
        
        elif game_state == "GAME_OVER":
            engine.render(SCREEN) # Show final score
            engine.display_game_over(SCREEN, winner)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()