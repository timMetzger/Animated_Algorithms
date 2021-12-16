import random


# TODO if i want to add more sorting algorithms i am going to need to rework the way that I am visualzing them because
# at the moment i am just returning the list of updated height values. I will need to pass the bar object to the
# algorithm to update the values directly for algorithms like merge sort or bin sort

def radix_sort(arr):
    # LSD method for nums
    # MSD method for alphabet
    max_num = max(arr)
    exp = 1
    while max_num / exp > 1:
        yield from counting_sort(arr, exp)
        exp *= 10


def counting_sort(arr, exp):
    n = len(arr)

    output = [0] * n
    count = [0] * 250

    # Counting occurrences of values
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
        yield arr, 0, n - 1, i

    # Change count[i] to be actual position in output
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build output
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    # Modify arr so that bars are correct height
    i = 0
    for i in range(n):
        arr[i] = output[i]
        yield arr, 0, n - 1, i


def merge_sort(arr):
    print(arr)
    if len(arr) <= 1:
        return arr

    # Dividing list into left and right halves
    left = []
    right = []

    for i, x in enumerate(arr):
        if i < len(arr) / 2:
            left.append(x)
        else:
            right.append(x)

    left = merge_sort(left)
    right = merge_sort(right)

    yield from merge(left, right, len(arr))


def merge(left, right, size):
    result = []
    i = 0
    print(left, right)
    while left and right:
        if left[0] <= right[0]:
            l = left[0]
            result.append(left[0])
            left = left[1:]
        else:
            l = left[0]
            result.append(right[0])
            right = right[1:]
        i += 1

        yield result, 0, size, 0

    while left:
        result.append(left[0])
        left = left[1:]

    while right:
        result.append(right[0])
        right = right[1:]

    yield result, 0, size, 0


def quick_sort(arr, left=None, right=None):
    if right is None:
        right = len(arr) - 1
    if left is None:
        left = 0

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
    yield from quick_sort(arr, left, j - 1)
    yield from quick_sort(arr, j + 1, right)


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr, 0, n - i - 1, j


def insertion_sort(arr):
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


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        minimum = i
        for j in range(i + 1, n):
            if arr[minimum] > arr[j]:
                minimum = j
            yield arr, i, n, j

        arr[i], arr[minimum] = arr[minimum], arr[i]
        yield arr, i, n, j


def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[largest] < arr[left]:
        largest = left
    if right < n and arr[largest] < arr[right]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]

        yield arr, left, right, i

        yield from heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield from heapify(arr, i, 0)


# arr = [random.randint(1, 100) for _ in range(100)]
# print(merge_sort(arr))
