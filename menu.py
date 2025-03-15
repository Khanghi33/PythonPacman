import pygame
import config
import handle_file
import random
import pygame.freetype
import sys
import leaderboard


pygame.init()

# Screen scaling
# WIDTH, HEIGHT = config.WIDTH, config.HEIGHT
WIDTH, HEIGHT = config.WIDTH, config.HEIGHT
Xscale = WIDTH / 800
print(Xscale)
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pacman Menu")

# Define color
YELLOW = (255, 204, 0)
BLUE = (0, 0, 200)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
COLOR_CYCLE = [RED, YELLOW, BLUE]  # Flick color

COLORS = [YELLOW] 

# Font
font = pygame.freetype.SysFont("Arial Black", 120 * Xscale, bold=True, italic=True)
menu_font = pygame.freetype.SysFont("Arial Black", 50 * Xscale, italic=True)
sub_text_font = pygame.freetype.SysFont("Bauhaus 93", 50 * Xscale, italic=True)
name_font = pygame.font.SysFont("arial narrow", WIDTH // 20)
input_font = pygame.font.SysFont("arial narrow", WIDTH // 25)
options = ["PLAY", "LEADERBOARD", "EXIT"]
options2 = ["LEVEL1", "LEVEL2", "LEVEL3", "LEVEL4", "LEVEL5", "LEVEL6", "BACK"]
selected = 0

# Flicker
blink_timer = 0
blink_delay = 1000  # time (1 second)
blink_index = 0

def draw_text(text, x, y, text_color, border_color, background_color):
    text_surface, text_rect = font.render(text, text_color)
    text_rect.center = (x, y)
    
    background_rect = text_rect.inflate(80 * Xscale // 1, 50 * Xscale // 1)
    background_surface = pygame.Surface(background_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(background_surface, background_color, (0, 0, *background_rect.size), border_radius=(20))
    pygame.draw.rect(background_surface, BLUE, (0, 0, *background_rect.size), 10, border_radius=(20))
    
    screen.blit(background_surface, background_rect.topleft)
    
    for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4)]:
        shadow_surface, _ = font.render(text, border_color)
        screen.blit(shadow_surface, text_rect.move(dx, dy))
    
    screen.blit(text_surface, text_rect)

def enter_name():
    name = ""
    active = True
    flag = False

    while active:
        screen.fill(BLACK)

        # Draw PAC-MAN
        text_color = YELLOW
        border_color = BLUE
        background_color = ORANGE
        draw_text("PAC-MAN", WIDTH // 2, 100 * Xscale, text_color, BLUE, background_color)

        # Enter name
        text_surface = name_font.render("Enter Your Name:", True, YELLOW)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 40))

        # Rectangle of typing answrer
        input_box = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, HEIGHT // 20)
        pygame.draw.rect(screen, WHITE, input_box, 2)

        # Show typing
        name_surface = input_font.render(name, True, WHITE)
        screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

        # Username already existed text
        warning_surface = name_font.render("Username has already existed!!", True, RED)
        if flag == True:
            screen.blit(warning_surface, (WIDTH // 2 - warning_surface.get_width() // 2, HEIGHT // 2 + 50))

        # Update screen
        pygame.display.update()

        # Event from users
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if handle_file.check_already_name(name):
                        flag = True
                    else:
                        return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]  # Remove the last character
                elif len(name) < 8:  # Limit to 8 words
                    name += event.unicode  # Add character
        


def draw_menu(type):
    global blink_timer, blink_index
    screen.fill(BLACK)
    
    # Update flicker screen
    if pygame.time.get_ticks() - blink_timer > blink_delay:
        blink_timer = pygame.time.get_ticks()
        blink_index = (blink_index + 1) % len(COLOR_CYCLE)
    
    blink_color = COLOR_CYCLE[blink_index]
    
    # Draw PAC-MAN
    text_color = YELLOW
    border_color = BLUE
    background_color = ORANGE
    draw_text("PAC-MAN", WIDTH // 2, 100 * Xscale, text_color, BLUE, background_color)
    
    
    # Draw menu
    if (type == 1):
        # Draw 23CLC08-HCMUS
        sub_text = "23CLC08-HCMUS"
        sub_text_surface, sub_text_rect = sub_text_font.render(sub_text, blink_color)
        sub_text_rect.center = (WIDTH // 2, 220 * Xscale)
        screen.blit(sub_text_surface, sub_text_rect)

        for i, text in enumerate(options):
            color = COLORS[0] if i == selected else WHITE
            glow_color = COLORS[0] if i == selected else BLACK
            
            label, _ = menu_font.render(text, color)
            rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
            pygame.draw.rect(screen, glow_color, rect.inflate(45, 25), 3, border_radius=15)
            screen.blit(label, rect)
    elif type == 2:
        for i, text in enumerate(options2):
            color = COLORS[0] if i == selected else WHITE
            glow_color = COLORS[0] if i == selected else BLACK
            
            label, _ = menu_font.render(text, color)
            rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60 - 100))
            pygame.draw.rect(screen, glow_color, rect.inflate(45, 25), 3, border_radius=15)
            screen.blit(label, rect)
    elif type == 3:
        config.player_name = enter_name()
        
    
    pygame.display.flip()

def main():
    global selected
    running = True
    clock = pygame.time.Clock()
    type = 1
    
    while running:
        draw_menu(type)
        if type == 3:
            return selected
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if type == 1:
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            print("Starting Game...")
                            type = 2
                        elif selected == 1:
                            print("Opening Leaderboard...")
                            leaderboard.main()
                        elif selected == 2:
                            running = False
                            pygame.quit()
                elif type == 2:
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options2)
                    elif event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options2)
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            print("Starting Game level 1...")
                        elif selected == 1:
                            print("Starting Game level 2...")
                        elif selected == 2:
                            print("Starting Game level 3...")
                        elif selected == 3:
                            print("Starting Game level 4...")
                        elif selected == 4:
                            print("Starting Game level 5...")
                        elif selected == 5:
                            print("Starting Game level 6...")
                            type = 3
                        elif selected == 6:
                            type = 1
                        if (type == 2): return selected
        
        clock.tick(60)
    sys.exit()
    pygame.quit()
    

if __name__ == "__main__":
    main()




