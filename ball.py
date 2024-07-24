import pygame

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def check_collision(self, paddle1, paddle2):
        if self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect):
            self.speed_x = -self.speed_x

        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.speed_y = -self.speed_y
