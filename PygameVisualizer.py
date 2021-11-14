import random
import pygame
import numpy as np
from scipy.io import wavfile
from time import sleep
import sorting_algorithms, pathfinding_algorithms, spanning_tree_algorithms
from collections import defaultdict

# Number of elements for sorting
ELEMENTS = 100

# Sleep duration
SLEEP = 0.01

# Screen Size
WIDTH = 1000
HEIGHT = WIDTH
GAP = WIDTH // ELEMENTS

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
AQUA = (50, 80, 99)
DARK_AQUA = (50, 80, 110)
GREEN = (75, 150, 0)
GRAY = (169, 169, 169)
DIM_GRAY = (105, 105, 105)
PINK = (219, 112, 147)
DARK_PINK = (199, 21, 133)
YELLOW = (204, 204, 0)
AQUATIC_GREEN = (0, 255, 145)


class Weighted_Graph:
    def __init__(self):
        self.graph = defaultdict(dict)

    def addEdge(self, u, v, weight=1):
        self.graph[u][v] = weight


class Bar:
    def __init__(self, height, color, i):
        self.height = height
        self.color = color
        self.x = i * GAP
        self.y = 0
        self.width = GAP

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def set_height(self, h):
        self.height = h

    def set_color(self, c):
        self.color = c

    def get_height(self):
        return self.height

    def get_color(self):
        return self.color

    def __lt__(self, bar):
        return self.height


class Box:
    """Creates and update the boxs for pathfinding algorithms"""

    def __init__(self, x, y, width, height, value, weight=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE
        self.value = value
        self.weight = weight

    def draw_box(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def draw_bounds(self, event, boxs):
        flat_list = [item.color for row in boxs for item in row]

        # Left,Middle,Right Click Handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
                if event.button == 1:
                    if flat_list.count(GREEN) == 0:
                        self.color = GREEN

                    elif self.color == GREEN:
                        self.color = WHITE

                elif event.button == 3:
                    if flat_list.count(RED) == 0:
                        self.color = RED

                    elif self.color == RED:
                        self.color = WHITE


                elif event.button == 2:
                    if self.color == BLACK:
                        self.color = WHITE

                    else:
                        self.color = BLACK

        # Add weights to the graph
        elif event.type == pygame.KEYDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
                if event.key == 113:
                    if self.color == AQUATIC_GREEN:
                        self.color = WHITE
                        self.weight = 1

                    else:
                        self.color = AQUATIC_GREEN
                        self.weight = 5


class Button:

    def __init__(self, height, width, x, y, label, next_screen, alg=None):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = GRAY
        self.label = label
        self.font = pygame.font.Font('fonts/RobotoSlab-ExtraBold.ttf', 32)
        self.alg = alg
        self.next_screen = next_screen

    def draw_button(self, screen):
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]

        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            pygame.draw.rect(screen, DIM_GRAY, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height))

        button_text = self.font.render(self.label, True, BLACK, None)
        button_text_rect = button_text.get_rect()
        button_text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
        screen.blit(button_text, button_text_rect)

    def next_menu(self, screen):
        if self.alg is None:
            self.next_screen(screen)
        else:
            self.next_screen(screen, self.alg)

    def set_color(self, color):
        self.color = color

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class Text:
    def __init__(self, x, y, size, text, color=BLACK):
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.size = size
        self.font = pygame.font.Font('fonts/RobotoSlab-ExtraBold.ttf', self.size)
        self.text_object = None
        self.text_object_rect = None

    def create_text(self):
        self.text_object = self.font.render(self.text, True, self.color, None)
        self.text_object_rect = self.text_object.get_rect()
        self.text_object_rect.center = (self.x, self.y)

    def draw_text(self, screen):
        screen.blit(self.text_object, self.text_object_rect)


class Menu:
    def __init__(self):
        self.menu_buttons = []

    def create_menu(self, n, text, algs, func=None):
        if n == 1:
            x = int(WIDTH // 2 - 0.25 * WIDTH)
            y = int(HEIGHT // 2 - 0.25 * WIDTH)

            box_width = WIDTH // 2
            box_height = HEIGHT // 2
            button1 = Button(box_height, box_width, x, y, text[0], algs[0])
            self.menu_buttons.append(button1)

        box_width = int(WIDTH * 1 / 3)
        box_height = int((0.9 * HEIGHT) // n)
        gap = 25
        y = gap

        for i in range(0, n, 2):
            # Checking if drawing left or right column
            left_x = int(WIDTH // 2 - gap - box_width)
            right_x = int(WIDTH // 2 + gap)

            button1 = Button(box_height, box_width, left_x, y, text[i - 1], alg=algs[i - 1], next_screen=func)
            button2 = Button(box_height, box_width, right_x, y, text[i], alg=algs[i], next_screen=func)

            self.menu_buttons.append(button1)
            self.menu_buttons.append(button2)

            y += box_height + gap

    def draw_menu(self, screen):
        for button in self.menu_buttons:
            button.draw_button(screen)

    def menu_selection(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        for button in self.menu_buttons:
            if button.x < mouse_x < button.x + button.width and button.y < mouse_y < button.y + button.height:
                button.next_menu(screen)


class Generator:
    def __init__(self, gen):
        self.gen = gen

    def __iter__(self):
        self.value = yield from self.gen


# Generate Random List
def getList():
    random.seed(0)
    return [random.randint(1, HEIGHT) for _ in range(ELEMENTS)]


def build_adj_list(lyst):
    """Builds the adjacency list for use in pathfinding algorithms"""

    rows = len(lyst)
    cols = len(lyst[0])

    graph = Weighted_Graph()

    for i in range(rows):
        for j in range(cols):
            if lyst[i][j].color == BLACK:
                continue
            if j - 1 >= 0:
                if lyst[i][j - 1].color != BLACK and lyst[i][j - 1].color != AQUATIC_GREEN:
                    graph.addEdge(lyst[i][j].value, lyst[i][j - 1].value)
                elif lyst[i][j - 1].color == AQUATIC_GREEN:
                    graph.addEdge(lyst[i][j].value, lyst[i][j - 1].value, lyst[i][j - 1].weight)

            if j + 1 < cols:
                if lyst[i][j + 1].color != BLACK and lyst[i][j + 1].color != AQUATIC_GREEN:
                    graph.addEdge(lyst[i][j].value, lyst[i][j + 1].value)
                elif lyst[i][j + 1].color == AQUATIC_GREEN:
                    graph.addEdge(lyst[i][j].value, lyst[i][j + 1].value, lyst[i][j + 1].weight)

            if i - 1 >= 0:
                if lyst[i - 1][j].color != BLACK and lyst[i - 1][j].color != AQUATIC_GREEN:
                    graph.addEdge(lyst[i][j].value, lyst[i - 1][j].value)
                elif lyst[i - 1][j].color == AQUATIC_GREEN:
                    graph.addEdge(lyst[i][j].value, lyst[i - 1][j].value, lyst[i - 1][j].weight)

            if i + 1 < rows:
                if lyst[i + 1][j].color != BLACK and lyst[i + 1][j].color != AQUATIC_GREEN:
                    graph.addEdge(lyst[i][j].value, lyst[i + 1][j].value)
                elif lyst[i + 1][j].color == AQUATIC_GREEN:
                    graph.addEdge(lyst[i][j].value, lyst[i + 1][j].value, lyst[i + 1][j].weight)

    return graph.graph


# Maps list values to a frequency and creates .wav files
def map_sound(lst, duration):
    FREQUENCY_UPPER = 1500
    FREQUENCY_LOWER = 100
    SAMPLE_RATE = 44100
    AMPLITUDE = 4096 / 10

    norm_lst = [float(i) / max(lst) for i in lst]

    # Linear interpolating normalized values to frequency band
    frequencies = {val: int(
        (FREQUENCY_UPPER - FREQUENCY_LOWER) / (max(norm_lst) - min(norm_lst)) * (i - min(norm_lst)) + FREQUENCY_LOWER)
        for i, val in zip(norm_lst, lst)}
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    for value in frequencies.values():
        wave = AMPLITUDE * np.sin(2 * np.pi * float(value) * t)
        wavfile.write(f'tones/{value}.wav', SAMPLE_RATE, wave.astype(np.int16))

    return frequencies


# Draws bars for each loop
def draw_bars(generator, bars, screen, frequencies):
    try:
        step = next(generator)
        arr = step[0]
        left = step[1]
        right = step[2]
        current = step[3]

        for i, (bar, height) in enumerate(zip(bars, arr)):
            if i == left or i == right:
                bar.set_color(RED)
            elif current == i:
                bar.set_color(GREEN)
            else:
                bar.set_color(AQUA)

            bar.set_height(height)
            bar.draw(screen)
            pygame.mixer.Sound(f'tones/{frequencies[height]}.wav').play()

        sleep(SLEEP)
    except StopIteration:
        for bar in sorted(bars):
            bar.set_color(DARK_AQUA)
            bar.draw(screen)
            pygame.mixer.Sound(f'tones/{frequencies[bar.height]}.wav').play()
            sleep(SLEEP)
            pygame.display.update()

        return True


def draw_border(boxs):
    # Top edge
    rows = len(boxs)
    cols = len(boxs[0])

    for j in range(cols):
        boxs[0][j].color = BLACK
        boxs[rows - 1][j].color = BLACK

    for i in range(rows):
        boxs[i][0].color = BLACK
        boxs[i][cols - 1].color = BLACK

def draw_pathfinding(generator, screen, boxs):
    for i in generator:
        if boxs[i].color == GREEN or boxs[i].color == RED:
            continue
        elif boxs[i].color == AQUATIC_GREEN:
            boxs[i].color = DARK_PINK
        else:
            boxs[i].color = PINK
        boxs[i].draw_box(screen)
        pygame.display.update()
        sleep(SLEEP)

    for i in generator.value:
        if boxs[i].color == GREEN or boxs[i].color == RED:
            continue
        else:
            boxs[i].color = YELLOW
            boxs[i].draw_box(screen)
            pygame.display.update()
            sleep(SLEEP)

    return True


# Need to blit algorithm name to screen; create a back button, a timer, maybe log for comparison of algs
def displaySortingAlgorithm(screen, alg):
    alg_name = Text(WIDTH // 2, 20, 32, alg.__name__.upper())
    alg_name.create_text()

    screen.fill(AQUA)
    lst = getList()
    frequencies = map_sound(lst, SLEEP)
    bars = []

    for count, value in enumerate(lst):
        bar = Bar(color=BLACK, height=value, i=count)
        bar.draw(screen)
        bars.append(bar)

    generator = alg(lst)
    running = True
    done = False
    # Game loop
    start = pygame.time.get_ticks()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == 8:
                running = False

        if not done:
            screen.fill(WHITE)
            done = draw_bars(generator, bars, screen, frequencies)
            alg_name.draw_text(screen)

            end = pygame.time.get_ticks()
            delta_t = end - start
            timer_text = Text(int(0.9 * WIDTH), 20, 32, str(delta_t / 1000) + " s")
            timer_text.create_text()
            timer_text.draw_text(screen)

        pygame.display.update()


def displayPathfindingAlgorithm(screen, alg):
    boxs = []
    box_width = 20
    box_height = 20
    counter = 0
    for y in range(3, HEIGHT, 25):
        row = []
        for x in range(3, WIDTH, 25):
            row.append(Box(x=x, y=y, width=box_width, height=box_height, value=counter))
            counter += 1
        boxs.append(row)

    draw_border(boxs)

    gen = None
    flattened_box_list = None
    running = True
    start = False
    path_displayed = False
    maze_building = False

    while running:
        screen.fill(AQUA)
        for row in boxs:
            for col in row:
                col.draw_box(screen)

        if maze_building:
            for step in maze_generator:
                if type(step) is list:
                    for val in step:
                        val.draw_box(screen)
                        pygame.display.update()
                else:
                    step.draw_box(screen)
                    pygame.display.update()

            maze_building = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == 8:
                running = False

            # Handle drawing of start,end,and bounds
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                for row in boxs:
                    for col in row:
                        col.draw_bounds(event, boxs)

            # Build weighted maze when 'e' is pressed
            if maze_building is False:
                if event.type == pygame.KEYDOWN and event.key == 101:
                    maze_generator = Generator(pathfinding_algorithms.depth_first_maze_weighted(boxs))
                    maze_building = True

                # Build maze when 'w' is pressed
                elif event.type == pygame.KEYDOWN and event.key == 119:
                    maze_generator = Generator(pathfinding_algorithms.depth_first_maze(boxs))
                    maze_building = True

            # Start algorithm
            if event.type == pygame.KEYDOWN and event.key == 13 and start is False:
                start = None
                end = None
                for row in range(len(boxs)):
                    if start is not None and end is not None:
                        break
                    for col in range(len(boxs[0])):
                        if boxs[row][col].color == GREEN:
                            start = boxs[row][col].value
                        elif boxs[row][col].color == RED:
                            end = boxs[row][col].value

                lyst = build_adj_list(boxs)

                if alg.__name__ == 'a_star':
                    box_positions = []
                    for row in boxs:
                        for box in row:
                            box_positions.append((box.x, box.y))
                    gen = Generator(gen=alg(lyst, start, end, box_positions))
                else:
                    gen = Generator(gen=alg(lyst, start, end))

                flattened_box_list = [item for row in boxs for item in row]
                start = True

        if start is True and path_displayed is False:
            path_displayed = draw_pathfinding(gen, screen, flattened_box_list)

        pygame.display.update()

def displayMST_Algorithm(screen, alg):
    boxs = []
    box_width = 5
    box_height = 5
    counter = 0

    for y in range(50, HEIGHT, 150):
        row = []
        for x in range(50, WIDTH, 150):
            row.append(Box(x=random.randint(50,WIDTH), y=random.randint(50,HEIGHT), width=box_width, height=box_height, value=counter))
            counter += 1

        boxs.append(row)

    lyst = build_adj_list(boxs)
    flattened_box_list = [item for row in boxs for item in row]

    screen.fill(AQUA)
    for node in lyst.keys():
        start_pos = (flattened_box_list[node].x, flattened_box_list[node].y)
        for neighbor in lyst[node].keys():
            end_pos = (flattened_box_list[neighbor].x, flattened_box_list[neighbor].y)
            pygame.draw.line(screen,BLACK,start_pos=start_pos,end_pos=end_pos)

    for row in boxs:
        for col in row:
            col.draw_box(screen)


    gen = Generator(alg(lyst))

    running = True
    start = False
    while running:
        if start:
            for item in gen:
                node = flattened_box_list[item[0]]

                start_pos = (flattened_box_list[item[0]].x, flattened_box_list[item[0]].y)


                for neighbor in lyst[item[0]].keys():
                    print(neighbor)
                    if neighbor == item[1]:
                        continue
                    end_pos = (flattened_box_list[neighbor].x, flattened_box_list[neighbor].y)
                    pygame.draw.line(screen,AQUA,start_pos=start_pos,end_pos=end_pos)
                    flattened_box_list[neighbor].draw_box(screen)


                end_pos = (flattened_box_list[item[1]].x, flattened_box_list[item[1]].y)
                pygame.draw.line(screen,RED,start_pos=start_pos,end_pos=end_pos,width = 2)
                flattened_box_list[item[0]].draw_box(screen)
                sleep(SLEEP)
                pygame.display.update()

            start = False







        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == 8:
                running = False

            if event.type == pygame.KEYDOWN and event.key == 13 and start is False:
                start = True

        pygame.display.update()


def sortingAlgorithmsMenu(screen):
    sorting_menu = Menu()
    button_labels = ["Quick Sort", "Heap Sort", "Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"]
    button_functions = [sorting_algorithms.quick_sort, sorting_algorithms.heap_sort, sorting_algorithms.bubble_sort,
                        sorting_algorithms.selection_sort, sorting_algorithms.insertion_sort,
                        sorting_algorithms.merge_sort]
    sorting_menu.create_menu(6, button_labels, button_functions, displaySortingAlgorithm)

    running = True
    while running:
        screen.fill(AQUA)
        sorting_menu.draw_menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == 8:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                sorting_menu.menu_selection(screen)

        sleep(SLEEP)
        pygame.display.update()


def pathfindingAlgorithmMenu(screen):
    pathfinding_menu = Menu()
    button_labels = ["A-Star", "Breadth First", "Depth First", "Dijkstra"]
    button_functions = [pathfinding_algorithms.a_star, pathfinding_algorithms.breadth_first,
                        pathfinding_algorithms.depth_first, pathfinding_algorithms.dijkstra]
    pathfinding_menu.create_menu(len(button_labels), button_labels, button_functions, displayPathfindingAlgorithm)

    running = True
    while running:
        screen.fill(AQUA)
        pathfinding_menu.draw_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == 8:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pathfinding_menu.menu_selection(screen)

        pygame.display.update()


def spanningTreeAlgorithmsMenu(screen):
    spanning_tree_menu = Menu()
    button_labels = ["Boruvka's", "Prim's", "Kruskal's", 'Reverse-Delete']
    button_functions = [spanning_tree_algorithms.boruvkas, spanning_tree_algorithms.prims,
                        spanning_tree_algorithms.kruskals, spanning_tree_algorithms.reverse_delete]

    spanning_tree_menu.create_menu(len(button_labels), button_labels, button_functions, displayMST_Algorithm)
    running = True

    while running:
        screen.fill(AQUA)
        spanning_tree_menu.draw_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == 8:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                spanning_tree_menu.menu_selection(screen)

        pygame.display.update()

def otherAlgorithmsMenu(screen):
    pass

def main_menu():
    pygame.init()
    icon = pygame.image.load("blur.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Algorithm Visualizer")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    menu = Menu()
    button_labels = ["Pathfinding", "Spanning Trees", "Other",  "Sorting"]
    button_functions = [pathfindingAlgorithmMenu, spanningTreeAlgorithmsMenu, otherAlgorithmsMenu, sortingAlgorithmsMenu]
    menu.create_menu(len(button_labels), button_labels, button_functions)
    menu.menu_buttons[0].next_menu = sortingAlgorithmsMenu
    menu.menu_buttons[1].next_menu = pathfindingAlgorithmMenu
    menu.menu_buttons[2].next_menu = spanningTreeAlgorithmsMenu
    menu.menu_buttons[3].next_menu = otherAlgorithmsMenu


    running = True
    while running:
        screen.fill(AQUA)
        menu.draw_menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu.menu_selection(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main_menu()
