import pygame
import random

class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, 700), random.randint(50, 550), 20, 20)
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 215, 0), self.rect)  # Gold color

    def move(self):
        self.rect.x = random.randint(100, 700)
        self.rect.y = random.randint(50, 550)
        self.spawn_time = pygame.time.get_ticks()
