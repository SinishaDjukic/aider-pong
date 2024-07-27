import pygame

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)
        self.speed = 0
        self.max_speed = 3  # Further reduced for slower movement
        self.acceleration = 0.3  # Further reduced for smoother acceleration
        self.deceleration = 0.3  # Further reduced for smoother deceleration

    def move(self, up=None):
        if up is not None:
            if up:
                if self.rect.top > 20:  # 20 is the height of the top box
                    self.speed = max(self.speed - self.deceleration, -self.max_speed)
                else:
                    self.speed = 0
            else:
                if self.rect.bottom < 768 - 20:  # 20 is the height of the bottom box
                    self.speed = min(self.speed + self.acceleration, self.max_speed)
                else:
                    self.speed = 0
        else:
            # Apply deceleration when no key is pressed
            if self.speed > 0:
                self.speed = max(self.speed - self.deceleration, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.deceleration, 0)

        # Update paddle position
        self.rect.y += self.speed

        # Ensure the paddle does not move beyond the top box
        if self.rect.top < 20:
            self.rect.top = 20
            self.speed = 0

        # Ensure the paddle does not move beyond the bottom box
        if self.rect.bottom > 768 - 20:
            self.rect.bottom = 768 - 20
            self.speed = 0


    def draw(self, screen, base_color=(255, 255, 255), shadow_color=(50, 50, 50), shadow_offset=(5, 5)):
        # Draw the shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += shadow_offset[0]
        shadow_rect.y += shadow_offset[1]
        shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow_surface.fill((*shadow_color[:3], 128))  # 128 is 50% transparency
        screen.blit(shadow_surface, shadow_rect.topleft)
        
        # Draw the paddle
        pygame.draw.rect(screen, base_color, self.rect)
