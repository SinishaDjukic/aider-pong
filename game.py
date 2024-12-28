import pygame
import random
from paddle import Paddle
from powerup import PowerUp
from ball import Ball
from obstacle import Obstacle
from colors import WHITE_BALL, ORANGE_BALL, PLAYER1_COLOR, PLAYER2_COLOR

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
        self.obstacles = self.initialize_obstacles(10)
        self.balls = [Ball(502, 374, obstacles=self.obstacles, color=WHITE_BALL)]  # Centered horizontally and vertically
        self.powerup = PowerUp()

    def initialize_obstacles(self, num_obstacles):
        obstacles = []
        for _ in range(num_obstacles):
            new_obstacle = Obstacle()
            while any(self.lines_intersect(new_obstacle, obstacle) for obstacle in obstacles):
                new_obstacle = Obstacle()
            obstacles.append(new_obstacle)
        return obstacles

    def lines_intersect(self, line1, line2):
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        A, B = line1.start, line1.end
        C, D = line2.start, line2.end
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    def update(self):
        """Update game state"""
        keys = pygame.key.get_pressed()
        
        # Move paddles with sub-pixel precision
        paddle_steps = 10
        if keys[pygame.K_w] or keys[pygame.K_s]:
            for _ in range(paddle_steps):
                self.paddle1.move(up=keys[pygame.K_w])
                self.check_ball_paddle_collisions()
        else:
            for _ in range(paddle_steps):
                self.paddle1.move(up=None)
                self.check_ball_paddle_collisions()

        if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            for _ in range(paddle_steps):
                self.paddle2.move(up=keys[pygame.K_UP])
                self.check_ball_paddle_collisions()
        else:
            for _ in range(paddle_steps):
                self.paddle2.move(up=None)
                self.check_ball_paddle_collisions()

        if self.score1 >= 100 or self.score2 >= 100:
            self.display_winner()
            return

        for ball in self.balls[:]:  # Use a copy of the list to safely remove balls
            result = ball.move(self.paddle1, self.paddle2, self.obstacles)
            if result == "left" or result == "right":
                # Determine which player scored based on the last paddle to hit the ball
                scoring_player = ball.last_deflected_by
                
                # Calculate score based on ball color
                if ball.color == WHITE_BALL:
                    score = 10
                elif ball.color == ORANGE_BALL:
                    score = 5
                else:
                    score = 1

                # Award points to the correct player
                if scoring_player == "paddle1":
                    self.score1 += score
                else:
                    self.score2 += score

                # Handle white ball special case
                if ball.color == WHITE_BALL:
                    self.balls.remove(ball)
                    self.paddle1.rect.height = 100  # Reset paddle1 size to default
                    self.paddle2.rect.height = 100  # Reset paddle2 size to default
                    # Ensure only one white ball exists
                    if not any(b.color == WHITE_BALL for b in self.balls):
                        self.balls.append(Ball(502, 374, obstacles=self.obstacles, color=WHITE_BALL))
                    self.timer = 10
                else:
                    self.balls.remove(ball)

            # Check for powerup collisions
            self.check_powerup_collision(ball)

    def check_ball_paddle_collisions(self):
        for ball in self.balls:
            ball.check_collision(self.paddle1, self.paddle2)

    def check_powerup_collision(self, ball):
        if ball.rect.colliderect(self.powerup.rect) and ball.color == WHITE_BALL:
            new_ball = Ball(ball.rect.x, ball.rect.y, obstacles=self.obstacles, color=ORANGE_BALL)  # Duck orange
            # Copy velocity from the original ball
            new_ball.velocity = ball.velocity.copy()
            new_ball.speed = ball.speed
            self.balls.append(new_ball)
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
                while any(self.lines_intersect(new_obstacle, obstacle) for obstacle in self.obstacles):
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

        # Draw white boxes at the top and bottom of the screen
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, screen_width, 20))  # Top box
        pygame.draw.rect(self.screen, (255, 255, 255), (0, screen_height - 20, screen_width, 20))  # Bottom box

        self.paddle1.draw(self.screen, base_color=PLAYER1_COLOR)  # Baby blue
        self.paddle2.draw(self.screen, base_color=PLAYER2_COLOR)  # Bright green
        for ball in self.balls:
            ball.draw(self.screen)
        self.powerup.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Draw the scores without shadow (moved to the end)
        font = pygame.font.Font(None, 74)
        score1_surface = font.render(str(self.score1), True, PLAYER1_COLOR)  # Baby blue
        score2_surface = font.render(str(self.score2), True, PLAYER2_COLOR)  # Bright green

        screen_width = self.screen.get_width()
        score1_x = (screen_width // 4) - (score1_surface.get_width() // 2)
        score2_x = (3 * screen_width // 4) - (score2_surface.get_width() // 2)

        self.screen.blit(score1_surface, (score1_x, 50))
        self.screen.blit(score2_surface, (score2_x, 50))

    def display_winner(self):
        font = pygame.font.Font(None, 150)
        if self.score1 >= 100:
            winner_text = "BLUE WINS!"
            color = PLAYER1_COLOR  # Baby blue
        else:
            winner_text = "GREEN WINS!"
            color = PLAYER2_COLOR  # Bright green

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
        self.balls = [Ball(502, 374, obstacles=self.obstacles, color=WHITE_BALL)]  # Centered horizontally and vertically
        self.powerup = PowerUp()
        # Draw the scores without shadow
        font = pygame.font.Font(None, 74)
        score1_surface = font.render(str(self.score1), True, PLAYER1_COLOR)  # Baby blue
        score2_surface = font.render(str(self.score2), True, PLAYER2_COLOR)  # Bright green

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


        self.paddle1.draw(self.screen, base_color=PLAYER1_COLOR)  # Baby blue
        self.paddle2.draw(self.screen, base_color=PLAYER2_COLOR)  # Bright green
        for ball in self.balls:
            ball.draw(self.screen)
        self.powerup.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
