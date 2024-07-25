import pygame
import random
from paddle import Paddle
from powerup import PowerUp
from ball import Ball
from obstacle import Obstacle

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load('background.png')
        self.score1 = 0
        self.score2 = 0
        self.timer = 10
        self.last_timer_update = pygame.time.get_ticks()
        self.paddle1 = Paddle(30, 334)  # Centered vertically
        self.paddle2 = Paddle(984, 334)  # Centered vertically
        self.obstacles = []
        self.balls = [Ball(502, 374, obstacles=self.obstacles)]  # Centered horizontally and vertically
        self.powerup = PowerUp()
        self.obstacles = []

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddle1.move(up=True)
        if keys[pygame.K_s]:
            self.paddle1.move(up=False)
        if keys[pygame.K_UP]:
            self.paddle2.move(up=True)
        if keys[pygame.K_DOWN]:
            self.paddle2.move(up=False)

        for ball in self.balls:
            result = ball.move()
            if result == "left" or result == "right":
                if result == "left":
                    self.score1 += 1
                else:
                    self.score2 += 1
                self.balls.remove(ball)
                # Ensure only one white ball exists
                if not any(b.color == (255, 255, 255) for b in self.balls):
                    self.balls.append(Ball(502, 374, obstacles=self.obstacles))  # Re-spawn the ball at the center
                else:
                    self.balls.append(Ball(502, 374, obstacles=self.obstacles, color=(255, 165, 0)))  # Duck orange
                self.timer = 10
            ball.check_collision(self.paddle1, self.paddle2)

            if ball.rect.colliderect(self.powerup.rect) and ball.color == (255, 255, 255):
                new_ball = Ball(ball.rect.x, ball.rect.y, obstacles=self.obstacles, color=(255, 165, 0))  # Duck orange
                new_ball.speed_x = ball.speed_x
                new_ball.speed_y = random.choice([-4, 4])
                self.balls.append(new_ball)
                self.powerup.move()

        if pygame.time.get_ticks() - self.powerup.spawn_time > 15000:
            self.powerup.move()

        # Update the countdown timer
        current_time = pygame.time.get_ticks()
        if current_time - self.last_timer_update >= 1000:
            self.timer -= 1
            self.last_timer_update = current_time
            if self.timer <= 0:
                self.obstacles.append(Obstacle())
                self.obstacles.append(Obstacle())
                self.timer = 10

    def draw(self):
        # Draw the scores with shadow
        font = pygame.font.Font(None, 74)
        score1_surface = font.render(str(self.score1), True, (255, 255, 255))
        score2_surface = font.render(str(self.score2), True, (255, 255, 255))

        shadow_offset = 5
        shadow_color = (0, 0, 0, 128)  # Black shadow with 50% transparency

        # Create shadow surfaces
        shadow_surface1 = font.render(str(self.score1), True, shadow_color)
        shadow_surface2 = font.render(str(self.score2), True, shadow_color)

        # Blit shadows
        self.screen.blit(shadow_surface1, (50 + shadow_offset, 50 + shadow_offset))
        self.screen.blit(shadow_surface2, (924 + shadow_offset, 50 + shadow_offset))

        # Blit scores
        screen_width = self.screen.get_width()
        score1_x = (screen_width // 4) - (score1_surface.get_width() // 2)
        score2_x = (3 * screen_width // 4) - (score2_surface.get_width() // 2)
        
        self.screen.blit(score1_surface, (score1_x, 50))
        self.screen.blit(score2_surface, (score2_x, 50))
        # Get the dimensions of the screen
        screen_width, screen_height = self.screen.get_size()
        
        # Get the dimensions of the background image
        bg_width, bg_height = self.background_image.get_size()
        
        # Calculate the scaling factor to fill the screen with the image
        scale_factor = max(screen_width / bg_width, screen_height / bg_height)
        
        # Calculate the new size of the background image
        new_bg_width = int(bg_width * scale_factor)
        new_bg_height = int(bg_height * scale_factor)
        
        # Scale the background image
        scaled_background = pygame.transform.scale(self.background_image, (new_bg_width, new_bg_height))
        
        # Calculate the position to center the image on the screen
        bg_x = (screen_width - new_bg_width) // 2
        bg_y = (screen_height - new_bg_height) // 2
        
        # Draw the scaled background image
        self.screen.blit(scaled_background, (bg_x, bg_y))
        # Create a semi-transparent black overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 128 is 50% transparency
        self.screen.blit(overlay, (0, 0))

        # Draw the countdown timer
        timer_font = pygame.font.Font(None, 74)
        timer_surface = timer_font.render(str(self.timer), True, (255, 255, 255))
        timer_x = (screen_width // 2) - (timer_surface.get_width() // 2)
        self.screen.blit(timer_surface, (timer_x, 10))

        self.paddle1.draw(self.screen, base_color=(137, 207, 240))  # Baby blue
        self.paddle2.draw(self.screen, base_color=(0, 128, 0))  # Grass green
        for ball in self.balls:
            ball.draw(self.screen)
        self.powerup.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        font = pygame.font.Font(None, 74)
        
        score_text1 = font.render(str(self.score1), 1, (255, 255, 255))  # White
        score_text2 = font.render(str(self.score2), 1, (255, 255, 255))  # White
        score_text1_x = (screen_width // 4) - (score_text1.get_width() // 2)
        score_text2_x = (3 * screen_width // 4) - (score_text2.get_width() // 2)
        
        self.screen.blit(score_text1, (score_text1_x, 10))
        self.screen.blit(score_text2, (score_text2_x, 10))
