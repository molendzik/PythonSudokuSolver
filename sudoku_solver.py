import pygame
import threading

# delay between algorithm steps - only for presentation purposes (in ms)
base_delay = 1

# sudoku input
puzzle = [
    [0, 3, 0, 0, 1, 0, 0, 6, 0],
    [7, 5, 0, 0, 3, 0, 0, 4, 8],
    [0, 0, 6, 9, 8, 4, 3, 0, 0],
    [0, 0, 3, 0, 0, 0, 8, 0, 0],
    [9, 1, 2, 0, 0, 0, 6, 7, 4],
    [0, 0, 4, 0, 0, 0, 5, 0, 0],
    [0, 0, 1, 6, 7, 5, 2, 0, 0],
    [6, 8, 0, 0, 9, 0, 0, 1, 5],
    [0, 9, 0, 0, 4, 0, 0, 3, 0]]


# check for empty spaces
def empty_coordinates(sudoku):
    for x in range(len(sudoku)):
        for y in range(len(sudoku[x])):
            if sudoku[x][y] == 0:
                return (x, y)


# check if move is possible

def is_move_valid(sudoku, move, coordinates):
    row, column = coordinates

    # column
    for i in range(0, len(sudoku)):
        if move == sudoku[i][column]:
            # print("column rule broken")
            return False
    # row
    for i in range(0, len(sudoku)):
        if move == sudoku[row][i]:
            # print("row rule broken")
            return False

    # 3x3 square
    square_x = row // 3
    square_y = column // 3

    for i in range(square_x * 3, square_x * 3 + 3):
        for j in range(square_y * 3, square_y * 3 + 3):
            if sudoku[i][j] == move:
                # print("square rule broken")
                return False

    return True


# backtracking algorithm
def sudoku_solver(sudoku):
    empty = empty_coordinates(sudoku)
    if empty is not None:
        row, column = empty
    else:
        return True

    for move in range(1, 10):
        if is_move_valid(sudoku, move, [row, column]):
            sudoku[row][column] = move
            if sudoku_solver(sudoku):
                # update GUI
                draw(base_delay)
                return True
            else:
                sudoku[row][column] = 0

    draw(base_delay)
    return False


# pygame GUI

pygame.font.init()

WINDOW_WIDTH = 540
WINDOW_HEIGHT = 540
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku - press space to trigger algorithm")
FRAME_RATE_CAP = 60

SUDOKU_GRID = pygame.image.load("blank sudoku grid.png")
WINDOW.blit(SUDOKU_GRID, (0, 0))
FONT = pygame.font.SysFont("comicsansms", 30)


# draw every changeable thing in GUI
def draw(delay):
    iteration = 0
    for index, line in enumerate(puzzle):
        # if 0 in line:
        for i in range(9):
            if line[i] != 0:
                pygame.time.delay(delay)
                WINDOW.fill((255, 255, 255), (5 + i * 60, 5 + index * 60, 50, 50))
                textsurface = FONT.render(str(line[i]), True, (0, 0, 0))
                WINDOW.blit(textsurface, (20 + i * 60, 10 + index * 60))
            elif line[i] == 0:
                WINDOW.fill((255, 255, 255), (5 + i * 60, 5 + index * 60, 50, 50))
    pygame.display.update()


def main_loop():
    game_state = True
    clock = pygame.time.Clock()
    draw(0)

    while game_state:
        clock.tick(FRAME_RATE_CAP)

        # quitting and solving sudoku on space(key) press
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sudoku_solver(puzzle)
                    print("Solved!")


    pygame.quit()


main_loop()