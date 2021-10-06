import random
import pygame
import numpy as np
from scipy.io import wavfile
from time import sleep

ELEMENTS = 200
FREQUENCY_UPPER = 1500
FREQUENCY_LOWER = 100
SAMPLE_RATE = 44100
AMPLITUDE = 4096/10
DURATION = 0.01
WIDTH = 1000
HEIGHT = WIDTH//2
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
AQUA = (50, 80, 99)
GREEN = (0,255,0)
GAP = WIDTH // ELEMENTS


class Bar():
    def __init__(self ,height ,color,i):
        self.height = height
        self.color = color
        self.x = i*GAP
        self.y = 0
        self.width = GAP

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))

    def set_height(self ,h):
        self.height = h

    def set_color(self ,c):
        self.color = c

    def get_height(self):
        return self.height

    def get_color(self):
        pass

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
        for j in range(0,n-i-1):
            if arr[j] > arr[j+1]:
                arr[j],arr[j+1] = arr[j+1],arr[j]
            yield arr,0,n-i-1,j

def insertionSort(arr):
    n = len(arr)

    for i in range(n):
        key = arr[i]
        j = i - 1
        while j >= 0  and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
            yield arr,i,n,j
        arr[j+1] = key

        yield arr,i,n,j

def selectionSort(arr):
    n = len(arr)
    for i in range(n):
        min = i
        for j in range(i+1,n):
            if arr[min] > arr[j]:
                min = j
            yield arr,i,n,j

        arr[i],arr[min] = arr[min],arr[i]
        yield arr,i,n,j

# Generate Random List
def getList():

    random.seed(0)
    return [random.randint(1,HEIGHT) for _ in range(ELEMENTS)]

# Maps list values to a frequency and creates .wav files
def map_sound(lst,duration):

    norm_lst = [float(i)/max(lst) for i in lst]

    # Linear interpolating normalized values to frequency band
    frequencies = {val:int((FREQUENCY_UPPER-FREQUENCY_LOWER)/(max(norm_lst)-min(norm_lst))*(i-min(norm_lst))+FREQUENCY_LOWER) for i,val in zip(norm_lst,lst)}
    t = np.linspace(0,duration,int(SAMPLE_RATE*duration))

    for value in frequencies.values():
        wave = AMPLITUDE*np.sin(2*np.pi*float(value)*t)
        wavfile.write(f'tones/{value}.wav',SAMPLE_RATE,wave.astype(np.int16))



    return frequencies

# Draws bars for each loop
def draw_bars(generator,bars,screen,frequencies):
    try:
        step = next(generator)
        arr = step[0]
        left = step[1]
        right = step[2]
        current = step[3]

        for i,(bar,height) in enumerate(zip(bars,arr)):
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
def draw_gaps(screen,gap,width):
    for i in range(ELEMENTS):
        pygame.draw.line(screen,BLACK, (i*gap,0),(i*gap,width))


def main():
    pygame.init()
    icon = pygame.image.load("blur.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Algorithm Visualizer")
    screen = pygame.display.set_mode((WIDTH,HEIGHT))


    lst = getList()
    frequencies = map_sound(lst,DURATION)
    bars = []
    for count,value in enumerate(lst):
        bar = Bar(color=BLACK,height=value,i=count)
        bar.draw(screen)
        bars.append(bar)
    # generator = quicksort(lst,0,len(lst)-1)
    generator = selectionSort(lst)
    running = True
    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_bars(generator, bars, screen,frequencies)

    pygame.quit()





if __name__ == "__main__":
    main()