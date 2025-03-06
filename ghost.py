import math
import copy

# Scale
X = 612
dI = X // 34
dJ = X // 32

# Map
from board import boards
level = copy.deepcopy(boards)

class Ghost():
    def __init__(self):
        self.direction = 0
        self.turns_allowed = [False, False, False, False]
        self.player_speed = 2
        self.idx_x = 14
        self.idx_y = 30
        dI = X // 34
        dJ = X // 32
        self.px_x = 14 * X // 34 + dJ - X // 100
        self.px_y = 30 * X // 34 + dI - X // 100