import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.reset()

    def move(self, wall_sound):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
            self.velocity_y *= -1
            if wall_sound:
                wall_sound.play()

# In game/ball.py

    def check_collision(self, player, ai, paddle_sound):
        # Player collision
        if self.velocity_x < 0 and self.rect.colliderect(player.rect):
            # --- MAKE IT FASTER ---
            self.velocity_x *= -1.05 # Increase horizontal speed by 5%
            delta_y = self.rect.centery - player.rect.centery
            self.velocity_y = delta_y * 0.15
            self.rect.left = player.rect.right
            if paddle_sound:
                paddle_sound.play()

        # AI collision
        if self.velocity_x > 0 and self.rect.colliderect(ai.rect):
            # --- MAKE IT FASTER ---
            self.velocity_x *= -1.05 # Increase horizontal speed by 5%
            delta_y = self.rect.centery - ai.rect.centery
            self.velocity_y = delta_y * 0.15
            self.rect.right = ai.rect.left
            if paddle_sound:
                paddle_sound.play()


    def reset(self):
        self.rect.x = self.original_x
        self.rect.y = self.original_y
        self.velocity_x = random.choice([-7, 7])
        self.velocity_y = random.choice([-7, 7])