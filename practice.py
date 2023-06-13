import time

start_time = time.time()

def insertion_sort(sequence):
    for i in range(1, len(sequence)):
        key = sequence[i]
        j = i - 1
        while j >= 0 and sequence[j] > key:
            sequence[j + 1] = sequence[j]
            j -= 1
        sequence[j + 1] = key

def find_position(sequence, k):
    insertion_sort(sequence)
    for i in range(len(sequence)):
        if sequence[i] == k:
            return i + 1
    return -1

sequence = [2, -1, 3, 0, 7, 3]
k = 3
position = find_position(sequence, k)
print(position)

end_time = time.time()
execution_time = end_time - start_time

print("Execution time:", execution_time, "seconds")
