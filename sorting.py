import time

begin_time = time.time()
sort_list = []
active_pieces = []
pas = 0
ended = 0


def swap(arr, i1, i2):
    i3 = arr[i1]
    arr[i1] = arr[i2]
    arr[i2] = i3
    return arr


def partition(lil, st, en, i):
    pre_preset = lil[en]
    preset = pre_preset[0]
    index = st
    value = preset[i]

    for p in range(en-st):
        pre_preset = lil[p + st]
        preset = pre_preset[0]
        if preset[i] <= value:
            lil = swap(lil, index, p + st)
            index += 1

    lil = swap(lil, index, en)
    return lil, index


def quicksort(list_name, start, end, item):
    if start >= end:
        return

    list_name, pivot_index = partition(list_name, start, end, item)

    quicksort(list_name, start, pivot_index - 1, item)
    quicksort(list_name, pivot_index + 1, end, item)
    return list_name
