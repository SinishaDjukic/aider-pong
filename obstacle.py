import pygame
import random

class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, 974), random.randint(50, 718), 50, 50)
        self.color = (128, 0, 0)  # Red burgundy color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
