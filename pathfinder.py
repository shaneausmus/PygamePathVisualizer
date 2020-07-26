
try:
    import pygame
    from button_pygame import *
    from time import sleep
    from queue import Queue
    from math import sqrt, pow      
except:
    import install_req_libraries

    import pygame
    from button_pygame import *
    from time import sleep
    from queue import Queue
    import math

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (105,105,105)
D_GREEN = (34,139,34)
GREEN = (0, 255, 0)
RED = (220,20,60)
BLUE = (65,105,225)

HEIGHT = 24
WIDTH = 24
MARGIN = 4

window = pygame.display.set_mode((680, 800))
pygame.display.set_caption("Sorting Visualizer")
clock = pygame.time.Clock()

rows, cols = (24, 24)

def make_grid():
    global GRID
    GRID = [[[pygame.Rect((MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, 
                            WIDTH, HEIGHT), WHITE] for row in range(rows)] for col in range(cols)]

def draw_grid():
    global GRID
    for row in GRID:
        for item in row:
            rect, color = item[0], item[1]
            pygame.draw.rect(window, color, rect)

def is_green_and_red():
    global GRID
    check_green_and_red = [False, False]
    for row in GRID:
        for col in row:
            if col[1] is RED:
                check_green_and_red[0] = True
            elif col[1] is GREEN:
                check_green_and_red[1] = True
    return check_green_and_red

def clear_board():
    global GRID
    for row in GRID:
        for col in row:
            col[1] = WHITE

def set_obstacles(click):
    global GRID
    for row in GRID:
        for col in row:
            rect, color = col
            if rect.collidepoint(click):
                check_red, check_green = is_green_and_red()
                if check_red and check_green:
                    if color is GREY or color is GREEN or color is RED:
                        col[1] = WHITE
                    elif color is WHITE:
                        col[1] = GREY
                elif check_red:
                    if color is GREY:
                        col[1] = GREEN
                    elif color is RED:
                        col[1] = WHITE
                    else:
                        col[1] = GREY
                elif check_green:
                    if color is GREY or color is GREEN:
                        col[1] = RED
                    else:
                        col[1] = GREY
                else:
                    if color is GREY:
                        col[1] = GREEN
                    elif color is GREEN:
                        col[1] = RED
                    elif color is RED:
                        col[1] = WHITE
                    else:
                        col[1] = GREY

def get_green():
    for i in range(0, len(GRID)):
        for j in range(0, len(GRID[i])):
            if GRID[i][j][1] == GREEN:
                return (i, j)

def get_red():
    for i in range(0, len(GRID)):
        for j in range(0, len(GRID[i])):
            if GRID[i][j][1] == RED:
                return (i, j)
            

def is_in_open_rects(rect, open_rects):
    for i in range(0, len(open_rects)):
        if open_rects[i] is rect:
                return True
    return False

def initialize_a_star():
    # getting x and y coords for the green square and calculating each node's
    # initial A* value
    x2, y2 = get_green()
    x1, y1 = get_red()
    for row in range(0, len(GRID)):
        for col in range(0, len(GRID[row])):
            # I specify each letter just to make clear what means what
            g = round(10 * sqrt(pow(x1 - row, 2) + pow(y1 - col, 2)))
            h = round(10 * sqrt(pow(x2 - row, 2) + pow(y2 - col, 2)))
            f = g + h 
            GRID[row][col].append([g, h, f])

def get_lowest(open_rects):
    min = open_rects[0]
    for i in range(0, len(open_rects)):
        if open_rects[i][2][2] < min[2][2]:
            min = open_rects[i]
    return min

def get_heuristic(coords):
    x1, y1 = coords
    x2, y2 = get_green()
    return round(10 * sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2)))

def clean_a_star():
    for i in range(0, len(GRID)):
        for j in range(0, len(GRID[i])):
            GRID[i][j].pop()

def run_dfs():
    check_red, check_green = is_green_and_red()
    if not (check_red and check_green):
        print("The start and/or end points haven't been set!")
    else:
        start_rect = prev_rect = None
        done = False
        row = col = 0
        neighbors = []
        visited_neighbors = dict()
        for row in GRID:
            for col in row:
                if col[1] is RED:
                    start_rect = prev_rect = col
        neighbors.append(start_rect)
        while len(neighbors) != 0 and not done:
            current_rect = neighbors[len(neighbors) - 1]
            neighbors.pop()
            count = list(visited_neighbors.keys()).count(current_rect)
            if count == 0:
                if current_rect[1] is GREEN:
                    done = True
                elif current_rect[1] is RED or current_rect[1] is D_GREEN:
                    pass
                elif current_rect[1] is WHITE:
                    current_rect[1] = D_GREEN

                for i in range(0, len(GRID)):
                    for j in range(0, len(GRID[i])):
                        if GRID[i][j] == current_rect:
                            row = i
                            col = j

                curr_rect_loc = (row, col)
                visited_neighbors.update({curr_rect_loc: prev_rect})

                for x, y in (
                    (row - 1, col - 1), (row + 1, col - 1),
                    (row - 1, col + 1), (row + 1, col + 1),
                    (row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1) ):
                    if not (0 <= x < len(GRID) and 0 <= y < len(GRID[x]) and GRID[x][y][1] is not GREY and GRID[x][y][1] is not D_GREEN and GRID[x][y][1] is not RED):
                        continue
                    neighbors.append(GRID[x][y])

                prev_rect = (row, col)
                draw_grid()
                pygame.display.flip()
                sleep(0.1)
        
        row, col = get_green()

        while GRID[row][col] != start_rect:
            GRID[row][col][1] = GREEN
            pair = visited_neighbors.get((row, col))
            row, col = pair
            draw_grid()
            pygame.display.flip()

# any element starting with 1 relates to the starting red square
# any element starting with 2 interfaces with the ending green square
def run_bidirectional():
    check_red, check_green = is_green_and_red()
    if not check_red or not check_green:
        print("The start and/or end points haven't been set!")
    else:
        done = False
        prev_rect1 = prev_rect2 = None
        row1 = row2 = col1 = col2 = 0
        neighbors1 = Queue(maxsize=-1)
        neighbors2 = Queue(maxsize=-1)
        visited_neighbors = dict()
        x_red, y_red = get_red()
        curr_rect_loc1 = (x_red, y_red)
        x_green, y_green = get_green()
        curr_rect_loc2 = (x_green, y_green)
        prev_distance1 = prev_distance2 = 10*sqrt(pow(x_red - x_green, 2) + pow(y_red - y_green, 2))

        for row in GRID:
            for col in row:
                if col[1] is RED:
                    prev_rect1 = col
                    neighbors1.put(prev_rect1)
                elif col[1] is GREEN:
                    prev_rect2 = col
                    neighbors2.put(prev_rect2)

        while not neighbors1.empty() and not neighbors2.empty() and not done:
            current_rect1 = neighbors1.get()
            current_rect2 = neighbors2.get()
            
            for i in range(0, len(GRID)):
                for j in range(0, len(GRID[i])):
                    if GRID[i][j] == current_rect1:
                        row1 = i
                        col1 = j
                        prev_rect1 = (row1, col1)
                    elif GRID[i][j] == current_rect2:
                        row2 = i
                        col2 = j
                        prev_rect2 = (row2, col2)

            for x, y in ((row1, col1 - 1), (row1 + 1, col1), (row1, col1 + 1), (row1 - 1, col1)):
                if not (0 <= x < len(GRID) and 0 <= y < len(GRID[x]) and GRID[x][y][1] is not GREY and GRID[x][y][1] is not RED):
                    continue
                else:
                    if GRID[x][y][1] is WHITE:
                        GRID[x][y][1] = D_GREEN
                        draw_grid()
                        pygame.display.flip()
                    elif GRID[x][y][1] is RED:
                        pass
                    elif GRID[x][y][1] is BLUE:
                        done = True
                        break
                    if prev_distance1 > 10*sqrt(pow(curr_rect_loc2[0] - x, 2) + pow(curr_rect_loc2[1] - y, 2)):
                        curr_rect_loc1 = (x, y)
                        prev_distance1 = 10*sqrt(pow(curr_rect_loc2[0] - x, 2) + pow(curr_rect_loc2[1]- y, 2))
                        visited_neighbors.update({curr_rect_loc1: prev_rect1})
            
            neighbors1.put(GRID[curr_rect_loc1[0]][curr_rect_loc1[1]])

            for x, y in ((row2, col2 - 1), (row2 + 1, col2), (row2, col2 + 1), (row2 - 1, col2)):
                if not (0 <= x < len(GRID) and 0 <= y < len(GRID[x]) and GRID[x][y][1] is not GREY and GRID[x][y][1] is not GREEN):
                    continue
                else:
                    if GRID[x][y][1] is WHITE:
                        GRID[x][y][1] = BLUE
                        draw_grid()
                        pygame.display.flip()
                    elif GRID[x][y][1] is GREEN:
                        pass
                    elif GRID[x][y][1] is D_GREEN:
                        done = True
                        break
                    if prev_distance2 > 10*sqrt(pow(curr_rect_loc1[0] - x, 2) + pow(curr_rect_loc1[1] - y, 2)):
                        curr_rect_loc2 = (x, y) 
                        prev_distance2 = 10*sqrt(pow(curr_rect_loc1[0]- x, 2) + pow(curr_rect_loc1[1] - y, 2))
                        visited_neighbors.update({curr_rect_loc2: prev_rect2})
            
            neighbors2.put(GRID[curr_rect_loc2[0]][curr_rect_loc2[1]])

        for i in range(0, len(GRID)):
            for j in range(0, len(GRID[i])):
                if (i, j) == curr_rect_loc1:
                    row1 = i
                    col1 = j
                if (i, j) == curr_rect_loc2:
                    row2 = i
                    col2 = j

        while GRID[row1][col1] != None:
            GRID[row1][col1][1] = BLACK
            draw_grid()
            pygame.display.flip()
            pair1 = visited_neighbors.get((row1, col1))
            if pair1 == None:
                break
            row1, col1 = pair1

        while GRID[row2][col2] != None:
            GRID[row2][col2][1] = BLACK
            draw_grid()
            pygame.display.flip()
            pair2 = visited_neighbors.get((row2, col2))
            if pair2 == None:
                break
            row2, col2 = pair2


def run_bfs():
    check_red, check_green = is_green_and_red()
    if not check_red or not check_green:
        print("The start and/or end points haven't been set!")
    else:
        start_rect = prev_rect = None
        done = False
        row = col = 0
        neighbors = Queue(maxsize=-1)
        visited_neighbors = dict()
        for row in GRID:
            for col in row:
                if col[1] is RED:
                    start_rect = prev_rect = col
        neighbors.put(start_rect)
        while not neighbors.empty() and not done:
            current_rect = neighbors.get()
            
            for i in range(0, len(GRID)):
                for j in range(0, len(GRID[i])):
                    if GRID[i][j] == current_rect:
                        row = i
                        col = j
                        prev_rect = (row, col)

            for x, y in (
                (row, col - 1), (row + 1, col), (row, col + 1), (row - 1, col)):
                if not (0 <= x < len(GRID) and 0 <= y < len(GRID[x]) and GRID[x][y][1] is not GREY and GRID[x][y][1] is not D_GREEN and GRID[x][y][1] is not RED):
                    continue
                else:
                    if GRID[row][col][1] is WHITE:
                        GRID[row][col][1] = D_GREEN
                    elif GRID[row][col][1] is RED or GRID[row][col][1] is D_GREEN:
                        pass
                    elif GRID[row][col][1] is GREEN:
                        done = True
                    neighbors.put(GRID[x][y])
                    curr_rect_loc = (x,y)
                    visited_neighbors.update({curr_rect_loc: prev_rect})
            
            draw_grid()
            pygame.display.flip()
        
        row, col = get_green()

        while GRID[row][col] != start_rect:
            GRID[row][col][1] = GREEN
            pair = visited_neighbors.get((row, col))
            row, col = pair
            draw_grid()
            pygame.display.flip()

def run_a_star():
    check_red, check_green = is_green_and_red()
    if not check_red or not check_green:
        print("The start and/or end points haven't been set!")
    else:
        initialize_a_star()
        start_rect = curr_rect = final_rect = None
        open_rects = []
        visited_neighbors = dict()
        for row in GRID:
            for col in row:
                if col[1] is RED:
                    start_rect = col
                elif col[1] is GREEN:
                    final_rect = col
        open_rects.append(start_rect)
        while (curr_rect != final_rect):
            curr_rect = get_lowest(open_rects)
            if curr_rect[1] is GREEN:
                break
            else:
                for i in range(0, len(GRID)):
                    for j in range(0, len(GRID[i])):
                        if GRID[i][j] == curr_rect:
                            row = i
                            col = j
                            break

                curr_rect_loc = (row, col)
                prev_rect_loc = visited_neighbors.get((row, col))
                if curr_rect != start_rect:
                    curr_rect[1] = D_GREEN
                    curr_rect[2][0] = GRID[prev_rect_loc[0]][prev_rect_loc[1]][2][0] + round(10 * sqrt(pow(prev_rect_loc[0] - row, 2) + pow(prev_rect_loc[1] - col, 2)))
                    curr_rect[2][1] = get_heuristic((row, col))
                    curr_rect[2][2] = curr_rect[2][0] + curr_rect[2][1]
                    draw_grid()
                    pygame.display.flip()

                open_rects.remove(curr_rect)
                for x, y in (
                (row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)):
                    if not (0 <= x < len(GRID) and 0 <= y < len(GRID[x]) and GRID[x][y][1] is not GREY and GRID[x][y][1] is not D_GREEN and GRID[x][y][1] is not RED):
                        continue
                    else:
                        in_open_rects = is_in_open_rects(GRID[x][y], open_rects)
                        if (GRID[x][y][2][0] < curr_rect[2][0] and GRID[x][y][1] is D_GREEN):
                            visited_neighbors.update({(x, y): (row, col)})
                        elif GRID[x][y][2][0] > curr_rect[2][0] and in_open_rects:
                            GRID[x][y][2][0] = curr_rect[2][0] + round(10 * sqrt(pow(x - row, 2) + pow(y - col, 2)))
                            visited_neighbors[(x, y)] = (row, col)
                        elif (GRID[x][y][1] is not D_GREEN and not in_open_rects):
                            GRID[x][y][2][0] = curr_rect[2][0] + round(10 * sqrt(pow(x - row, 2) + pow(y - col, 2)))
                            open_rects.append(GRID[x][y])
                            visited_neighbors.update({(x, y): (row, col)})
                        draw_grid()
                        pygame.display.flip()


    row, col = get_green()

    while GRID[row][col] != start_rect:
        GRID[row][col][1] = GREEN
        pair = visited_neighbors.get((row, col))
        row, col = pair
        draw_grid()
        pygame.display.flip()

    clean_a_star()


make_grid()
CHECK_QUIT = True

bfs = button_pygame(GREEN, 30, 700, 100, 80, "Breadth-first")
dfs = button_pygame(GREEN, 160, 700, 100, 80, "Depth-first")
bidirectional = button_pygame(GREEN, 290, 700, 100, 80, "Bidirectional")
a_star = button_pygame(GREEN, 420, 700, 100, 80, "A*")
clear = button_pygame(GREEN, 550, 700, 100, 80, "Clear Board")
btn_list = [bfs, dfs, bidirectional, a_star, clear]

while CHECK_QUIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            CHECK_QUIT = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                CHECK_QUIT = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bfs.rect.collidepoint(pygame.mouse.get_pos()):
                run_bfs()
            elif dfs.rect.collidepoint(pygame.mouse.get_pos()):
                run_dfs()
            elif bidirectional.rect.collidepoint(pygame.mouse.get_pos()):
                run_bidirectional()
            elif a_star.rect.collidepoint(pygame.mouse.get_pos()):
                run_a_star()
            elif clear.rect.collidepoint(pygame.mouse.get_pos()):
                clear_board()
            else:
                set_obstacles(pygame.mouse.get_pos())

    window.fill(BLACK)

    draw_grid()

    for btn in btn_list:
        btn.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
