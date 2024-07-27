import pygame
import random
import math

class Ball:
    def __init__(self, x, y, color=(255, 255, 255), obstacles=None):
        self.last_deflected_by = None  # Track the last user who deflected the ball
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.radius = self.rect.width // 2  # Assuming the ball is a circle and width equals height
        self.speed = 5  # Constant speed
        angle = random.uniform(0, 2 * math.pi)
        self.speed_x = self.speed * math.cos(angle)
        self.speed_y = self.speed * math.sin(angle)
        self.obstacles = obstacles if obstacles is not None else []

    def normalize_speed(self):
        magnitude = math.sqrt(self.speed_x**2 + self.speed_y**2)
        if magnitude != 0:
            self.speed_x = (self.speed_x / magnitude) * self.speed
            self.speed_y = (self.speed_y / magnitude) * self.speed

    def increase_speed(self):
        self.speed *= 1.1  # Increase speed by 10%
        self.normalize_speed()

    def increase_speed(self):
        self.speed *= 1.05
        self.normalize_speed()

    def move(self):
        steps = max(abs(int(self.speed_x)), abs(int(self.speed_y)), 1)
        dx = self.speed_x / steps
        dy = self.speed_y / steps

        for _ in range(steps):
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.left <= 0:
                return "right"
            elif self.rect.right >= 1024:
                return "left"
            if self.rect.top <= 20 + self.radius:  # 20 is the height of the top box
                self.rect.top = 20 + self.radius  # Correct the position to avoid sticking
                self.speed_y = -self.speed_y
            elif self.rect.bottom >= 768 - 20 - self.radius:  # 20 is the height of the bottom box
                self.rect.bottom = 768 - 20 - self.radius  # Correct the position to avoid sticking
                self.speed_y = -self.speed_y

            for obstacle in self.obstacles:
                if self.rect.colliderect(obstacle.rect):
                    if abs(self.rect.right - obstacle.rect.left) < abs(self.rect.bottom - obstacle.rect.top) and abs(self.rect.right - obstacle.rect.left) < abs(self.rect.top - obstacle.rect.bottom):
                        self.rect.right = obstacle.rect.left
                        self.speed_x = -self.speed_x
                    elif abs(self.rect.left - obstacle.rect.right) < abs(self.rect.bottom - obstacle.rect.top) and abs(self.rect.left - obstacle.rect.right) < abs(self.rect.top - obstacle.rect.bottom):
                        self.rect.left = obstacle.rect.right
                        self.speed_x = -self.speed_x
                    elif abs(self.rect.bottom - obstacle.rect.top) < abs(self.rect.right - obstacle.rect.left) and abs(self.rect.bottom - obstacle.rect.top) < abs(self.rect.left - obstacle.rect.right):
                        self.rect.bottom = obstacle.rect.top
                        self.speed_y = -self.speed_y
                    elif abs(self.rect.top - obstacle.rect.bottom) < abs(self.rect.right - obstacle.rect.left) and abs(self.rect.top - obstacle.rect.bottom) < abs(self.rect.left - obstacle.rect.right):
                        self.rect.top = obstacle.rect.bottom
                        self.speed_y = -self.speed_y
                    self.increase_speed()  # Increase the ball's speed after hitting an obstacle
                    return None

        self.normalize_speed()

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
            colliding_paddle = paddle1 if self.rect.colliderect(paddle1.rect) else paddle2
            
            # Check if the ball hits the top or bottom of the paddle
            if self.rect.bottom > colliding_paddle.rect.top and self.rect.top < colliding_paddle.rect.bottom:
                # Side collision
                offset = (self.rect.centery - colliding_paddle.rect.centery) / (colliding_paddle.rect.height / 2)
                self.speed_x = -self.speed_x
            else:
                # Top or bottom collision
                self.speed_y = -self.speed_y
                offset = 0  # No horizontal deflection for top/bottom collisions
            
            self.last_deflected_by = "paddle1" if colliding_paddle == paddle1 else "paddle2"
            
            # Clamp the offset between -0.9 and 0.9
            offset = max(-0.9, min(0.9, offset))
            
            # Apply curvature effect only for side collisions
            if self.speed_x != 0:
                self.speed_y += offset * 5  # Adjust the multiplier as needed for desired effect
            
            self.normalize_speed()
