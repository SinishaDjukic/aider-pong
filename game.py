import pygame
from paddle import Paddle
from ball import Ball

class Game:
    def __init__(self, screen):
        self.screen = screen
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

        self.ball.move()
        self.ball.check_collision(self.paddle1, self.paddle2)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.paddle1.draw(self.screen)
        self.paddle2.draw(self.screen)
        self.ball.draw(self.screen)
