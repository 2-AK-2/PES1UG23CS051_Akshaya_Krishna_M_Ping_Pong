# game/paddle.py
import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 7

    def move(self, dy, screen_height):
        self.rect.y += dy
        # Keep the paddle on the screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def auto_track(self, ball, screen_height):
        # A simple AI to track the ball's y position
        if ball.rect.centery < self.rect.centery:
            self.move(-self.speed, screen_height)
        elif ball.rect.centery > self.rect.centery:
            self.move(self.speed, screen_height)