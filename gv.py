import pygame
import copy
from board import boards

# Screen scaling
WIDTH = 612
X = WIDTH
dI = X // 34
dJ = X // 32


# Game setting
screen = pygame.display.set_mode([WIDTH, WIDTH])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'
game_over = False
game_won = False

counter = 0
flicker = False



