import pygame
from game import Game
from colors import (
    WHITE_BALL, ORANGE_BALL,
    PLAYER1_COLOR, PLAYER2_COLOR,
    OBSTACLE_COLOR, BACKGROUND_COLOR
)

def draw_rules_screen(screen):
    # Set up colors
    BLACK = BACKGROUND_COLOR
    WHITE = WHITE_BALL
    TITLE_COLOR = ORANGE_BALL
    
    # Fill background
    screen.fill(BLACK)
    
    # Create font objects
    title_font = pygame.font.Font(None, 64)
    rule_font = pygame.font.Font(None, 36)
    
    # Render title
    title = title_font.render("PONG RULES", True, TITLE_COLOR)
    title_rect = title.get_rect(centerx=screen.get_rect().centerx, top=50)
    
    # Rules text with colors
    rules = [
        ("Controls:", WHITE),
        ("Left Player: W/S to move up/down", PLAYER1_COLOR),
        ("Right Player: UP/DOWN arrows to move up/down", PLAYER2_COLOR),
        ("", WHITE),
        ("Scoring:", WHITE),
        ("- White ball: 10 points", WHITE_BALL),
        ("- Orange ball: 5 points", ORANGE_BALL),
        ("", WHITE),
        ("Special Features:", WHITE),
        ("- Hit white balls to create orange balls", WHITE),
        ("- Obstacles reflect balls and increase their speed", OBSTACLE_COLOR),
        ("- First to 100 points wins!", WHITE),
        ("", WHITE),
        ("Press SPACE to start", WHITE)
    ]
    
    # Draw everything
    screen.blit(title, title_rect)
    
    y_offset = 150
    for rule, color in rules:
        rule_surface = rule_font.render(rule, True, color)
        rule_rect = rule_surface.get_rect(centerx=screen.get_rect().centerx, top=y_offset)
        screen.blit(rule_surface, rule_rect)
        y_offset += 40
    
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Pong Game")
    clock = pygame.time.Clock()
    
    # Show rules screen and wait for space
    show_rules = True
    while show_rules:
        draw_rules_screen(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_rules = False
            
        clock.tick(60)
    
    # Start the game
    game = Game(screen)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
