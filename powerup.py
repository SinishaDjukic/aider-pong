import pygame
import random
import math

class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, 700), random.randint(50, 550), 80, 80)
        self.image = pygame.image.load('powerup_icon.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.spawn_time = pygame.time.get_ticks()
        self.animation_start_time = pygame.time.get_ticks()
        self.animation_duration = 500  # Animation duration in milliseconds
        self.animation_start_time = pygame.time.get_ticks()

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        if self.animation_start_time:
            elapsed_time = current_time - self.animation_start_time
            if elapsed_time < self.animation_duration:
                # Calculate rotation angle and alpha value
                rotation_angle = (elapsed_time / self.animation_duration) * 360
                alpha_value = (elapsed_time / self.animation_duration) * 255

                # Rotate and fade the image
                rotated_image = pygame.transform.rotate(self.image, rotation_angle)
                rotated_image.set_alpha(alpha_value)

                # Calculate the position to keep the image centered
                new_rect = rotated_image.get_rect(center=self.rect.center)
                screen.blit(rotated_image, new_rect)
            else:
                self.animation_start_time = None
                screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x = random.randint(100, 700)
        self.rect.y = random.randint(50, 550)
        self.spawn_time = pygame.time.get_ticks()
        self.animation_start_time = pygame.time.get_ticks()
    def draw(self, screen):
        # Draw the scores with shadow
        font = pygame.font.Font(None, 74)
        score1_surface = font.render(str(self.score1), True, (255, 255, 255))
        score2_surface = font.render(str(self.score2), True, (255, 255, 255))

        # Create shadow surfaces
        shadow_surface1 = pygame.Surface(score1_surface.get_size(), pygame.SRCALPHA)
        shadow_surface2 = pygame.Surface(score2_surface.get_size(), pygame.SRCALPHA)
        shadow_surface1.fill((50, 50, 50, 128))  # 128 is 50% transparency
        shadow_surface2.fill((50, 50, 50, 128))  # 128 is 50% transparency

        # Blit shadows
        self.screen.blit(shadow_surface1, (50 + 5, 50 + 5))  # Offset by 5 pixels for shadow
        self.screen.blit(shadow_surface2, (924 + 5, 50 + 5))  # Offset by 5 pixels for shadow

        # Blit scores with shadow
        shadow_text1 = font.render(str(self.score1), True, (0, 0, 0, 128))  # Black shadow with 50% transparency
        shadow_text2 = font.render(str(self.score2), True, (0, 0, 0, 128))  # Black shadow with 50% transparency
        self.screen.blit(shadow_text1, (50 + 5, 50 + 5))  # Offset by 5 pixels for shadow
        self.screen.blit(shadow_text2, (924 + 5, 50 + 5))  # Offset by 5 pixels for shadow

        self.screen.blit(score1_surface, (50, 50))
        self.screen.blit(score2_surface, (924, 50))
        screen.blit(self.image, self.rect.topleft)
