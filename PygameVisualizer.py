import random
import pygame
import numpy as np
from scipy.io import wavfile
from time import sleep
import sys

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

class Button:

    def __init__(self,height,width,x,y):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.color = GRAY

    def draw_button(self,screen):
        pygame.draw.rect(screen,GRAY,(self.x,self.y,self.width,self.height))

    def set_color(self,color):
        self.color = color

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

class menu:

     def draw_menu(self,screen,n,text,text_rect):
         if n == 1:
             x = int(WIDTH // 2 - 0.25*WIDTH)
             y = int(HEIGHT // 2 - 0.25*WIDTH)
             box_width = WIDTH//2
             box_height = HEIGHT//2
             pygame.draw.rect(screen,GRAY,(x,y,box_width,box_height))

         box_width = int(WIDTH * 1 / 3)
         box_height = int((0.9 * HEIGHT)//n)
         for i in range(n):

            # Checking if drawing left or right column
            if i % 2 != 0:
                x = int(WIDTH // 2 - 0.25 * WIDTH)
            else:
                x = int(WIDTH // 2 + 0.25 * WIDTH - box_width)

                y = HEIGHT // 10
                pygame.draw.rect(screen,GRAY,(x,y,box_width,box_height))





# quicksort function
def quicksort(arr, left, right):
    if left >= right:
        return
    x = arr[left]
    j = left
    for i in range(left + 1, right + 1):
        if arr[i] <= x:
            j += 1
            arr[j], arr[i] = arr[i], arr[j]
        yield arr, left, right, i
    arr[left], arr[j] = arr[j], arr[left]
    yield arr, left, right, i

    # yield from statement used to yield
    # the array after dividing
    yield from quicksort(arr, left, j - 1)
    yield from quicksort(arr, j + 1, right)


def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr, 0, n - i - 1, j


def insertionSort(arr):
    n = len(arr)

    for i in range(n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, i, n, j
        arr[j + 1] = key

        yield arr, i, n, j


def selectionSort(arr):
    n = len(arr)
    for i in range(n):
        min = i
        for j in range(i + 1, n):
            if arr[min] > arr[j]:
                min = j
            yield arr, i, n, j

        arr[i], arr[min] = arr[min], arr[i]
        yield arr, i, n, j


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


def displaySortingAlgorithm(screen,alg):
    screen.fill(AQUA)
    lst = getList()
    frequencies = map_sound(lst, DURATION)
    bars = []
    for count, value in enumerate(lst):
        bar = Bar(color=BLACK, height=value, i=count)
        bar.draw(screen)
        bars.append(bar)
    # generator = quicksort(lst,0,len(lst)-1)
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


def sortingAlgorithmsMenu(screen,font):
    sorting_alg_list = ["bubbleSortMenu,selectionSort","insertionSort",'quickSort','mergeSort','heapSort','bucketSort']

    rows = 3
    columns = 2
    padding = 100

    button_padding = 50
    box_width = 250
    box_height = 100

    button_labels = ["Bubble Sort","Selection Sort","Insertion Sort","Quick Sort","Merge Sort","Heap Sort","Bucket Sort"]

    button_y = (HEIGHT - 2 * padding) // rows - box_height // 2
    buttons = []
    for i in range(rows):
        button_x = (WIDTH - 2 * padding) // columns - box_width // 2

        for j in range(columns):
                buttons.append(Button(box_height,box_width,button_x,button_y))
                button_x += box_width+button_padding
        button_y += box_height+button_padding

    button_text = []
    for text,button in zip(button_labels,buttons):
        button.draw_button(screen)

        text = font.render(text,True,BLACK,None)
        text_rect = text.get_rect()
        text_rect.center = (button.get_x()+button.get_width()//2,button.get_y()+button.get_height()//2)
        button_text.append([text,text_rect])



    # start_time = pygame.time.get_ticks()


    mouse = pygame.mouse.get_pos()
    running = True
    while running:
        # current_time = pygame.time.get_ticks()
        # delta_t = (current_time-start_time)//2
        # counter_text = font.render(str(delta_t),True,BLACK,None)
        # counter_text_rect = counter_text.get_rect()
        # counter_text_rect.center = (25, 25)
        screen.fill(AQUA)
        # screen.blit(counter_text,counter_text_rect)


        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event == pygame.QUIT:
                running = False
            if event == pygame.MOUSEBUTTONDOWN:
                if buttons[0].get_x() < mouse[0] < buttons[0].get_x() + box_width:
                    if buttons[1].get_y() < mouse[1] < buttons[1].get_y() + box_height:
                        print("Send it ")
                        displaySortingAlgorithm(screen,bubbleSort)
                # for alg,button in zip(sorting_alg_list,buttons):
                #     if button.get_x() < mouse[0] < button.get_x()+button.get_width():
                #         if button.get_y() < mouse[1] < button.get_y()+button.get_height():
                #             displaySortingAlgorithm(screen,alg)

        # for button in buttons:
        #     if button.get_x() < mouse[0] < button.get_x() + box_width:
        #         print(mouse[1])
        #         print(button.get_y(),button.get_y() + box_height)
        #         if button.get_y() < mouse[1] < button.get_y() + box_height:
        #             button.set_color(DIM_GRAY)
        #             button.draw_button(screen)
        #     else:
        #         button.set_color(GRAY)
        #         button.draw_button(screen)
        if buttons[0].get_x() < mouse[0] < buttons[0].get_x() + box_width:
            if buttons[0].get_y() < mouse[1] < buttons[0].get_y() + box_height:
                buttons[0].set_color(DIM_GRAY)
                buttons[0].draw_button(screen)
        else:
            buttons[0].set_color(GRAY)
            buttons[0].draw_button(screen)

        for text in button_text:
            screen.blit(text[0],text[1])



        pygame.display.update()
    pygame.quit()



def pathfindingAlgorithmMenu(screen,font):
    pass

def main_menu():
    pygame.init()
    icon = pygame.image.load("blur.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Algorithm Visualizer")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    font = pygame.font.Font('fonts/RobotoSlab-ExtraBold.ttf', 32)

    button1_bounds = [[0.3 * WIDTH, 0.7 * WIDTH], [0.15 * HEIGHT, 0.45 * HEIGHT]]
    button2_bounds = [[0.3 * WIDTH, 0.7 * WIDTH], [0.55 * HEIGHT, 0.85 * HEIGHT]]

    sorting_text = font.render('Sorting Algorithms', True, BLACK, None)
    sorting_text_rect = sorting_text.get_rect()
    sorting_text_rect.center = (500, 150)


    pathfinding_text = font.render('Pathfinding Algorithms', True, BLACK, None)
    pathfinding_text_rect = pathfinding_text.get_rect()
    pathfinding_text_rect.center = (500, 350)

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill(AQUA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1_bounds[0][0] < mouse[0] < button1_bounds[0][1]:
                    if button1_bounds[1][0] < mouse[1] < button1_bounds[1][1]:
                       sortingAlgorithmsMenu(screen,font)

                elif button2_bounds[0][0] < mouse[0] < button2_bounds[0][1]:
                    if button2_bounds[1][0] < mouse[1] < button2_bounds[1][1]:
                        pathfindingAlgorithmMenu(screen,font)

        if button1_bounds[0][0] < mouse[0] < button1_bounds[0][1] and button1_bounds[1][0] < mouse[1] < button1_bounds[1][1]:
            pygame.draw.rect(screen, DIM_GRAY, (300, 75, 400, 150))
        else:
            pygame.draw.rect(screen, GRAY, (300, 75, 400, 150))


        if button2_bounds[0][0] < mouse[0] < button2_bounds[0][1] and button2_bounds[1][0] < mouse[1] < button2_bounds[1][1]:
            pygame.draw.rect(screen, DIM_GRAY, (300, 275, 400, 150))
        else:
            pygame.draw.rect(screen, GRAY, (300, 275, 400, 150))

        screen.blit(sorting_text, sorting_text_rect)
        screen.blit(pathfinding_text, pathfinding_text_rect)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main_menu()
