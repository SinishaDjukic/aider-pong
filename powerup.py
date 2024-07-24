import pygame
import random
import math

class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, 700), random.randint(50, 550), 40, 40)
        self.image = pygame.image.load('powerup_icon.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x = random.randint(100, 700)
        self.rect.y = random.randint(50, 550)
        self.spawn_time = pygame.time.get_ticks()
