import pygame
import random
from paddle import Paddle
from ball import Ball

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.score1 = 0
        self.score2 = 0
        self.paddle1 = Paddle(30, 250)
        self.paddle2 = Paddle(760, 250)
        self.ball = Ball(395, 295)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddle1.move(up=True)
        if keys[pygame.K_s]:
            self.paddle1.move(up=False)
        if keys[pygame.K_UP]:
            self.paddle2.move(up=True)
        if keys[pygame.K_DOWN]:
            self.paddle2.move(up=False)

        result = self.ball.move()
        if result == "left":
            self.score1 += 1
            self.ball = Ball(395, 295)
            self.ball.speed_x = random.choice([-5, 5])
            self.ball.speed_y = random.choice([-5, 5])
        elif result == "right":
            self.score2 += 1
            self.ball = Ball(395, 295)
        self.ball.check_collision(self.paddle1, self.paddle2)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.paddle1.draw(self.screen, color=(137, 207, 240))  # Baby blue
        self.paddle2.draw(self.screen, color=(0, 128, 0))  # Grass green
        self.ball.draw(self.screen)
        font = pygame.font.Font(None, 74)
        score_text1 = font.render(str(self.score1), 1, (255, 255, 255))
        score_text2 = font.render(str(self.score2), 1, (255, 255, 255))
        score_text1 = font.render(str(self.score1), 1, (137, 207, 240))  # Baby blue
        score_text2 = font.render(str(self.score2), 1, (0, 128, 0))  # Grass green
        self.screen.blit(score_text1, (250, 10))
        self.screen.blit(score_text2, (520, 10))
