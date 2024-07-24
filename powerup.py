import pygame
import random

class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, 700), random.randint(50, 550), 40, 40)
        self.image = pygame.image.load('powerup_icon.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.spawn_time = pygame.time.get_ticks()
        self.animation_start_time = self.spawn_time
        self.animation_start_time = self.spawn_time
        self.animation_duration = 1000  # 1 second for the animation

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time

        if elapsed_time < self.animation_duration:
            # Calculate the scale factor
            scale_factor = 1 + 0.5 * (1 - (elapsed_time / self.animation_duration)) * abs(math.sin(elapsed_time / 100))
            scaled_image = pygame.transform.scale(self.image, (int(40 * scale_factor), int(40 * scale_factor)))

            # Calculate the shake offset
            shake_offset = 5 * math.sin(elapsed_time / 50)

            # Draw the scaled and shaken image
            screen.blit(scaled_image, (self.rect.x + shake_offset, self.rect.y + shake_offset))
        else:
            screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x = random.randint(100, 700)
        self.rect.y = random.randint(50, 550)
        self.spawn_time = pygame.time.get_ticks()
