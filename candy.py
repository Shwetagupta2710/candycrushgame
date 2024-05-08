import pygame
import random

# initializing the game
pygame.init()

# constraints
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE

# colors
WHITE = (255, 255, 255)

# initializing the game screen 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Crush")

# create a grid of candies
grid = [[random.randint(1, 3) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

selected_candy = None

def handle_click(row, col):
    global selected_candy
    if selected_candy is None:
        selected_candy = (row, col)
    else:
        # swap the candies
        row1, col1 = selected_candy
        grid[row][col], grid[row1][col1] = grid[row1][col1], grid[row][col] 
        selected_candy = None

def detect_matches():
    matches = set()

    # horizontal matches
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2]:
                matches.add((row, col))
                matches.add((row, col + 1))
                matches.add((row, col + 2))

    # vertical matches
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col]:
                matches.add((row, col))
                matches.add((row + 1, col))
                matches.add((row + 2, col))

    return matches

def fill_empty_spaces():
    # Shift candies down
    for col in range(GRID_SIZE):
        empty_count = 0
        # count and remove empty spaces
        for row in range(GRID_SIZE - 1, -1, -1):
            if grid[row][col] == 0:
                empty_count += 1
            elif empty_count > 0:
                # shift candy down
                grid[row + empty_count][col] = grid[row][col]
                grid[row][col] = 0
    # Add new candies to the top
    for col in range(GRID_SIZE):
        for row in range(empty_count):
            grid[row][col] = random.randint(1, 3)

# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            col = event.pos[0] // CELL_SIZE
            row = event.pos[1] // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                handle_click(row, col)

    # Detect and remove matches
    matches = detect_matches()
    if matches:
        for row, col in matches:
            grid[row][col] = 0

    # Fill empty spaces after removing matches
    fill_empty_spaces()

    # Draw the candies
    screen.fill(WHITE)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            candy_type = grid[row][col]
            candy_color = (255, 0, 0) if candy_type == 1 else (0, 255, 0) if candy_type == 2 else (0, 0, 255)
            pygame.draw.rect(screen, candy_color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.delay(100)

pygame.quit()
