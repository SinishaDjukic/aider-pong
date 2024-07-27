import pygame
import random
import math

class Obstacle:
    def __init__(self):
        screen_width = 1024
        left_bound = int(screen_width * 0.2)
        right_bound = int(screen_width * 0.8)
        self.rect = pygame.Rect(random.randint(left_bound, right_bound - 60), random.randint(50, 748 - 20), 60, 20)
        self.angle = random.uniform(0, 360)  # Random angle between 0 and 360 degrees
        self.color = (245, 245, 220)  # Beige color
        self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.surface.fill(self.color)

    def draw(self, screen):
        # Create a rotated surface
        rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=self.rect.center)

        # Draw the shadow
        shadow_surface = pygame.Surface(rotated_surface.get_size(), pygame.SRCALPHA)
        shadow_surface.fill((50, 50, 50, 128))  # 128 is 50% transparency
        shadow_rect = shadow_surface.get_rect(center=(rotated_rect.centerx + 5, rotated_rect.centery + 5))
        screen.blit(shadow_surface, shadow_rect.topleft)
        
        # Draw the rotated obstacle
        screen.blit(rotated_surface, rotated_rect.topleft)
