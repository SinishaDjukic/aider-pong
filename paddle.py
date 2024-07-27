import pygame

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)
        self.speed = 2  # Reduced speed by 60% (5 * 0.4 = 2)

    def move(self, up=None):
        if up is not None:
            self.rect.y += -self.speed if up else self.speed
        
        # Ensure the paddle does not move beyond the top box
        if self.rect.top < 20:
            self.rect.top = 20

        # Ensure the paddle does not move beyond the bottom box
        if self.rect.bottom > 768 - 20:
            self.rect.bottom = 768 - 20


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
