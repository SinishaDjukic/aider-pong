import pygame
import random
import math
from typing import Tuple, Optional, List
from colors import WHITE_BALL

class Ball:
    def __init__(self, x: int, y: int, color: Tuple[int, int, int] = WHITE_BALL, obstacles: List = None):
        self.last_deflected_by = None
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = color
        self.radius = self.rect.width // 2
        self.speed = 5
        
        # Initialize velocity with random angle
        angle = math.radians(random.uniform(-45, 45))
        direction = random.choice([-1, 1])
        self.velocity = pygame.math.Vector2(
            direction * self.speed * math.cos(angle),
            self.speed * math.sin(angle)
        )
        
        self.obstacles = obstacles if obstacles is not None else []
        self.position = pygame.math.Vector2(x, y)
        
        # Add collision cooldown tracking
        self.last_collision_time = 0
        self.collision_cooldown = 100  # milliseconds
        self.last_collision_obstacle = None

    def normalize_velocity(self) -> None:
        """Normalize velocity to maintain constant speed and prevent vertical movement"""
        if self.velocity.length() != 0:
            # Prevent perfectly vertical movement
            if abs(self.velocity.x) < 0.1 * self.speed:
                # Add a horizontal component
                current_sign = 1 if self.velocity.x >= 0 else -1
                self.velocity.x = current_sign * 0.2 * self.speed
                # Adjust y component to maintain speed
                max_y = math.sqrt(self.speed**2 - self.velocity.x**2)
                self.velocity.y = max_y if self.velocity.y > 0 else -max_y
            
            # Normalize to maintain constant speed
            self.velocity.scale_to_length(self.speed)

    def increase_speed(self) -> None:
        """Increase ball speed by 5%"""
        self.speed *= 1.05
        self.normalize_velocity()

    def reflect_velocity(self, normal: pygame.math.Vector2) -> None:
        """Reflect velocity about a normal vector"""
        # v' = v - 2(v·n)n
        self.velocity -= 2 * self.velocity.dot(normal) * normal
        
        # Ensure minimum reflection angle
        min_angle = math.radians(10)
        current_angle = math.atan2(self.velocity.y, self.velocity.x)
        if abs(current_angle) < min_angle:
            sign = 1 if current_angle >= 0 else -1
            self.velocity.rotate_ip(sign * min_angle)

    def circle_line_collision(self, start: Tuple[float, float], end: Tuple[float, float]) -> Optional[Tuple[pygame.math.Vector2, pygame.math.Vector2]]:
        """
        Check collision between circle and line segment.
        Returns (collision_point, normal) if collision occurs, None otherwise.
        """
        # Convert line segment to vector form
        line_start = pygame.math.Vector2(start)
        line_end = pygame.math.Vector2(end)
        line_vec = line_end - line_start
        
        if line_vec.length_squared() == 0:
            return None
            
        # Vector from line start to circle center
        circle_center = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        to_circle = circle_center - line_start
        
        # Project circle onto line
        t = to_circle.dot(line_vec) / line_vec.length_squared()
        
        # Find closest point on line segment
        if t <= 0:
            closest = line_start
        elif t >= 1:
            closest = line_end
        else:
            closest = line_start + t * line_vec
            
        # Check if circle intersects with closest point
        to_closest = circle_center - closest
        distance_squared = to_closest.length_squared()
        
        if distance_squared <= (self.radius * 1.1) ** 2:  # 10% buffer for more reliable collisions
            # Calculate collision normal
            if distance_squared > 0:
                normal = to_closest.normalize()
            else:
                # If circle center is exactly on the line, use perpendicular vector
                normal = pygame.math.Vector2(-line_vec.y, line_vec.x).normalize()
            return closest, normal
            
        return None

    def handle_obstacle_collision(self, obstacle, collision_data: Tuple[pygame.math.Vector2, pygame.math.Vector2]) -> bool:
        """Handle collision with an obstacle. Returns True if collision was handled."""
        current_time = pygame.time.get_ticks()
        
        # Check collision cooldown
        if (obstacle == self.last_collision_obstacle and 
            current_time - self.last_collision_time < self.collision_cooldown):
            return False
            
        collision_point, normal = collision_data
        
        # Update collision tracking
        self.last_collision_time = current_time
        self.last_collision_obstacle = obstacle
        
        # Calculate reflection with more precision
        incoming = self.velocity.normalize()
        dot_product = incoming.dot(normal)
        
        # Only reflect if we're moving towards the obstacle
        if dot_product < 0:
            # Reflect velocity with a slight random variation to prevent repetitive collisions
            reflection = incoming - 2 * dot_product * normal
            
            # Add a minimum angle to prevent near-vertical reflections
            current_angle = math.atan2(reflection.y, reflection.x)
            min_angle = math.radians(15)  # Increased minimum angle
            
            if abs(current_angle) > math.pi/2 - min_angle and abs(current_angle) < math.pi/2 + min_angle:
                # Too close to vertical, adjust the angle
                new_angle = math.pi/2 - min_angle if current_angle > 0 else -math.pi/2 + min_angle
                reflection.x = math.cos(new_angle)
                reflection.y = math.sin(new_angle)
            
            # Add random variation after ensuring non-vertical angle
            angle_variation = math.radians(random.uniform(-5, 5))
            reflection.rotate_ip(angle_variation)
            
            # Update velocity
            self.velocity = reflection * self.speed
            
            # Double check for vertical movement
            if abs(self.velocity.x) < 0.1 * self.speed:
                # Force a minimum horizontal component
                self.velocity.x = 0.2 * self.speed * (1 if self.velocity.x >= 0 else -1)
                # Adjust y to maintain speed
                max_y = math.sqrt(self.speed**2 - self.velocity.x**2)
                self.velocity.y = max_y if self.velocity.y > 0 else -max_y
            
            # Move ball outside obstacle with extra margin
            push_distance = (self.radius * 1.5) - (pygame.math.Vector2(self.rect.centerx, self.rect.centery) - collision_point).length()
            if push_distance > 0:
                self.position += normal * push_distance * 1.2  # Extra push to prevent sticking
                self.rect.center = self.position
            
            self.increase_speed()
            return True
            
        return False

    def move(self, paddle1, paddle2, obstacles) -> Optional[str]:
        """Update ball position and handle collisions"""
        prev_pos = pygame.math.Vector2(self.position)
        self.position += self.velocity
        self.rect.center = self.position

        # Check wall collisions
        if self.rect.top <= 20:
            self.rect.top = 20
            self.velocity.y *= -1
        elif self.rect.bottom >= 768 - 20:
            self.rect.bottom = 768 - 20
            self.velocity.y *= -1

        # Check if ball went past paddles
        if self.rect.right < 0:
            # Ball went past left paddle - point for right player (paddle2)
            self.last_deflected_by = "paddle2"
            return "left"
        elif self.rect.left > 1024:
            # Ball went past right paddle - point for left player (paddle1)
            self.last_deflected_by = "paddle1"
            return "right"

        # Handle paddle collisions
        self.check_collision(paddle1, paddle2)

        # Handle obstacle collisions
        if obstacles:
            movement_vector = self.position - prev_pos
            steps = max(1, int(movement_vector.length() / self.radius))
            collision_handled = False
            
            for i in range(steps + 1):
                if collision_handled:
                    break
                    
                t = i / steps
                check_pos = prev_pos + movement_vector * t
                self.rect.center = check_pos
                
                for obstacle in self.obstacles:
                    collision_data = self.circle_line_collision(obstacle.start, obstacle.end)
                    if collision_data:
                        collision_handled = self.handle_obstacle_collision(obstacle, collision_data)
                        if collision_handled:
                            return None

            # Restore position if no collision was handled
            if not collision_handled:
                self.rect.center = self.position

        self.normalize_velocity()
        return None

    def check_collision(self, paddle1, paddle2) -> None:
        """Handle collisions with paddles"""
        for paddle in [paddle1, paddle2]:
            if self.rect.colliderect(paddle.rect):
                # Calculate hit position relative to paddle center
                hit_pos = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
                
                # Adjust velocity based on hit position
                self.velocity.y = self.speed * hit_pos
                self.velocity.x *= -1
                
                # Ensure minimum horizontal velocity
                min_horizontal = 0.5
                if abs(self.velocity.x) < min_horizontal:
                    self.velocity.x = min_horizontal if self.velocity.x > 0 else -min_horizontal

                self.last_deflected_by = "paddle1" if paddle == paddle1 else "paddle2"

                # Move ball outside paddle
                if self.velocity.x > 0:
                    self.rect.left = paddle.rect.right
                else:
                    self.rect.right = paddle.rect.left
                    
                self.position = pygame.math.Vector2(self.rect.center)
                self.increase_speed()
                self.normalize_velocity()
                break

    def draw(self, screen) -> None:
        """Draw ball with shadow effect"""
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (50, 50, 50, 128), shadow_surface.get_rect())
        screen.blit(shadow_surface, shadow_rect.topleft)
        
        # Draw ball
        pygame.draw.ellipse(screen, self.color, self.rect)
