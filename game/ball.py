import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        # Move in sub-steps to prevent high-speed tunneling
        steps = max(abs(self.velocity_x), abs(self.velocity_y))
        if steps == 0:
            steps = 1

        for _ in range(steps):
            self.x += self.velocity_x / steps
            self.y += self.velocity_y / steps

            # Bounce off top/bottom walls
            if self.y <= 0:
                self.y = 0
                self.velocity_y *= -1
            elif self.y + self.height >= self.screen_height:
                self.y = self.screen_height - self.height
                self.velocity_y *= -1

    def check_collision(self, player, ai):
        # Collision with player paddle
        if self.rect().colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x *= -1
        # Collision with AI paddle
        elif self.rect().colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x *= -1

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
