import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

def getList():
    ELEMENTS = 200
    random.seed(0)
    return [random.randint(1,1000) for _ in range(ELEMENTS)]

def bubbleSort():
    n = len(lst)
    i = bubbleSort.counter
    for j in range(0,n-i-1):
        if lst[j] > lst[j+1]:
            lst[j],lst[j+1]=lst[j+1],lst[j]

    bubbleSort.counter += 1

bubbleSort.counter = 0

def selectionSort():
    i = selectionSort.counter
    if i != len(lst):
        min = i
        for j in range(i+1,len(lst)):
            if lst[min] > lst[j]:
                min = j
        lst[i],lst[min] = lst[min],lst[i]
        selectionSort.counter += 1

selectionSort.counter = 0

def insertionSort():
    i = insertionSort.counter
    if i != len(lst):
        key = lst[i]
        j = i - 1
        while j>=0 and key < lst[j]:
            lst[j+1] = lst[j]
            j -= 1
        lst[j+1] = key
        insertionSort.counter += 1

insertionSort.counter = 1


# quicksort function
def quicksort(a, l, r):
    if l >= r:
        return
    x = a[l]
    j = l
    for i in range(l + 1, r + 1):
        if a[i] <= x:
            j += 1
            a[j], a[i] = a[i], a[j]
        yield a
    a[l], a[j] = a[j], a[l]
    yield a

    # yield from statement used to yield
    # the array after dividing
    yield from quicksort(a, l, j - 1)
    yield from quicksort(a, j + 1, r)

def update(frame,algorithm):

    for i,rect in enumerate(bars):
        rect.set_height(lst[i])

    return bars


update.counter = 0

lst = getList()

generator = quicksort(lst,0,len(lst)-1)



# fig = plt.figure(figsize=[12,12])
#
# bars = plt.bar(x = range(len(lst)),height = lst,width=1.5,linewidth=0)
# ani = FuncAnimation(fig,update,fargs=(bubbleSort,),frames=len(lst),blit=True,interval=200)
# plt.show()
# # ani.save('quickSort.gif',fps=60)



