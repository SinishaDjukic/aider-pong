import pygame
import random
import math

import pygame
import random
import math

class Obstacle:
    def __init__(self):
        screen_width = 1024
        left_bound = int(screen_width * 0.2)
        right_bound = int(screen_width * 0.8)
        self.start = (random.randint(left_bound, right_bound), random.randint(50, 748 - 20))
        angle = random.uniform(0, 2 * math.pi)
        length = 60
        self.end = (
            self.start[0] + length * math.cos(angle),
            self.start[1] + length * math.sin(angle)
        )
        self.rect = pygame.Rect(
            min(self.start[0], self.end[0]),
            min(self.start[1], self.end[1]),
            abs(self.start[0] - self.end[0]),
            abs(self.start[1] - self.end[1])
        )
        self.color = (245, 245, 220)  # Beige color

    def draw(self, screen):
        # Draw the shadow
        shadow_start = (self.start[0] + 5, self.start[1] + 5)
        shadow_end = (self.end[0] + 5, self.end[1] + 5)
        pygame.draw.line(screen, (50, 50, 50, 128), shadow_start, shadow_end, 3)
        
        # Draw the obstacle line
        pygame.draw.line(screen, self.color, self.start, self.end, 3)
