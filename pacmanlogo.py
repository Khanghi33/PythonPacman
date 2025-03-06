import pygame
import random
import time
import pygame.freetype

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 612, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Text Effect")

# Định nghĩa màu sắc
YELLOW = (255, 204, 0)
BLUE = (0, 0, 200)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)

def random_brightness(color):
    factor = random.uniform(0.8, 1.2)
    return (min(int(color[0] * factor), 255),
            min(int(color[1] * factor), 255),
            min(int(color[2] * factor), 255))

# Font chữ nghiêng gần giống Impact có sẵn trên Windows
font = pygame.freetype.SysFont("Arial Black", 80, bold=True, italic=True)

def draw_text(text, x, y, text_color, border_color, background_color):
    text_surface, text_rect = font.render(text, text_color)
    text_rect.center = (x, y)
    
    # Nền chữ nhật cam nhấp nháy (không nghiêng)
    background_rect = text_rect.inflate(80, 50)  # Tăng kích thước nền
    background_surface = pygame.Surface(background_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(background_surface, background_color, (0, 0, *background_rect.size), border_radius=20)
    pygame.draw.rect(background_surface, border_color, (0, 0, *background_rect.size), 10, border_radius=20)
    
    screen.blit(background_surface, background_rect.topleft)
    
    # Viền xanh chữ (vẽ trước để không che khoảng trống bên trong)
    for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4)]:
        shadow_surface, _ = font.render(text, border_color)
        screen.blit(shadow_surface, text_rect.move(dx, dy))
    
    screen.blit(text_surface, text_rect)

def main():
    running = True
    clock = pygame.time.Clock()
    
    while running:
        screen.fill(WHITE)  # Màu nền trắng
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Hiệu ứng nhấp nháy
        text_color = random_brightness(YELLOW)
        border_color = BLUE
        background_color = random_brightness(ORANGE)
        
        # Vẽ chữ PAC-MAN
        draw_text("PAC-MAN", WIDTH // 2, HEIGHT // 2, text_color, border_color, background_color)
        
        pygame.display.flip()
        time.sleep(0.5)
        clock.tick(2)
    
    pygame.quit()

if __name__ == "__main__":
    main()
