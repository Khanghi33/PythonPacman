import pygame
import config

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình (scale theo WIDTH)
WIDTH = config.WIDTH
HEIGHT = config.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enter Your Name")

def write_file(name, score):
    file_name = "player.txt"
    """
    Write a list of names and scores to a file.
    
    file_name: The name of the file to save data (str).
    data: A list of tuples containing (Name, Score) (list of tuples).
    """
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"{name},{score}\n")

def check_already_name(name_check):
    file_name = "player.txt"
    data = []
    """
    Read the file and print names with scores.
    
    file_name: The name of the file to read (str).
    """
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            name, score = line.strip().split(",")
            if (name_check == name): return True
    return False

def read_file():
    file_name = "player.txt"
    data = []
    """
    Read the file and print names with scores.
    
    file_name: The name of the file to read (str).
    """
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            name, score = line.strip().split(",")
            data.append((name, int(float(score) // 1)))
    return data
