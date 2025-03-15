import math
import copy
import config

# Scale
X = config.X
dI = config.dI
dJ = config.dJ

# Map
from board import boards
level = copy.deepcopy(boards)

# Model
# char_size = math.floor(X // 20)
# player_images = []
# for i in range(1, 5):
#     player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (char_size, char_size)))


class Pacman():
    def __init__(self):
        self.direction = 0
        self.turns_allowed = [False, False, False, False]
        self.eat_ghost = False
        self.player_speed = 2
        self.idx_x = 14
        self.idx_y = 30
        self.px_x = self.idx_x * X // 34 + dJ - X // 100
        self.px_y = self.idx_y * X // 34 + dI - X // 100
    # Encapsulation
    def get_px_x(self): return self.px_x
    def get_px_y(self): return self.px_y
    def get_idx_x(self): return self.idx_x
    def get_idx_y(self): return self.idx_y
    def get_direction(self): return self.direction
    def can_eat_ghost(self): self.eat_ghost = True
    def cannot_eat_ghost(self): self.eat_ghost = False

    def back_to_original_position(self):
        self.idx_x, self.idx_y = config.pacman_x, config.pacman_y
        self.px_x = self.idx_x * X // 34 + dJ - X // 100
        self.px_y = self.idx_y * X // 34 + dI - X // 100

    def index_to_px(self):
        px_x = self.idx_x * X // 34 + dJ - X // 100
        px_y = self.idx_y * X // 34 + dI - X // 100
        return px_x, px_y

    def update_index(self, direction_command):
        # right: 0, left: 1, up: 2, down: 3
        if direction_command == 1:
            self.idx_x = math.ceil(((self.px_x - dJ + X // 100) * 34) / X)
            if self.direction == 2: self.idx_y = math.ceil(((self.px_y - dI + X // 100) * 34) / X)
            elif self.direction == 3: self.idx_y = math.floor(((self.px_y - dI + X // 100) * 34) / X)
        elif direction_command == 2:
            self.idx_y = math.ceil(((self.px_y - dI + X // 100) * 34) / X)
            if self.direction == 1: self.idx_x = math.ceil(((self.px_x - dJ + X // 100) * 34) / X)
            elif self.direction == 0: self.idx_x = math.floor(((self.px_x - dJ + X // 100) * 34) / X)
        elif direction_command == 3:
            self.idx_y = math.floor(((self.px_y - dI + X // 100) * 34) / X)
            if self.direction == 1: self.idx_x = math.ceil(((self.px_x - dJ + X // 100) * 34) / X)
            elif self.direction == 0: self.idx_x = math.floor(((self.px_x - dJ + X // 100) * 34) / X)
        elif direction_command == 0:
            self.idx_x = math.floor(((self.px_x - dJ + X // 100) * 34) / X)
            if self.direction == 2: self.idx_y = math.ceil(((self.px_y - dI + X // 100) * 34) / X)
            elif self.direction == 3: self.idx_y = math.floor(((self.px_y - dI + X // 100) * 34) / X)

    def check_position(self):
        # r, l, u , d
        self.turns_allowed = [False, False, False, False]
        # check collisions based on center x and center y of player +/- fudge number
        if self.idx_x < 30 and self.idx_x >= 0 and self.idx_y < 34 and self.idx_y >= 0:
            if level[self.idx_y][self.idx_x + 1] < 3:
                self.turns_allowed[0] = True
            if level[self.idx_y][self.idx_x - 1] < 3:
                self.turns_allowed[1] = True
            if level[self.idx_y - 1][self.idx_x] < 3:
                self.turns_allowed[2] = True
            if level[self.idx_y + 1][self.idx_x] < 3:
                self.turns_allowed[3] = True



    def move_player(self):
        px_x, px_y = self.index_to_px()
        # r, l, u, d
        if self.direction == 0 and self.turns_allowed[0]:
            self.px_x += self.player_speed
            self.px_y = px_y
        elif self.direction == 1 and self.turns_allowed[1]:
            self.px_x -= self.player_speed
            self.px_y = px_y
        if self.direction == 2 and self.turns_allowed[2]:
            self.px_y -= self.player_speed
            self.px_x = px_x
        elif self.direction == 3 and self.turns_allowed[3]:
            self.px_y += self.player_speed
            self.px_x = px_x

    # def draw_player(self, counter):
    #     # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    #     if self.direction == 0:
    #         screen.blit(player_images[counter // 5], (self.px_x, self.px_y))
    #     elif self.direction == 1:
    #         screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (self.px_x, self.px_y))
    #     elif self.direction == 2:
    #         screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (self.px_x, self.px_y))
    #     elif self.direction == 3:
    #         screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (self.px_x, self.px_y))
    
    def check_direction(self, direction_command):
        if direction_command == 0 and self.turns_allowed[0]:
            self.direction = 0
        if direction_command == 1 and self.turns_allowed[1]:
            self.direction = 1
        if direction_command == 2 and self.turns_allowed[2]:
            self.direction = 2
        if direction_command == 3 and self.turns_allowed[3]:
            self.direction = 3    

    def move_animation(self, direction_command):
        self.check_direction(direction_command)
        self.update_index(direction_command)
        self.check_position()
        self.move_player()

        if self.idx_x == 28 and self.idx_y == 15:
            self.idx_x = 2
            self.px_x = self.idx_x * X // 34 + dJ - X // 100
        elif self.idx_x == 1 and self.idx_y == 15:
            self.idx_x = 27
            self.px_x = self.idx_x * X // 34 + dJ - X // 100
        
