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
        self.obstacle_timer = 10
        self.last_obstacle_update = pygame.time.get_ticks()
        self.paddle1 = Paddle(30, 334)  # Centered vertically
        self.paddle2 = Paddle(984, 334)  # Centered vertically
        self.obstacles = []
        self.balls = [Ball(502, 374, obstacles=self.obstacles)]  # Centered horizontally and vertically
        self.powerup = PowerUp()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_s]:
            self.paddle1.move(up=keys[pygame.K_w])
        else:
            self.paddle1.move(up=None)

        if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.paddle2.move(up=keys[pygame.K_UP])
        else:
            self.paddle2.move(up=None)

        if self.score1 >= 100 or self.score2 >= 100:
            self.display_winner()
            return

        for ball in self.balls:
            result = ball.move()
            if result == "left" or result == "right":
                if ball.color == (255, 255, 255):  # White ball
                    score = 10
                elif ball.color == (255, 165, 0):  # Orange ball
                    score = 5
                else:
                    score = 1  # Default score for any other color

                if result == "left":
                    self.score2 += score
                else:
                    self.score1 += score

                if ball.color == (255, 255, 255):
                    print(f"Last deflected by: {ball.last_deflected_by}")
                    self.balls.remove(ball)
                    self.paddle1.rect.height = 100  # Reset paddle1 size to default
                    self.paddle2.rect.height = 100  # Reset paddle2 size to default
                    # Ensure only one white ball exists
                    if not any(b.color == (255, 255, 255) for b in self.balls):
                        self.balls.append(Ball(502, 374, obstacles=self.obstacles))  # Re-spawn the ball at the center
                    self.timer = 10
                else:
                    self.balls.remove(ball)
            ball.check_collision(self.paddle1, self.paddle2)

            if ball.rect.colliderect(self.powerup.rect) and ball.color == (255, 255, 255):
                new_ball = Ball(ball.rect.x, ball.rect.y, obstacles=self.obstacles, color=(255, 165, 0))  # Duck orange
                new_ball.speed_x = ball.speed_x
                new_ball.speed_y = random.choice([-4, 4])
                self.balls.append(new_ball)
                if ball.last_deflected_by == "paddle1":
                    self.score1 += 1
                    self.paddle1.rect.height += 10
                elif ball.last_deflected_by == "paddle2":
                    self.score2 += 1
                    self.paddle2.rect.height += 10
                if ball.last_deflected_by == "paddle1":
                    self.score1 += 1
                    self.paddle1.rect.height += 10
                elif ball.last_deflected_by == "paddle2":
                    self.score2 += 1
                    self.paddle2.rect.height += 10
                self.powerup.move()

        if pygame.time.get_ticks() - self.powerup.spawn_time > 15000:
            self.powerup.move()

        # Update the obstacle timer
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_update >= 1000:
            self.obstacle_timer -= 1
            self.last_obstacle_update = current_time
            if self.obstacle_timer <= 0:
                new_obstacle = Obstacle()
                # Ensure the new obstacle does not overlap with existing obstacles
                while any(new_obstacle.rect.colliderect(obstacle.rect) for obstacle in self.obstacles):
                    new_obstacle = Obstacle()
                self.obstacles.append(new_obstacle)
                for ball in self.balls:
                    ball.obstacles = self.obstacles
                self.obstacle_timer = 10

    def draw(self):
        # Draw the background image
        screen_width, screen_height = self.screen.get_size()
        bg_width, bg_height = self.background_image.get_size()
        scale_factor = max(screen_width / bg_width, screen_height / bg_height)
        new_bg_width = int(bg_width * scale_factor)
        new_bg_height = int(bg_height * scale_factor)
        scaled_background = pygame.transform.scale(self.background_image, (new_bg_width, new_bg_height))
        bg_x = (screen_width - new_bg_width) // 2
        bg_y = (screen_height - new_bg_height) // 2
        self.screen.blit(scaled_background, (bg_x, bg_y))

        # Dim the background by adding a semi-transparent black overlay
        dim_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        dim_overlay.fill((0, 0, 0, 128))  # 128 is 50% transparency
        self.screen.blit(dim_overlay, (0, 0))

        # Draw the scores without shadow
        font = pygame.font.Font(None, 74)
        score1_surface = font.render(str(self.score1), True, (137, 207, 240))  # Baby blue
        score2_surface = font.render(str(self.score2), True, (0, 255, 0))  # Bright green

        screen_width = self.screen.get_width()
        score1_x = (screen_width // 4) - (score1_surface.get_width() // 2)
        score2_x = (3 * screen_width // 4) - (score2_surface.get_width() // 2)

        self.screen.blit(score1_surface, (score1_x, 50))
        self.screen.blit(score2_surface, (score2_x, 50))


        self.paddle1.draw(self.screen, base_color=(137, 207, 240))  # Baby blue
        self.paddle2.draw(self.screen, base_color=(0, 255, 0))  # Bright green
        for ball in self.balls:
            ball.draw(self.screen)
        self.powerup.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

    def display_winner(self):
        font = pygame.font.Font(None, 150)
        if self.score1 >= 100:
            winner_text = "BLUE WINS!"
            color = (137, 207, 240)  # Baby blue
        else:
            winner_text = "GREEN WINS!"
            color = (0, 255, 0)  # Bright green

        text_surface = font.render(winner_text, True, color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        # Wait for 5 seconds
        pygame.time.wait(5000)

        # Display "Press any key to restart" message
        font = pygame.font.Font(None, 50)
        restart_text = "Press any key to restart"
        restart_surface = font.render(restart_text, True, (255, 255, 255))  # White color
        restart_rect = restart_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))
        self.screen.blit(restart_surface, restart_rect)
        pygame.display.flip()

        # Wait for key press to restart the game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
        self.reset_game()

    def reset_game(self):
        self.score1 = 0
        self.score2 = 0
        self.timer = 10
        self.last_timer_update = pygame.time.get_ticks()
        self.paddle1 = Paddle(30, 334)  # Centered vertically
        self.paddle2 = Paddle(984, 334)  # Centered vertically
        self.obstacles = []
        self.balls = [Ball(502, 374, obstacles=self.obstacles)]  # Centered horizontally and vertically
        self.powerup = PowerUp()
        # Draw the scores without shadow
        font = pygame.font.Font(None, 74)
        score1_surface = font.render(str(self.score1), True, (137, 207, 240))  # Baby blue
        score2_surface = font.render(str(self.score2), True, (0, 255, 0))  # Bright green

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


        self.paddle1.draw(self.screen, base_color=(137, 207, 240))  # Baby blue
        self.paddle2.draw(self.screen, base_color=(0, 255, 0))  # Bright green
        for ball in self.balls:
            ball.draw(self.screen)
        self.powerup.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
