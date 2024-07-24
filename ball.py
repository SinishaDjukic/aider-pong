import pygame

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0:
            return "right"
        elif self.rect.right >= 800:
            return "left"
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def check_collision(self, paddle1, paddle2):
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            # Calculate the deflection based on where the ball hits the paddle
            if self.rect.colliderect(paddle1.rect):
                offset = (self.rect.centery - paddle1.rect.centery) / (paddle1.rect.height / 2)
            else:
                offset = (self.rect.centery - paddle2.rect.centery) / (paddle2.rect.height / 2)
            
            # Apply curvature effect: the closer to the edge, the larger the deflection
            self.speed_x = -self.speed_x
            self.speed_y += offset * 5  # Adjust the multiplier as needed for desired effect

        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.speed_y = -self.speed_y
