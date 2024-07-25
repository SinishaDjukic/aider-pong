import pygame
import random

class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, 974), random.randint(50, 718), 50, 50)
        self.color = (128, 0, 0)  # Red burgundy color

    def draw(self, screen):
        # Draw the shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow_surface.fill((50, 50, 50, 128))  # 128 is 50% transparency
        screen.blit(shadow_surface, shadow_rect.topleft)
        
        # Draw the obstacle
        pygame.draw.rect(screen, self.color, self.rect)
