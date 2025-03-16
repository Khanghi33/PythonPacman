import math


# Screen 
WIDTH = 850
HEIGHT = 850
X = WIDTH
dI = HEIGHT // 34
dJ = HEIGHT // 32

# Time flip
fps = 60

# Initial value
direction = 0
direction_command = 0

score = 0
total_point = 0
count_point = 0

startup_counter = 0
counter = 0
flicker = False

powerup = False
power_counter = 0

player_speed = 2
ghost_speed = 1

turn_allowed = [False, False, False, False]

# Initial index position of characters
blue_x, blue_y = 16,16
pink_x, pink_y = 16,16
orange_x, orange_y = 16,16
red_x, red_y = 16,16
pacman_x, pacman_y = 14, 30

# Game value
lifes = 5
game_over = False
game_won = False

PI = math.pi

# Player name
player_name = ""