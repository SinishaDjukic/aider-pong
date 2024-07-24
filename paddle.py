import pygame

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)
        self.speed = 5

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        elif not up and self.rect.bottom < 600:
            self.rect.y += self.speed

    def draw(self, screen, base_color=(255, 255, 255)):
        # Draw the paddle with a gradient effect
        paddle_height = self.rect.height
        segment_height = paddle_height // 5
        for i in range(5):
            segment_color = (
                max(0, base_color[0] - i * 20),
                max(0, base_color[1] - i * 20),
                max(0, base_color[2] - i * 20)
            )
            segment_rect = pygame.Rect(
                self.rect.x,
                self.rect.y + i * segment_height,
                self.rect.width,
                segment_height
            )
            pygame.draw.rect(screen, segment_color, segment_rect)
