import multiprocessing
import random
import re
from time import time
import matplotlib.pyplot as plt


def benchmark(func,
              lst,
              queue: list[int]):
    pattern = r'[a-z]*_[a-z]*'
    start = time()
    func(lst)
    end = time()
    working_time = end - start
    queue.put((*re.findall(pattern, (str(func))), len(lst), working_time))


def bubble_sort(lst: list[int]) -> list[int]:
    n = len(lst)

    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


def selection_sort(lst: list[int]) -> list[int]:
    size = len(lst)
    for s in range(size):
        min_idx = s

        for i in range(s + 1, size):
            if lst[i] < lst[min_idx]:
                min_idx = i

        (lst[s], lst[min_idx]) = (lst[min_idx], lst[s])
    return lst


def insertion_sort(lst: list[int]) -> list[int]:
    for i in range(1, len(lst)):

        a = lst[i]
        j = i - 1

        while j >= 0 and a < lst[j]:
            lst[j + 1] = lst[j]
            j -= 1

        lst[j + 1] = a

    return lst


def create_graph(plt,
                 data: dict,
                 text: bool = False):
    result = []
    for key, value in data.items():
        item = plt.plot(value[0], value[1], marker='o', markersize=3, label=f'{key}')
        result.append(item)
        if text:
            for size, time in zip(value[0], value[1]):
                plt.text(size, time, f'{round(time, 2)}', fontsize=6, color='black')
    return result


def unpack_data(raw_data: list) -> dict:
    print(raw_data)
    result = {}
    for i in raw_data:
        if not i[0] in result:
            result[i[0]] = [i[1]], [i[2]]
        else:
            result[i[0]][0].append(i[1])
            result[i[0]][1].append(i[2])
    print(result)
    return result


if __name__ == '__main__':
    small_data = random.sample(range(1000), 1000)
    medium_data = random.sample(range(5000), 5000)
    big_data = random.sample(range(10000), 10000)

    sorting_algorithms = [bubble_sort, selection_sort, insertion_sort]
    list_to_sort = [small_data, medium_data, big_data]

    queue = multiprocessing.Queue()

    processes = []

    for i in sorting_algorithms:
        for j in list_to_sort:
            p = multiprocessing.Process(target=benchmark, args=(i, j, queue))
            processes.append(p)

    for i in processes:
        i.start()

    raw_data = []

    for i in range(len(processes)):
        raw_data.append(queue.get())

    for p in processes:
        p.join()

    data = unpack_data(raw_data)
    fig, ax = plt.subplots()
    colors = ('red', 'blue', 'green')

    graphs = create_graph(ax, data, True)
    ax.set_ylabel('Time (seconds)')
    ax.set_xlabel('Size (items)')
    plt.title('Time Spent and Size of Work by function')
    ax.legend()
    plt.show()
