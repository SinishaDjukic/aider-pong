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
        
        # Choose a random angle between -45 and 45 degrees
        angle = math.radians(random.uniform(-45, 45))
        
        # Randomly choose left or right direction
        direction = random.choice([-1, 1])
        
        self.speed_x = direction * self.speed * math.cos(angle)
        self.speed_y = self.speed * math.sin(angle)
        
        self.obstacles = obstacles if obstacles is not None else []

    def normalize_speed(self):
        magnitude = math.sqrt(self.speed_x**2 + self.speed_y**2)
        if magnitude != 0:
            self.speed_x = (self.speed_x / magnitude) * self.speed
            self.speed_y = (self.speed_y / magnitude) * self.speed

    def time_of_impact(self, paddle1, paddle2, obstacles):
        # Calculate the TOI for the ball with respect to paddles and obstacles
        # This is a simplified version and may need adjustments based on the actual game physics
        toi = 1.0  # Default to no collision within the next frame

        # Check collision with paddles
        for paddle in [paddle1, paddle2]:
            if self.rect.colliderect(paddle.rect):
                toi = 0.0
                break

        # Check collision with obstacles
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                toi = 0.0
                break

        return toi

    def increase_speed(self):
        self.speed *= 1.05
        self.normalize_speed()

    def move(self, paddle1, paddle2, obstacles):
        toi = self.time_of_impact(paddle1, paddle2, obstacles)
        self.rect.x += self.speed_x * toi
        self.rect.y += self.speed_y * toi

        if self.rect.left <= 0:
            return "right"
        elif self.rect.right >= 1024:
            return "left"
        
        # Check for top and bottom collisions
        if self.rect.top <= 20:  # 20 is the height of the top box
            self.rect.top = 20
            self.speed_y = abs(self.speed_y)  # Ensure the ball moves downward
            # Ensure the ball is not moving straight vertically
            if abs(self.speed_x) < 0.1:  # If horizontal speed is very low
                self.speed_x = 0.5 if random.random() < 0.5 else -0.5  # Add a small horizontal component
        elif self.rect.bottom >= 768 - 20:  # 20 is the height of the bottom box
            self.rect.bottom = 768 - 20
            self.speed_y = -abs(self.speed_y)  # Ensure the ball moves upward
            # Ensure the ball is not moving straight vertically
            if abs(self.speed_x) < 0.1:  # If horizontal speed is very low
                self.speed_x = 0.5 if random.random() < 0.5 else -0.5  # Add a small horizontal component

        for obstacle in self.obstacles:
            collision_point = self.check_line_collision(obstacle)
            if collision_point:
                self.handle_line_collision(obstacle, collision_point)
                self.increase_speed()  # Increase the ball's speed after hitting an obstacle
                return None

        self.normalize_speed()

    def check_line_collision(self, obstacle):
        # Vector from line start to end
        line_vec = (obstacle.end[0] - obstacle.start[0], obstacle.end[1] - obstacle.start[1])
        
        # Vector from line start to ball center
        to_ball = (self.rect.centerx - obstacle.start[0], self.rect.centery - obstacle.start[1])
        
        # Project to_ball onto line_vec
        line_length_squared = line_vec[0]**2 + line_vec[1]**2
        t = max(0, min(1, (to_ball[0]*line_vec[0] + to_ball[1]*line_vec[1]) / line_length_squared))
        
        # Calculate the closest point on the line
        closest_point = (
            obstacle.start[0] + t * line_vec[0],
            obstacle.start[1] + t * line_vec[1]
        )
        
        # Check if the distance from the ball to the closest point is less than the ball's radius
        dx = self.rect.centerx - closest_point[0]
        dy = self.rect.centery - closest_point[1]
        distance_squared = dx**2 + dy**2
        
        if distance_squared <= self.radius**2:
            return closest_point
        return None

    def handle_line_collision(self, obstacle, collision_point):
        # Calculate the normal vector of the line
        line_vec = (obstacle.end[0] - obstacle.start[0], obstacle.end[1] - obstacle.start[1])
        line_normal = (-line_vec[1], line_vec[0])
        length = math.sqrt(line_normal[0]**2 + line_normal[1]**2)
        line_normal = (line_normal[0] / length, line_normal[1] / length)
        
        # Calculate the dot product of the ball's velocity and the line normal
        dot_product = self.speed_x * line_normal[0] + self.speed_y * line_normal[1]

        # Calculate the reflection vector
        self.speed_x = self.speed_x - 2 * dot_product * line_normal[0]
        self.speed_y = self.speed_y - 2 * dot_product * line_normal[1]

        # Move the ball outside the line
        overlap = self.radius - math.sqrt((self.rect.centerx - collision_point[0])**2 + 
                                          (self.rect.centery - collision_point[1])**2)
        if overlap > 0:
            self.rect.x += line_normal[0] * overlap
            self.rect.y += line_normal[1] * overlap

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
        for paddle in [paddle1, paddle2]:
            if self.rect.colliderect(paddle.rect):
                # Determine if it's a side collision or top/bottom collision
                if abs(self.rect.right - paddle.rect.left) < 10 or abs(self.rect.left - paddle.rect.right) < 10:
                    # Side collision
                    self.speed_x = -self.speed_x
                else:
                    # Top or bottom collision
                    self.speed_y = -self.speed_y

                self.last_deflected_by = "paddle1" if paddle == paddle1 else "paddle2"

                # Move the ball outside the paddle to prevent multiple collisions
                if self.speed_x > 0:
                    self.rect.left = paddle.rect.right
                else:
                    self.rect.right = paddle.rect.left

                # Ensure the ball is not moving straight vertically
                if abs(self.speed_x) < 0.1:  # If horizontal speed is very low
                    self.speed_x = 0.5 if random.random() < 0.5 else -0.5  # Add a small horizontal component

                # Increase ball speed slightly after each paddle hit
                self.increase_speed()
                self.normalize_speed()
                break  # Exit the loop after handling the collision
