# Snake.py
# By Amine Asli <amine.asli@aol.com>
# MIT License

import pygame
from pygame.locals import *
import random

FPS = 10
SCREEN_SIZE = (640, 480)
CELL_SIZE = 20
COLS = SCREEN_SIZE[0] / CELL_SIZE
ROWS = SCREEN_SIZE[1] / CELL_SIZE

# Set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)

# Setup directions
LEFT  = (-1, 0)
RIGHT = (1, 0)
UP    = (0, -1)
DOWN  = (0, 1)

class Snake:
    def __init__(self, cols, rows, cell_size=20, direction=(1, 0), color=(255, 255, 255), size=3):
        self.cols = cols
        self.rows = rows
        self.start_x = int(self.cols//2)
        self.start_y = int(self.rows//2)
        self.cell_size = cell_size
        self.direction = direction
        self.color = color
        self.segments = []
        self.build_segments(size)

    def build_segments(self, size):
        # Set a list of segments coordinates
        for i in range(1, size+1):
            self.segments.append([(self.start_x - i) * self.cell_size, self.start_y * self.cell_size])

    def add_segment(self):
        x, y = self.direction
        tail = self.segments[-1]
        self.segments.append([tail[0] + x * self.cell_size, tail[1] + y * self.cell_size])

    def check_edge_collision(self):
        # Check if the Snake has hit the edges
        head = self.segments[0]
        if head[0] < 0 \
            or head[0] == self.cols * self.cell_size  \
            or head[1] < 0 \
            or head[1] == self.rows * self.cell_size: \
                return True
        return False
    
    def check_segment_collision(self):
        # Check if the Snake has hit itself 
        head = self.segments[0]
        for segment in self.segments[1:]:
            if head[0] == segment[0] and head[1] == segment[1]:
                return True
        return False
    
    def check_collisions(self):
        if self.check_edge_collision() or self.check_segment_collision():
            return True
        return False

    def collide(self, food):
        # Check if the Snake collided with the Food
        x = food.x
        y = food.y
        head = self.segments[0]
        if head[0] == x and head[1] == y:
            return True
        return False

    def update(self):
        x, y = self.direction
        head = self.segments[0]
        # Remove Snake's tail segment
        self.segments.pop()
        # Insert a new head segment
        self.segments.insert(0, [head[0] + x * self.cell_size, head[1] + y * self.cell_size])
    
    def render(self, surface):
        for segment in self.segments:
            segment_surface = pygame.Rect(segment[0], segment[1], self.cell_size, self.cell_size)
            pygame.draw.rect(surface, self.color, segment_surface)


class Food:
    def __init__(self, cols, rows, cell_size=20, color=(255, 255, 255)):
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.color = color
        self.x = 0
        self.y = 0

    def set_random_location(self):
        self.x = random.randint(0, (self.cols - 1)) * self.cell_size
        self.y = random.randint(0, (self.rows - 1)) * self.cell_size

    def render(self, surface):
        food_surface = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
        pygame.draw.rect(surface, self.color, food_surface)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    clock = pygame.time.Clock()
    # Create the Snake object. Only the two first arguments are mandatory
    snake = Snake(COLS, ROWS, CELL_SIZE, RIGHT, GREEN)
    # Create the Food object and set it's initial location. Only the two first arguments are mandatory
    food = Food(COLS, ROWS, CELL_SIZE, RED)
    food.set_random_location()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                elif event.key == K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == K_DOWN and snake.direction != UP:
                    snake.direction = DOWN

        screen.fill(BLACK)
        snake.update()
        # Check if the Snake has hit itself or the edge 
        if snake.check_collisions():
            break;
        # Check if the Snake has eaten the Food
        if snake.collide(food):
            snake.add_segment()
            food.set_random_location()
            score += 1
        
        
        food.render(screen)
        snake.render(screen)
        pygame.display.update()
        clock.tick(FPS)

    print("Your score:", score)
    pygame.quit()
    quit() 

if __name__ == "__main__":
    main()