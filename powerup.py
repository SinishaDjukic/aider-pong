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
