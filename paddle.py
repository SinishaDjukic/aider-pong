import pygame

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)
        self.speed = 5

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        elif not up and self.rect.bottom < 600:
            self.rect.y += self.speed

    def draw(self, screen, base_color=(255, 255, 255)):
        pygame.draw.rect(screen, base_color, self.rect)
