import pygame

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)
        self.speed = 10

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        elif not up and self.rect.bottom < 768:
            self.rect.y += self.speed

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
