import pygame
import random

class Ball:
    def __init__(self, x, y, color=(255, 255, 255), obstacles=None):
        self.last_deflected_by = None  # Track the last user who deflected the ball
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.radius = self.rect.width // 2  # Assuming the ball is a circle and width equals height
        self.speed_x = random.choice([-4, 4])
        self.obstacles = obstacles if obstacles is not None else []
        self.speed_y = random.choice([-4, 4])

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


        if self.rect.left <= 0:
            return "right"
        elif self.rect.right >= 1024:
            return "left"
        if self.rect.top <= self.radius:
            self.rect.top = self.radius  # Correct the position to avoid sticking
            self.speed_y = -self.speed_y
        elif self.rect.bottom >= 768 - self.radius:
            self.rect.bottom = 768 - self.radius  # Correct the position to avoid sticking
            self.speed_y = -self.speed_y

        for obstacle in self.obstacles:
            if self.rect.colliderect(obstacle.rect):
                if abs(self.rect.right - obstacle.rect.left) < abs(self.rect.bottom - obstacle.rect.top) and abs(self.rect.right - obstacle.rect.left) < abs(self.rect.top - obstacle.rect.bottom):
                    self.speed_x = -self.speed_x
                elif abs(self.rect.left - obstacle.rect.right) < abs(self.rect.bottom - obstacle.rect.top) and abs(self.rect.left - obstacle.rect.right) < abs(self.rect.top - obstacle.rect.bottom):
                    self.speed_x = -self.speed_x
                    if self.color == (255, 255, 255):
                        self.last_deflected_by = "paddle2"
                    self.speed_y = -self.speed_y
                return None

    def draw(self, screen):
        # Draw the shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (50, 50, 50, 128), shadow_surface.get_rect())  # 128 is 50% transparency
        screen.blit(shadow_surface, shadow_rect.topleft)
        
        # Draw the ball
        pygame.draw.ellipse(screen, self.color, self.rect)

    def check_collision(self, paddle1, paddle2):
        offset = 0  # Initialize offset
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            # Calculate the deflection based on where the ball hits the paddle
            if self.rect.colliderect(paddle1.rect):
                offset = (self.rect.centery - paddle1.rect.centery) / (paddle1.rect.height / 2)
                if self.color == (255, 255, 255):
                    self.last_deflected_by = "paddle1"
            elif self.rect.colliderect(paddle2.rect):
                offset = (self.rect.centery - paddle2.rect.centery) / (paddle2.rect.height / 2)
            
            # Apply curvature effect: the closer to the edge, the larger the deflection
            self.speed_x = -self.speed_x
            self.speed_y += offset * 5  # Adjust the multiplier as needed for desired effect

        if self.rect.top <= 0 or self.rect.bottom >= 768:
            self.speed_y = -self.speed_y
