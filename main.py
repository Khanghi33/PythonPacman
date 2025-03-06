
import copy
from board import boards
from pacman import Pacman

import pygame
import math
import time

pygame.init()

WIDTH = 612
X = WIDTH
screen = pygame.display.set_mode([WIDTH, WIDTH])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'
PI = math.pi
player_images = []
char_size = math.floor(X // 20)
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (char_size, char_size)))

player_x = 14
player_y = 30
dI = X // 34
dJ = X // 32
playerx = player_x * X // 34 + dJ - X // 100
playery = player_y * X // 34 + dI - X // 100

direction = 0

score = 0

counter = 0
flicker = False

powerup = False
power_counter = 0

player_speed = 2

turns_allowed = [False, False, False, False]

startup_counter = 0
lives = 3
game_over = False
game_won = False

direction_command = 0

def draw_board():
    dI = X // 34
    dJ = X // 32
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 68), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 68), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * X / 34 + dJ + X // 68, i * X // 34 + dI),
                                 (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 32), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * X / 34 + dJ, i * X // 34 + dI + X // 68),
                                 (j * X // 34 + dJ + X // 34, i * X // 34 + dI + X // 68), 3)
            if level[i][j] == 5:
                pygame.draw.line(screen, color, (j * X // 34 + dJ, i * X // 34 + dI + X // 68), (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 68), 3)
                pygame.draw.line(screen, color, (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 68), (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 34), 3)
            if level[i][j] == 6:
                pygame.draw.line(screen, color, (j * X // 34 + dJ + X // 34, i * X // 34 + dI + X // 68), (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 68), 3)
                pygame.draw.line(screen, color, (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 68), (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 34), 3)
            if level[i][j] == 7:
                pygame.draw.line(screen, color, (j * X // 34 + dJ + X // 68, i * X // 34 + dI), (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 68), 3)
                pygame.draw.line(screen, color, (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 68), (j * X // 34 + dJ + X // 34, i * X // 34 + dI + X // 68), 3)
            if level[i][j] == 8:
                pygame.draw.line(screen, color, (j * X // 34 + dJ + X // 68, i * X // 34 + dI), (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 68), 3)
                pygame.draw.line(screen, color, (j * X // 34 + dJ, i * X // 34 + dI + X // 68), (j * X // 34 + dJ + X // 68, i * X // 34 + dI + X // 68), 3)

            # if level[i][j] == 5:
            #     pygame.draw.arc(screen, color, [(j * X // 34 + dJ), (i * X // 34 + dI), X // 34, X // 34],
            #                     j * X // 34 + dJ, i * X // 34 + dI + X // 68, 3)
            # if level[i][j] == 6:
            #     pygame.draw.arc(screen, color,
            #                     [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            # if level[i][j] == 7:
            #     pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
            #                     3 * PI / 2, 3)
            # if level[i][j] == 8:
            #     pygame.draw.arc(screen, color,
            #                     [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
            #                     2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * X // 34 + dJ, i * X // 34 + dI + X // 68),
                                 (j * X // 34 + dJ + X // 34, i * X // 34 + dI + X // 68), 3)

def draw_player(playerx, playery, direction):
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (playerx, playery))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (playerx, playery))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (playerx, playery))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (playerx, playery))

def get_score(idx_x, idx_y):
    global score
    if level[idx_y][idx_x] == 1:
        score += 1
        level[idx_y][idx_x] = 0

pacman = Pacman()
run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')

    # Update Score
    score_board = font.render(f"Score: {score}", True, 'white')
    score_rect = score_board.get_rect()
    score_rect.topleft = (0, 0)
    screen.blit(score_board, score_rect)
    get_score(pacman.idx_x, pacman.idx_y)


    # Map
    draw_board()
    # center_x, center_y = px_to_index(playerx, playery, direction_command)

    draw_player(pacman.get_px_x(), pacman.get_px_y(), pacman.direction)
    # print(pacman.get_idx_x(), pacman.get_idx_y())
    if moving:
        pacman.move_animation(direction_command)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if direction_command == 0:
                direction_command = pacman.direction
            if direction_command == 1:
                direction_command = pacman.direction
            if direction_command == 2:
                direction_command = pacman.direction
            if direction_command == 3:
                direction_command = pacman.direction

    # if direction_command == 0 and turns_allowed[0]:
    #     direction = 0
    # if direction_command == 1 and turns_allowed[1]:
    #     direction = 1
    # if direction_command == 2 and turns_allowed[2]:
    #     direction = 2
    # if direction_command == 3 and turns_allowed[3]:
    #     direction = 3
    pygame.display.flip()
pygame.quit()

