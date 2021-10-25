import random
import pygame
import numpy as np
from scipy.io import wavfile
from time import sleep
import sorting_algorithms
import pathfinding_algorithms

ELEMENTS = 200
FREQUENCY_UPPER = 1500
FREQUENCY_LOWER = 100
SAMPLE_RATE = 44100
AMPLITUDE = 4096 / 10
DURATION = 0.01
WIDTH = 1000
HEIGHT = WIDTH // 2
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
AQUA = (50, 80, 99)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
DIM_GRAY = (105, 105, 105)
GAP = WIDTH // ELEMENTS


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
        pass

class Box:
    """Creates and update the boxs for pathfinding algorithms"""
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE

    def draw_box(self,screen):
        pygame.draw.rect(screen,self.color, (self.x, self.y, self.width, self.height))

    def update(self,screen):
        mouse = pygame.mouse.get_pos()
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        mouse_buttons = pygame.mouse.get_pressed(3)

        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height:
            if mouse_buttons[0]:
                self.color = GREEN
            elif mouse_buttons[1]:
                self.color = RED
            elif mouse_buttons[2]:
                self.color = BLACK

class Button:

    def __init__(self, height, width, x, y,label, next_screen, alg = None):
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

        button_text = self.font.render(self.label,True,BLACK,None)
        button_text_rect = button_text.get_rect()
        button_text_rect.center = (self.x+self.width//2,self.y+self.height//2)
        screen.blit(button_text,button_text_rect)


    def next_menu(self,screen):
        if self.alg is None:
            self.next_screen(screen)
        else:
            print(self.next_screen.__name__)
            self.next_screen(screen,self.alg)

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

class Menu:
    def __init__(self):
        self.menu_buttons = []

    def create_menu(self, n, text, algs,func = None):
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

            button1 = Button(box_height, box_width, left_x, y, text[i-1], alg = algs[i - 1],next_screen= func)
            button2 = Button(box_height, box_width, right_x, y, text[i], alg = algs[i],next_screen= func)

            self.menu_buttons.append(button1)
            self.menu_buttons.append(button2)

            y += box_height + gap

    def draw_menu(self,screen):
        for button in self.menu_buttons:
            button.draw_button(screen)

    def menu_selection(self,screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        for button in self.menu_buttons:
            if button.x < mouse_x < button.x + button.width and button.y < mouse_y < button.y + button.height:
                button.next_menu(screen)




# Generate Random List
def getList():
    random.seed(0)
    return [random.randint(1, HEIGHT) for _ in range(ELEMENTS)]


# Maps list values to a frequency and creates .wav files
def map_sound(lst, duration):
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

        pygame.display.update()
        sleep(DURATION)
    except StopIteration:
        pass


# Draws gaps will need later
def draw_gaps(screen, gap, width):
    for i in range(ELEMENTS):
        pygame.draw.line(screen, BLACK, (i * gap, 0), (i * gap, width))

# Need to blit algorithm name to screen; create a back button, a timer, maybe log for comparison of algs
def displaySortingAlgorithm(screen, alg):
    print(alg.__name__)

    screen.fill(AQUA)
    lst = getList()
    frequencies = map_sound(lst, DURATION)
    bars = []
    for count, value in enumerate(lst):
        bar = Bar(color=BLACK, height=value, i=count)
        bar.draw(screen)
        bars.append(bar)

    generator = alg(lst)
    running = True
    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_bars(generator, bars, screen, frequencies)


def displayPathfindingAlgorithm(screen):
    pass


def pathfindingAlgorithms(screen):
    pass


def sortingAlgorithmsMenu(screen):
    sorting_menu = Menu()
    button_labels = ["Quick Sort","Heap Sort","Bubble Sort","Selection Sort","Insertion Sort","Merge Sort"]
    button_functions = [sorting_algorithms.quick_sort,sorting_algorithms.heap_sort,sorting_algorithms.bubble_sort,sorting_algorithms.selection_sort,sorting_algorithms.insertion_sort,sorting_algorithms.merge_sort]
    sorting_menu.create_menu(6,button_labels,button_functions,displaySortingAlgorithm)

    running = True
    while running:
        screen.fill(AQUA)
        sorting_menu.draw_menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                sorting_menu.menu_selection(screen)

        sleep(DURATION)
        pygame.display.update()


def pathfindingAlgorithmMenu(screen):
    pathfinding_menu = Menu()
    button_labels = ["A-Star","Breadth First","Depth First","Dijkstra"]
    button_functions = [pathfinding_algorithms.a_star,pathfinding_algorithms.breadth_first,pathfinding_algorithms.depth_first,pathfinding_algorithms.dijkstra]
    pathfinding_menu.create_menu(4, button_labels,button_functions,displayPathfindingAlgorithm)

    running = True
    while running:
        screen.fill(AQUA)
        pathfinding_menu.draw_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pathfinding_menu.menu_selection(screen)

        pygame.display.update()


def main_menu():
    pygame.init()
    icon = pygame.image.load("blur.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Algorithm Visualizer")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))


    main_menu = Menu()
    button_labels = ["Pathfinding","Sorting"]
    button_functions = [pathfindingAlgorithmMenu,sortingAlgorithmsMenu]
    main_menu.create_menu(2,button_labels,button_functions)
    main_menu.menu_buttons[0].next_menu = sortingAlgorithmsMenu
    main_menu.menu_buttons[1].next_menu = pathfindingAlgorithmMenu

    running = True
    while running:
        screen.fill(AQUA)
        main_menu.draw_menu(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_menu.menu_selection(screen)


        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main_menu()
