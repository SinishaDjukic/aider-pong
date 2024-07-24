import pygame
import random
from paddle import Paddle
from powerup import PowerUp
from ball import Ball

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.score1 = 0
        self.score2 = 0
        self.paddle1 = Paddle(30, 250)
        self.paddle2 = Paddle(760, 250)
        self.balls = [Ball(395, 295)]
        self.powerup = PowerUp()

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

        for ball in self.balls:
            result = ball.move()
            if result == "left" or result == "right":
                if result == "left":
                    self.score1 += 1
                else:
                    self.score2 += 1
                self.balls.remove(ball)
                if not any(b.color == (255, 255, 255) for b in self.balls):
                    new_ball = Ball(395, 295)
                    new_ball.speed_x = random.choice([-4, 4])
                    new_ball.speed_y = random.choice([-4, 4])
                    self.balls.append(new_ball)
            ball.check_collision(self.paddle1, self.paddle2)

            if ball.rect.colliderect(self.powerup.rect):
                new_ball = Ball(ball.rect.x, ball.rect.y)
                new_ball.speed_x = ball.speed_x
                new_ball.speed_y = random.choice([-4, 4])
                self.balls.append(new_ball)
                self.balls[-1].color = (255, 165, 0)  # Duck orange
                self.powerup.move()

        if pygame.time.get_ticks() - self.powerup.spawn_time > 15000:
            self.powerup.move()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.paddle1.draw(self.screen, base_color=(137, 207, 240))  # Baby blue
        self.paddle2.draw(self.screen, base_color=(0, 128, 0))  # Grass green
        for ball in self.balls:
            ball.draw(self.screen)
        self.powerup.draw(self.screen)
        font = pygame.font.Font(None, 74)
        score_text1 = font.render(str(self.score1), 1, (255, 255, 255))
        score_text2 = font.render(str(self.score2), 1, (255, 255, 255))
        score_text1 = font.render(str(self.score1), 1, (137, 207, 240))  # Baby blue
        score_text2 = font.render(str(self.score2), 1, (0, 128, 0))  # Grass green
        self.screen.blit(score_text1, (250, 10))
        self.screen.blit(score_text2, (520, 10))
