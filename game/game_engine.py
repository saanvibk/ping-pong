import pygame
from pygame import mixer
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

# Initialize mixer
mixer.init()
SCORE_SOUND = mixer.Sound("assets/score.wav")

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.winning_score = 5

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            SCORE_SOUND.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            SCORE_SOUND.play()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def check_game_over(self, screen):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            message = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"
            screen.fill((0, 0, 0))

            font = pygame.font.SysFont("Arial", 50)
            text = font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text, text_rect)

            font_small = pygame.font.SysFont("Arial", 30)
            option_text = font_small.render("Press 3,5,7 for Best-of or ESC to Exit", True, WHITE)
            option_rect = option_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            screen.blit(option_text, option_rect)
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_3:
                            self.winning_score = 2
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.winning_score = 3
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.winning_score = 4
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()

            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
            return True
        return False
