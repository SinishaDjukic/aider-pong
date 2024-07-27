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
                side_hit = self.check_rotated_collision(obstacle)
                if side_hit:
                    self.handle_rotated_collision(obstacle, side_hit)
                    self.increase_speed()  # Increase the ball's speed after hitting an obstacle
                    return None

        self.normalize_speed()

    def check_rotated_collision(self, obstacle):
        # Get the obstacle's center and create a vector from it to the ball's center
        obstacle_center = obstacle.rect.center
        ball_center = self.rect.center
        relative_vector = (ball_center[0] - obstacle_center[0], ball_center[1] - obstacle_center[1])

        # Rotate the vector by the negative of the obstacle's angle
        angle_rad = math.radians(-obstacle.angle)
        rotated_vector = (
            relative_vector[0] * math.cos(angle_rad) - relative_vector[1] * math.sin(angle_rad),
            relative_vector[0] * math.sin(angle_rad) + relative_vector[1] * math.cos(angle_rad)
        )

        # Check if the rotated point is near the obstacle's edges, considering the ball's radius
        half_width = obstacle.rect.width / 2
        half_height = obstacle.rect.height / 2
        x_distance = abs(rotated_vector[0]) - half_width
        y_distance = abs(rotated_vector[1]) - half_height

        if x_distance <= self.radius and abs(rotated_vector[1]) <= half_height:
            return "left" if rotated_vector[0] < 0 else "right"
        elif y_distance <= self.radius and abs(rotated_vector[0]) <= half_width:
            return "top" if rotated_vector[1] < 0 else "bottom"
        elif math.sqrt(x_distance**2 + y_distance**2) <= self.radius:
            # Corner collision
            return "corner"
        return None

    def handle_rotated_collision(self, obstacle, side_hit):
        # Calculate the obstacle's center
        obstacle_center = obstacle.rect.center
        
        # Calculate the vector from the obstacle's center to the ball's center
        to_ball = (self.rect.centerx - obstacle_center[0], self.rect.centery - obstacle_center[1])
        
        # Rotate this vector by the negative of the obstacle's angle
        angle_rad = math.radians(-obstacle.angle)
        rotated_to_ball = (
            to_ball[0] * math.cos(angle_rad) - to_ball[1] * math.sin(angle_rad),
            to_ball[0] * math.sin(angle_rad) + to_ball[1] * math.cos(angle_rad)
        )
        
        # Determine the normal based on the side hit
        if side_hit == "left":
            normal = (-1, 0)
        elif side_hit == "right":
            normal = (1, 0)
        elif side_hit == "top":
            normal = (0, -1)
        elif side_hit == "bottom":
            normal = (0, 1)
        else:  # Corner collision
            # Normalize the vector from obstacle center to ball center for corner collisions
            length = math.sqrt(rotated_to_ball[0]**2 + rotated_to_ball[1]**2)
            normal = (rotated_to_ball[0] / length, rotated_to_ball[1] / length)
        
        # Rotate the normal back
        rotated_normal = (
            normal[0] * math.cos(-angle_rad) - normal[1] * math.sin(-angle_rad),
            normal[0] * math.sin(-angle_rad) + normal[1] * math.cos(-angle_rad)
        )
        
        # Calculate the dot product of the ball's velocity and the rotated normal
        dot_product = self.speed_x * rotated_normal[0] + self.speed_y * rotated_normal[1]

        # Calculate the reflection vector
        self.speed_x = self.speed_x - 2 * dot_product * rotated_normal[0]
        self.speed_y = self.speed_y - 2 * dot_product * rotated_normal[1]

        # Move the ball outside the obstacle
        overlap = self.radius - math.sqrt((self.rect.centerx - obstacle_center[0])**2 + 
                                          (self.rect.centery - obstacle_center[1])**2)
        if overlap > 0:
            self.rect.x += rotated_normal[0] * overlap
            self.rect.y += rotated_normal[1] * overlap

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
                # Calculate the collision point
                collision_point = self.rect.clip(paddle.rect).center

                # Determine if it's a side collision or top/bottom collision
                if abs(self.rect.right - paddle.rect.left) < 10 or abs(self.rect.left - paddle.rect.right) < 10:
                    # Side collision
                    self.speed_x = -self.speed_x
                    offset = (collision_point[1] - paddle.rect.centery) / (paddle.rect.height / 2)
                    offset = max(-0.7, min(0.7, offset))  # Clamp offset between -0.7 and 0.7
                    self.speed_y += offset * 5  # Adjust the multiplier for desired effect
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
