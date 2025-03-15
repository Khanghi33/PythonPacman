import math
import config
import heapq
import random

X = config.X
dJ = config.dJ
dI = config.dI

# Storing position of 4 ghost in the same time
Ghosts_position = [[0, 0], [0, 0], [0, 0], [0, 0]]

# def check_opposite_direction(prev_di , next_di):
#     if prev_di == 1 and next_di == 0: return True
#     elif prev_di == 0 and next_di == 1: return True
#     elif prev_di == 2 and next_di == 3: return True
#     elif prev_di == 3 and next_di == 2: return True
#     return False

dfs_visited = [()]
def sort_manhattan_distance(ghost_x, ghost_y, pacman_x, pacman_y): 
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    direction_values = [0, 1, 2, 3]  # Corresponding to direction constants

    # Tính toán khoảng cách Manhattan cho từng hướng di chuyển
    possible_moves = []
    for i, (dx, dy) in enumerate(directions):
        new_x, new_y = ghost_x + dx, ghost_y + dy
        distance = abs(new_x - pacman_x) + abs(new_y - pacman_y)
        possible_moves.append((distance, direction_values[i], (dx, dy)))

    # Sắp xếp theo khoảng cách Manhattan giảm dần, nếu bằng nhau thì theo direction_values giảm dần
    possible_moves.sort(key=lambda x: (-x[0], -x[1]))

    # Trả về danh sách direction_values và directions đã sắp xếp
    sorted_direction_values = [move[1] for move in possible_moves]
    sorted_directions = [move[2] for move in possible_moves]
    
    return sorted_direction_values, sorted_directions



def is_path_same_at_first(oldpath, newpath):
    for i in range(1, 3):
        if oldpath[i] != newpath[i]:
            return False
    return True


#Ghost class
class Ghost():
    def __init__(self, id, start_x, start_y, width):
        # ID (Blue: 0, Pink: 1, Orange: 2, Red: 3)
        self.id = id

        # turn can be move
        self.turns_allowed = [False, False, False, False]

        # Grid position
        self.idx_x = start_x
        self.idx_y = start_y

        # Set ghost position in Ghosts_position[][]
        Ghosts_position[self.id][0] = self.idx_x
        Ghosts_position[self.id][1] = self.idx_y

        # Screen dimensions
        self.WIDTH = width
        dI = X // 34
        dJ = X // 32
        
        # Pixel position calculation based on grid position
        self.px_x = self.idx_x * X // 34 + dJ - X // 100
        self.px_y = self.idx_y * X // 34 + dI - X // 100
        
        # Direction (0-RIGHT, 1-LEFT, 2-UP, 3-DOWN)
        self.prev_direction = 0
        self.direction = 0
        
        # Movement speed
        self.speed = 1

        # Be eaten or not
        self.be_eaten = False

    def get_id(self):
        return self.id

    def get_px_x(self):
        return self.px_x
        
    def get_px_y(self):
        return self.px_y

    def set_position(self, idx_x, idx_y):
        self.idx_x = idx_x
        self.idx_y = idx_y
        self.px_x = self.idx_x * X // 34 + dJ - X // 100
        self.px_y = self.idx_y * X // 34 + dI - X // 100
        self.update_ghosts_position()

    def get_idx_x(self):
        return self.idx_x
        
    def get_idx_y(self):
        return self.idx_y
    
    def is_wall(self, cell_value):
        # Define which values represent walls in your board
        return cell_value in [3, 4, 5, 6, 7, 8]
    
    def is_eaten(self):
        return self.be_eaten

    def increase_speed(self): self.speed += 0.5
    def decrease_speed(self): self.speed -= 0.5

    def make_revive(self):
        self.be_eaten = False
        self.speed = 1.5
    
    def make_dead(self):
        self.be_eaten = True
        self.speed = 3


    def draw(self, screen, ghost_image):
        """
        Draw the ghost on the screen
        """
        screen.blit(ghost_image, (self.px_x, self.px_y))

    def update_ghosts_position(self):
        Ghosts_position[self.id][0] = self.idx_x
        Ghosts_position[self.id][1] = self.idx_y

    def check_collusion_other_ghosts(self, Ghosts_position, new_idx_x, new_idx_y):
        for i in range(4):
            if(i != self.id and Ghosts_position[i][0] == new_idx_x and Ghosts_position[i][1] == new_idx_y): 
                return True
        return False

    def index_to_px(self):
        px_x = self.idx_x * X // 34 + dJ - X // 100
        px_y = self.idx_y * X // 34 + dI - X // 100
        return px_x, px_y
    def update_index(self):
        # Approximate the index
        if self.direction == 1:
            self.idx_x = math.ceil(((self.px_x - dJ + X // 100) * 34) / X)
        elif self.direction == 2:
            self.idx_y = math.ceil(((self.px_y - dI + X // 100) * 34) / X)
        elif self.direction == 3:
            self.idx_y = math.floor(((self.px_y - dI + X // 100) * 34) / X)
        elif self.direction == 0:
            self.idx_x = math.floor(((self.px_x - dJ + X // 100) * 34) / X)
        # Update the ghosts position array 
        self.update_ghosts_position()
    
    def move(self, board, pacman_x, pacman_y):
        # Find the path to Pac-Man
        path = self.find_path(board, pacman_x, pacman_y)
    
        px_x, px_y = self.index_to_px()

        # If there's a path and at least one step to take
        if path and len(path) > 0:
            # Get the first step's direction
            self.direction = path[0]
            # self.prev_direction = self.direction
        
            # Move based on direction
            if self.direction == 0:  # RIGHT
                self.px_x += self.speed
                self.px_y = px_y
            elif self.direction == 1:  # LEFT
                self.px_x -= self.speed
                self.px_y = px_y
            elif self.direction == 2:  # UP
                self.px_y -= self.speed
                self.px_x = px_x
            elif self.direction == 3:  # DOWN
                self.px_y += self.speed
                self.px_x = px_x
            
            # Update grid indices based on pixel position
            # self.idx_x = math.ceil(((self.px_x - dJ + X // 100) * 34) / X)
            # self.idx_y = math.ceil(((self.px_y - dI + X // 100) * 34) / X)
            self.update_index()
            #self.idx_x = (self.px_x + (612 // 100)) // (612 // 34)
            #self.idx_y = (self.px_y + (612 // 100)) // (612 // 34)
    

class BlueGhost(Ghost):
    # BFS
    def find_path(self, board, pacman_x, pacman_y):
        """
        Find the shortest path to Pac-Man using BFS algorithm
        Returns a list of directions to follow
        """
        # Queue for BFS, contains: (x, y, path)
        queue = [(self.idx_x, self.idx_y, [])]
        # Keep track of visited cells to avoid loops
        visited = set([(self.idx_x, self.idx_y)])
        
        # Possible movement directions: right, left, up, down
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        direction_values = [0, 1, 2, 3]  # Corresponding to direction constants
        
        while queue:
            x, y, path = queue.pop(0)
            
            # Check if we've reached Pac-Man
            if x == pacman_x and y == pacman_y:
                return path
            
            # Explore all four directions
            for i, (dx, dy) in enumerate(directions):
                new_x, new_y = x + dx, y + dy
                
                # Check if the new position is valid:
                # - Within board boundaries
                # - Not a wall
                # - Not previously visited
                # - Not collusion with other ghosts
                if (0 <= new_x < len(board[0]) and 
                    0 <= new_y < len(board) and 
                    not self.is_wall(board[new_y][new_x]) and
                    not self.check_collusion_other_ghosts(Ghosts_position, new_x, new_y) and
                    (new_x, new_y) not in visited):
                    
                    # Add direction to the path
                    new_path = path + [direction_values[i]]
                    queue.append((new_x, new_y, new_path))
                    visited.add((new_x, new_y))
        
        # If no path is found (should not happen in a valid Pac-Man maze)
        return []

class PinkGhost(Ghost):

    global dfs_visited
    # def is_stuck(self, board):
    #     directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    #     direction_values = [0, 1, 2, 3]  # Corresponding to direction constants
    #     for i, (dx, dy) in enumerate(directions):
    #         if ((self.idx_x + dx, self.idx_y + dy) not in dfs_visited and
    #             not self.is_wall(board[self.idx_y  + dy][self.idx_x + dx])):
    #             return False
    #     return True
    
    def handle_stuck(self, board):
        if (self.direction == 1 or self.direction == 0):
            next_idx_x = math.ceil(((self.px_x - dJ + X // 100) * 34) / X)
            prev_idx_x = math.floor(((self.px_x - dJ + X // 100) * 34) / X)
            if next_idx_x == prev_idx_x: return 
            if ((prev_idx_x, self.idx_y) in dfs_visited and
                (next_idx_x, self.idx_y) in dfs_visited and
                not self.is_wall(board[self.idx_y][prev_idx_x]) and
                not self.is_wall(board[self.idx_y][next_idx_x])):

                dfs_visited.remove((prev_idx_x, self.idx_y))
                dfs_visited.remove((next_idx_x, self.idx_y))
        else:
            next_idx_y = math.ceil(((self.px_y - dI + X // 100) * 34) / X)
            prev_idx_y = math.floor(((self.px_y - dI + X // 100) * 34) / X)
            if next_idx_y == prev_idx_y: return 
            if ((self.idx_x, next_idx_y) in dfs_visited and
                (self.idx_x, prev_idx_y) in dfs_visited and
                not self.is_wall(board[prev_idx_y][self.idx_x]) and
                not self.is_wall(board[next_idx_y][self.idx_x])):

                dfs_visited.remove((self.idx_x, prev_idx_y))
                dfs_visited.remove((self.idx_x, next_idx_y))


    # DFS
    def find_path(self, board, pacman_x, pacman_y):
        """
        Find a path to Pac-Man using DFS algorithm
        Returns a list of directions to follow
        """
        # Stack for DFS, contains: (x, y, path)
        stack = [(self.idx_x, self.idx_y, [])]
        # Keep track of visited cells to avoid loops
        visited = set()
        
        # Possible movement directions: right, left, up, down
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        direction_values = [0, 1, 2, 3]  # Corresponding to direction constants
        
        while stack:
            x, y, path = stack.pop()
            visited.add((x, y))
            
            # Check if we've reached Pac-Man
            if x == pacman_x and y == pacman_y:
                return path
            
            
            direction_values, directions = sort_manhattan_distance(x, y, pacman_x, pacman_y)
            # Explore all four directions
            for i, (dx, dy) in enumerate(directions):
                new_x, new_y = x + dx, y + dy
                
                # Check if the new position is valid:
                # - Within board boundaries
                # - Not a wall
                # - Not previously visited
                # - Not collusion with other ghosts
                if (0 <= new_x < len(board[0]) and 
                    0 <= new_y < len(board) and 
                    not self.is_wall(board[new_y][new_x]) and
                    not self.check_collusion_other_ghosts(Ghosts_position, new_x, new_y) and
                    (new_x, new_y) not in dfs_visited and
                    (new_x, new_y) not in visited):
                    

                    # Add direction to the path
                    new_path = path + [direction_values[i]]
                    stack.append((new_x, new_y, new_path))
        
        # If no path is found (should not happen in a valid Pac-Man maze)
        return []
    
    def move(self, board, pacman_x, pacman_y):
        # Find the path to Pac-Man
        path = self.find_path(board, pacman_x, pacman_y)
        if not path:
                dfs_visited.clear()

        px_x, px_y = self.index_to_px()

        # If there's a path and at least one step to take
        if path and len(path) > 0:
            # Get the first step's direction
            self.direction = path[0]
            # self.prev_direction = self.direction
        
            # Move based on direction
            if self.direction == 0:  # RIGHT
                self.px_x += self.speed
                self.px_y = px_y
            elif self.direction == 1:  # LEFT
                self.px_x -= self.speed
                self.px_y = px_y
            elif self.direction == 2:  # UP
                self.px_y -= self.speed
                self.px_x = px_x
            elif self.direction == 3:  # DOWN
                self.px_y += self.speed
                self.px_x = px_x
            
            # Update grid indices based on pixel position
            # self.idx_x = math.ceil(((self.px_x - dJ + X // 100) * 34) / X)
            # self.idx_y = math.ceil(((self.px_y - dI + X // 100) * 34) / X)
            self.update_index()
            #self.idx_x = (self.px_x + (612 // 100)) // (612 // 34)
            #self.idx_y = (self.px_y + (612 // 100)) // (612 // 34)
            # print("Ghost: ", self.idx_x, self.idx_y)
            # print("Ghost: ", ((self.px_x - dJ + X // 100) * 34) / X, ((self.px_y - dI + X // 100) * 34) / X)
            # print("DFS_vistied: ", dfs_visited)
            # Check stuck, if 4 position of ghost has been in global visited
            # -> Clear global visited make it not stand in one place
            # self.is_stuck(board)
            # Save global visited for dfs to prevent it from go again the same place
            if (self.idx_x, self.idx_y) not in dfs_visited:
                if len(dfs_visited) < 5:
                    dfs_visited.append((self.idx_x, self.idx_y))
                else:
                    dfs_visited.pop(0)
                    dfs_visited.append((self.idx_x, self.idx_y))
            # Check stuck, if 4 position of ghost has been in global visited
            # -> Clear global visited make it not stand in one place
            self.handle_stuck(board)


    # DFS Backtracking
    # def find_path(self, board, pacman_x, pacman_y):
    #     """
    #     Find the path to Pac-Man using DFS with backtracking.
    #     Returns a list of directions to follow.
    #     """
    #     # Set to track visited positions
    #     visited = set()
    #     # Possible movement directions: right, left, up, down
    #     directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    #     direction_values = [0, 1, 2, 3]  # Corresponding to direction constants
        
    #     def dfs(x, y, path):
    #         # If reached Pac-Man, return the path
    #         if x == pacman_x and y == pacman_y:
    #             return path
            
    #         visited.add((x, y))
            
    #         for i, (dx, dy) in enumerate(directions):
    #             new_x, new_y = x + dx, y + dy
                
    #             if (0 <= new_x < len(board[0]) and 
    #                 0 <= new_y < len(board) and 
    #                 not self.is_wall(board[new_y][new_x]) and
    #                 not self.check_collusion_other_ghosts(Ghosts_position, new_x, new_y) and
    #                 (new_x, new_y) not in visited):
                    
    #                 result = dfs(new_x, new_y, path + [direction_values[i]])
    #                 if result:
    #                     return result  # Stop as soon as we find a valid path
                    
    #         visited.remove((x, y))  # Backtrack if no path found from this position
    #         return None
        
    #     # Start DFS from ghost's initial position
    #     return dfs(self.idx_x, self.idx_y, []) or []
    
    #IDS
    # def find_path(self, board, pacman_x, pacman_y):
    #     """
    #     Find a path to Pac-Man using IDS algorithm
    #     Returns a list of directions to follow
    #     """
    #     # Possible movement directions: right, left, up, down
    #     directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    #     direction_values = [0, 1, 2, 3]  # Corresponding to direction constants
        
    #     def depth_limited_search(x, y, depth, path, visited):
    #         if x == pacman_x and y == pacman_y:
    #             return path
            
    #         if depth == 0:
    #             return None
            
            
    #         for i, (dx, dy) in enumerate(directions):
    #             new_x, new_y = x + dx, y + dy
                
    #             if (0 <= new_x < len(board[0]) and 
    #                 0 <= new_y < len(board) and 
    #                 not self.is_wall(board[new_y][new_x]) and
    #                 not self.check_collusion_other_ghosts(Ghosts_position, new_x, new_y) and
    #                 (new_x, new_y) not in visited):
                    
    #                 new_path = path + [direction_values[i]]
    #                 visited.add((new_x, new_y))
    #                 result = depth_limited_search(new_x, new_y, depth - 1, new_path, visited)
    #                 if result is not None:
    #                     return result
    #                 visited.remove((new_x, new_y))
            
    #         return None
    #     depth = 200
    #     while depth <= 200:
    #         visited = set([(self.idx_x, self.idx_y)])
    #         result = depth_limited_search(self.idx_x, self.idx_y, depth, [], visited)
    #         if result is not None:
    #             return result
    #         depth += 1
    #     return []

class OrangeGhost(Ghost):
    # UCS
    def find_path(self, board, pacman_x, pacman_y):
        """
        Find the shortest path to Pac-Man using UCS algorithm
        Returns a list of directions to follow
        """
        # Priority queue for UCS, contains: (cost, x, y, path)
        pq = [(0, self.idx_x, self.idx_y, [])]
        # Keep track of visited cells with their cost
        visited = {}
        visited[(self.idx_x, self.idx_y)] = 0
        
        # Possible movement directions: right, left, up, down
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        direction_values = [0, 1, 2, 3]  # Corresponding to direction constants
        
        while pq:
            cost, x, y, path = heapq.heappop(pq)  # Expand the lowest-cost node
            
            # Check if we've reached Pac-Man
            if x == pacman_x and y == pacman_y:
                return path
            
            # Explore all four directions
            for i, (dx, dy) in enumerate(directions):
                new_x, new_y = x + dx, y + dy
                new_cost = cost + 1  # Assume uniform cost of 1 per move
                
                # Check if the new position is valid:
                # - Within board boundaries
                # - Not a wall
                # - Not previously visited
                # - Not collusion with other ghosts
                if (0 <= new_x < len(board[0]) and 
                    0 <= new_y < len(board) and 
                    not self.check_collusion_other_ghosts(Ghosts_position, new_x, new_y) and
                    not self.is_wall(board[new_y][new_x])):
                    
                    # If new position is unvisited or found with a lower cost, add to queue
                    if (new_x, new_y) not in visited or new_cost < visited[(new_x, new_y)]:
                        visited[(new_x, new_y)] = new_cost
                        heapq.heappush(pq, (new_cost, new_x, new_y, path + [direction_values[i]]))
        
        # If no path is found
        return []

class RedGhost(Ghost):
    # A*
    def find_path(self, board, pacman_x, pacman_y):
        """
        Find the shortest path to Pac-Man using A* algorithm with Manhattan distance heuristic.
        Returns a list of directions to follow.
        """
        # Priority queue for A*, contains: (f-cost, g-cost, x, y, path)
        pq = [(0, 0, self.idx_x, self.idx_y, [])]
        # Keep track of visited cells with their g-cost
        visited = {}
        visited[(self.idx_x, self.idx_y)] = 0

        # Possible movement directions: right, left, up, down
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        direction_values = [0, 1, 2, 3]  # Corresponding to direction constants

        def manhattan_distance(x1, y1, x2, y2):
            """Calculate Manhattan distance between two points."""
            return abs(x1 - x2) + abs(y1 - y2)

        while pq:
            _, g_cost, x, y, path = heapq.heappop(pq)  # Expand the lowest f-cost node

            # Check if we've reached Pac-Man
            if x == pacman_x and y == pacman_y:
                return path

            # Explore all four directions
            for i, (dx, dy) in enumerate(directions):
                new_x, new_y = x + dx, y + dy
                new_g_cost = g_cost + 1  # Uniform cost of 1 per move
                h_cost = manhattan_distance(new_x, new_y, pacman_x, pacman_y)
                f_cost = new_g_cost + h_cost  # f = g + h

                # Check if the new position is valid:
                # - Within board boundaries
                # - Not a wall
                # - Not previously visited
                # - Not collusion with other ghosts
                if (0 <= new_x < len(board[0]) and 
                    0 <= new_y < len(board) and 
                    not self.check_collusion_other_ghosts(Ghosts_position, new_x, new_y) and
                    not self.is_wall(board[new_y][new_x])):

                    # If new position is unvisited or found with a lower g-cost, add to queue
                    if (new_x, new_y) not in visited or new_g_cost < visited[(new_x, new_y)]:
                        visited[(new_x, new_y)] = new_g_cost
                        heapq.heappush(pq, (f_cost, new_g_cost, new_x, new_y, path + [direction_values[i]]))

        # If no path is found
        return []