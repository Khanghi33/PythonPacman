import math
import config
import heapq
import time
import tracemalloc
import random

X = config.X
dJ = config.dJ
dI = config.dI

total_run_time = 0
total_memory = 0
total_peak_memory = 0
count = 0
expanded_nodes = 0
# Storing position of 4 ghost in the same time
Ghosts_position = [[0, 0], [0, 0], [0, 0], [0, 0]]

dfs_visited = [()]
def sort_manhattan_distance(ghost_x, ghost_y, pacman_x, pacman_y): 
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    direction_values = [0, 1, 2, 3]  # Corresponding to direction constants

    # Calculate Manhattan
    possible_moves = []
    for i, (dx, dy) in enumerate(directions):
        new_x, new_y = ghost_x + dx, ghost_y + dy
        distance = abs(new_x - pacman_x) + abs(new_y - pacman_y)
        possible_moves.append((distance, direction_values[i], (dx, dy)))

    # Sort direction base on Manhattan
    possible_moves.sort(key=lambda x: (-x[0], -x[1]))

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
        self.speed = config.ghost_speed

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
        self.speed = config.ghost_speed
    
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
        # Start time trace
        start_time = time.perf_counter()
        # Start memory trace
        tracemalloc.start()
        # Find the path to Pac-Man
        path = self.find_path(board, pacman_x, pacman_y)
        # Store traced time and memory
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.perf_counter() - start_time
        global total_memory
        global total_peak_memory
        global total_run_time
        global count
        total_run_time += end_time
        total_memory += current
        total_peak_memory += peak
        count += 1
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
            self.update_index()

    

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
            global expanded_nodes
            expanded_nodes += 1 # Increse expanded node count
            
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
            # Increase expanded node count
            global expanded_nodes
            expanded_nodes += 1
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
        # Start time trace
        start_time = time.perf_counter()
        # Start memory trace
        tracemalloc.start()
        # Find the path to Pac-Man
        path = self.find_path(board, pacman_x, pacman_y)
        # Store traced time and memory
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        end_time = time.perf_counter() - start_time
        global total_memory
        global total_peak_memory
        global total_run_time
        global count
        total_run_time += end_time
        total_memory += current
        total_peak_memory += peak
        count += 1

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
            
            # Update index base on px
            self.update_index()

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
            # Increase expanded node count
            global expanded_nodes
            expanded_nodes += 1
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
            # Increase expanded node count
            global expanded_nodes
            expanded_nodes += 1
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