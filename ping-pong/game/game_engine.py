# game/game_engine.py
import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)
GRAY = (40, 40, 40)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 15
        self.paddle_height = 100
        self.winning_score = 5 # Default winning score

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 25, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 15, 15, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 24)
        
        try:
            self.paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
            self.wall_bounce_sound = pygame.mixer.Sound("wall_bounce.wav")
            self.score_sound = pygame.mixer.Sound("score.wav")
        except pygame.error:
            print("Warning: Sound files not found. Game will run without sound.")
            self.paddle_hit_sound = None
            self.wall_bounce_sound = None
            self.score_sound = None

    def display_start_menu(self, screen):
        title_text = self.font.render("Ping Pong", True, WHITE)
        prompt_text = self.small_font.render("Press SPACE to Start", True, WHITE)
        
        screen.blit(title_text, (self.width//2 - title_text.get_width()//2, self.height//2 - 100))
        screen.blit(prompt_text, (self.width//2 - prompt_text.get_width()//2, self.height//2 + 20))


    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Move up with 'W' OR the Up Arrow key
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.move(-10, self.height)
        # Move down with 'S' OR the Down Arrow key
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move(self.wall_bounce_sound)
        self.ball.check_collision(self.player, self.ai, self.paddle_hit_sound)

        winner = None
        if self.ball.rect.left <= 0:
            self.ai_score += 1
            if self.score_sound: self.score_sound.play()
            self.ball.reset()
        elif self.ball.rect.right >= self.width:
            self.player_score += 1
            if self.score_sound: self.score_sound.play()
            self.ball.reset()
            
        if self.player_score >= self.winning_score:
            winner = "Player"
        elif self.ai_score >= self.winning_score:
            winner = "AI"

        self.ai.auto_track(self.ball, self.height)
        return winner

    def render(self, screen):
        # This now correctly draws the paddle's rect object
        pygame.draw.rect(screen, WHITE, self.player.rect)
        pygame.draw.rect(screen, WHITE, self.ai.rect)
        pygame.draw.ellipse(screen, WHITE, self.ball.rect)
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        
    def display_game_over(self, screen, winner):
        title_text = self.font.render(f"{winner} Wins!", True, WHITE)
        prompt1 = self.small_font.render("Play Again?", True, WHITE)
        prompt2 = self.small_font.render("Press (3) Best of 3 | (5) Best of 5 | (7) Best of 7", True, WHITE)
        prompt3 = self.small_font.render("Press (ESC) to Exit", True, WHITE)
        
        screen.blit(title_text, (self.width//2 - title_text.get_width()//2, self.height//2 - 100))
        screen.blit(prompt1, (self.width//2 - prompt1.get_width()//2, self.height//2 + 20))
        screen.blit(prompt2, (self.width//2 - prompt2.get_width()//2, self.height//2 + 50))
        screen.blit(prompt3, (self.width//2 - prompt3.get_width()//2, self.height//2 + 80))

    def reset_game(self, score_limit):
        self.winning_score = score_limit
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()

    def render(self, screen):
        # Draw paddles with rounded corners and a border
        pygame.draw.rect(screen, WHITE, self.player.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.ai.rect, border_radius=10)
        
        # Draw the ball and centerline
        pygame.draw.ellipse(screen, WHITE, self.ball.rect)
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4 - player_text.get_width()//2, 20))
        screen.blit(ai_text, (self.width * 3//4 - ai_text.get_width()//2, 20))