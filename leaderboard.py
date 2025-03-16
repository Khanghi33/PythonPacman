import pygame
import math
import config
import handle_file


pygame.init()

# Screen scale
WIDTH = config.WIDTH
HEIGHT = config.HEIGHT
Xscale = WIDTH / 612
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Leaderboard")

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font
title_font = pygame.font.SysFont("arialblack", math.floor(70 * Xscale)) 
player_font = pygame.font.SysFont("arialblack", math.floor(25 * Xscale) // 1, bold=False, italic=False) 
exit_font = pygame.font.SysFont("arialblack", math.floor(20 * Xscale) // 1)

def draw_leaderboard(ranked_data):
    screen.fill(BLACK)

    # Rectangle around leaderboard
    rect_x = WIDTH // 34
    rect_y = WIDTH // 32
    rect_width = WIDTH // 34 * 32
    rect_height = WIDTH // 34 * 30
    pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height), 3)

    # Print Leaderboard
    title = title_font.render("Leaderboard", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    # Divide 2 column
    column1_x = rect_x + 50 * Xscale
    column2_x = rect_x + rect_width // 2 + 50 * Xscale
    y_start = WIDTH // 32 * 8
    line_spacing = 40 * Xscale  # line spacing

    # Draw list of players
    if (len(ranked_data) > 0):
        for i, (rank, name, score) in enumerate(ranked_data):
            text = player_font.render(f"{rank}. {name} - {score}", True, WHITE)
            
            if i < 10:  # Col 1
                screen.blit(text, (column1_x, y_start + i * line_spacing))
            elif i < 20:  # Col 2
                screen.blit(text, (column2_x, y_start + (i - 10) * line_spacing))

    # Exit button
    exit_text = exit_font.render("Press ENTER to Exit", True, WHITE)
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, rect_y + rect_height + 10))

def main():
    leaderboard_data = handle_file.read_file() 

    if (len(leaderboard_data) > 0):
        leaderboard_data.sort(key=lambda x: x[1], reverse=True)
    # Make ranked
    ranked_data = [(rank + 1, name, score) for rank, (name, score) in enumerate(leaderboard_data)]   
    running = True
    while running:
        draw_leaderboard(ranked_data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        pygame.display.update()

if __name__ == "__main__":
    main()

