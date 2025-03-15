
import copy
from board import boards
from pacman import Pacman
from ghost import Ghost, BlueGhost, OrangeGhost, PinkGhost, RedGhost

import config
import pygame
import math
import menu
import time

pygame.init()

X = config.X
screen = pygame.display.set_mode([config.WIDTH, config.HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'
PI = math.pi

# Characters's model
player_images = []
char_size = math.floor(X // 20)
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (char_size, char_size)))
# Blue: 0, Pink: 1, Orange:2, Red: 3, Powerup: 4, Dead: 5
ghosts_images = [pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (char_size, char_size)),
                 pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (char_size, char_size)),
                 pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (char_size, char_size)),
                 pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (char_size, char_size)),
                 pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (char_size, char_size)),
                 pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (char_size, char_size))]

dI = config.dI
dJ = config.dJ

# Initial Characters
pacman = Pacman()

# Blue: 0, Pink: 1, Orange:2, Red: 3
start_index_ghosts = [[config.blue_x, config.blue_y],
               [config.pink_x, config.pink_y],
               [config.orange_x, config.orange_y],
               [config.red_x, config.red_y]]
Ghosts_list = [BlueGhost(0, start_index_ghosts[0][0], start_index_ghosts[0][1], char_size), 
               PinkGhost(1, start_index_ghosts[1][0], start_index_ghosts[1][1], char_size),
               OrangeGhost(2, start_index_ghosts[2][0], start_index_ghosts[2][1], char_size),
               RedGhost(3, start_index_ghosts[3][0], start_index_ghosts[3][1], char_size)]

direction = config.direction

score = config.score

counter = config.counter
flicker = config.flicker

powerup = config.powerup
power_counter = config.power_counter

player_speed = config.player_speed

turns_allowed = config.turn_allowed

startup_counter = config.startup_counter
 
game_over = config.game_over
game_won = config.game_won

direction_command = config.direction_command

# Graphic
def draw_board():
    global dI, dJ
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
    global score, powerup
    # Getting point
    if level[idx_y][idx_x] == 1:
        score += 1
        level[idx_y][idx_x] = 0
    # Getting powerup
    elif level[idx_y][idx_x] == 2:
        powerup = True
        level[idx_y][idx_x] = 0

def pacman_being_catch(idx_x, idx_y):
    global life
print("❤️")
# menu.main()
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
        pacman.can_eat_ghost()
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        pacman.cannot_eat_ghost()
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True
    if config.lifes == 0:
        game_over = True
        run = False
    

    # Screen
    screen.fill('black')

    # Update Score
    score_board = font.render(f"Score: {score}", True, 'white')
    score_rect = score_board.get_rect()
    score_rect.topleft = (0, 0)
    screen.blit(score_board, score_rect)
    get_score(pacman.idx_x, pacman.idx_y)

    #Update Lifes
    lifes_board = font.render(f"❤Life: {config.lifes}", True, 'white')
    lifes_rect = lifes_board.get_rect()
    lifes_rect.topleft = (X - 100, 0)
    screen.blit(lifes_board, lifes_rect)

    # Draw Map
    draw_board()

    # Draw Ghosts
    for i in range(4):
        if Ghosts_list[i].is_eaten():
            Ghosts_list[i].draw(screen, ghosts_images[5])
        elif powerup: 
            Ghosts_list[i].draw(screen, ghosts_images[4])
        else:
            Ghosts_list[i].draw(screen, ghosts_images[i])

    # Draw Pacman
    draw_player(pacman.get_px_x(), pacman.get_px_y(), pacman.direction)

    # print("Blue: ", blue_ghost.get_idx_x(), blue_ghost.get_idx_y())
    # print("Orange: ", orange_ghost.get_idx_x(), orange_ghost.get_idx_y())

    if moving:
        pacman.move_animation(direction_command)
        for i in range(0, 4):
            if powerup:
                # Run away from pacman
                Ghosts_list[i].decrease_speed()
                Ghosts_list[i].move(level, start_index_ghosts[i][0], start_index_ghosts[i][1])
                Ghosts_list[i].increase_speed()
            elif not Ghosts_list[i].is_eaten():
                # Move back to the original place
                Ghosts_list[i].move(level, pacman.get_idx_x(), pacman.get_idx_y())
            else: 
                # Find pacman
                Ghosts_list[i].move(level, start_index_ghosts[i][0], start_index_ghosts[i][1])
            
            if Ghosts_list[i].get_idx_x() == start_index_ghosts[i][0] and Ghosts_list[i].get_idx_y() == start_index_ghosts[i][1]:
                Ghosts_list[i].make_revive()

            if pacman.get_idx_x() == Ghosts_list[i].get_idx_x() and pacman.get_idx_y() == Ghosts_list[i].get_idx_y() and not Ghosts_list[i].is_eaten():
                if powerup:
                    Ghosts_list[i].make_dead()
                    score += (0.1 * (600 - power_counter)) // 1
                else:
                    config.lifes -= 1
                    for i in range(0, 4):
                        Ghosts_list[i].set_position(start_index_ghosts[i][0], start_index_ghosts[i][1])
                    pacman.back_to_original_position()
                    pygame.time.delay(2000)
            
            


    # Get event from players
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
                direction_command = pacman.get_direction()
            if direction_command == 1:
                direction_command = pacman.get_direction()
            if direction_command == 2:
                direction_command = pacman.get_direction()
            if direction_command == 3:
                direction_command = pacman.get_direction()
    pygame.display.flip()
pygame.quit()

