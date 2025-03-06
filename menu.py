import pygame
import random
import pygame.freetype
import sys

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Menu")

# Định nghĩa màu sắc
YELLOW = (255, 204, 0)
BLUE = (0, 0, 200)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_CYCLE = [RED, YELLOW, BLUE]  # Màu nhấp nháy

COLORS = [YELLOW]  # Chỉ màu vàng cho option được chọn

# Font chữ
font = pygame.freetype.SysFont("Arial Black", 120, bold=True, italic=True)
menu_font = pygame.freetype.SysFont("Arial Black", 50, italic=True)
sub_text_font = pygame.freetype.SysFont("Bauhaus 93", 50, italic=True)
options = ["PLAY", "LEADERBOARD", "EXIT"]
selected = 0

# Biến điều khiển nhấp nháy
blink_timer = 0
blink_delay = 1000  # Nhấp nháy cực kỳ chậm (1 giây)
blink_index = 0

def draw_text(text, x, y, text_color, border_color, background_color):
    text_surface, text_rect = font.render(text, text_color)
    text_rect.center = (x, y)
    
    background_rect = text_rect.inflate(80, 50)
    background_surface = pygame.Surface(background_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(background_surface, background_color, (0, 0, *background_rect.size), border_radius=20)
    pygame.draw.rect(background_surface, BLUE, (0, 0, *background_rect.size), 10, border_radius=20)
    
    screen.blit(background_surface, background_rect.topleft)
    
    for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4)]:
        shadow_surface, _ = font.render(text, border_color)
        screen.blit(shadow_surface, text_rect.move(dx, dy))
    
    screen.blit(text_surface, text_rect)

def draw_menu():
    global blink_timer, blink_index
    screen.fill(BLACK)
    
    # Cập nhật màu nhấp nháy
    if pygame.time.get_ticks() - blink_timer > blink_delay:
        blink_timer = pygame.time.get_ticks()
        blink_index = (blink_index + 1) % len(COLOR_CYCLE)
    
    blink_color = COLOR_CYCLE[blink_index]
    
    # Vẽ chữ PAC-MAN
    text_color = YELLOW
    border_color = BLUE
    background_color = ORANGE
    draw_text("PAC-MAN", WIDTH // 2, 100, text_color, BLUE, background_color)
    
    # Vẽ chữ 23CLC08-HCMUS với màu nhấp nháy cực chậm
    sub_text = "23CLC08-HCMUS"
    sub_text_surface, sub_text_rect = sub_text_font.render(sub_text, blink_color)
    sub_text_rect.center = (WIDTH // 2, 220)
    screen.blit(sub_text_surface, sub_text_rect)
    
    # Vẽ menu
    for i, text in enumerate(options):
        color = COLORS[0] if i == selected else WHITE
        glow_color = COLORS[0] if i == selected else BLACK
        
        label, _ = menu_font.render(text, color)
        rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
        pygame.draw.rect(screen, glow_color, rect.inflate(45, 25), 3, border_radius=15)
        screen.blit(label, rect)
    
    pygame.display.flip()

def main():
    global selected
    running = True
    clock = pygame.time.Clock()
    
    while running:
        draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        print("Starting Game...")
                    elif selected == 1:
                        print("Opening Leaderboard...")
                    elif selected == 2:
                        running = False
        
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()




