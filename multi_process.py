"""pypy 175.676 sec cpython 432.0126350000064 seconds"""
from typing import List, Dict
import multiprocessing as mp
import os

def process_chuck(start: int, end: int):
    filename = 'measurements.txt'
    
    results: Dict[str: List] = {}  # dict array like {'city': [..]} with index 0 minimum temperature, 1 average, 2 maximum, 3 the amount (needed to calcualte the average)

    with open(filename, 'r') as f:
        f.seek(start)
        current_char = start
        line_num = 0
        for line in f:
            current_char += len(line)  #
            if current_char > end:
                break
            city, temperature_str = line.split(';')
            temperature = float(temperature_str)
            if city not in results:
                results[city] = [temperature,temperature,temperature, 1]
            else:
                results[city][0] = min(results[city][0], temperature)  # update the minumun temperature
                results[city][1] = (results[city][1] * results[city][3] + temperature) / (results[city][3] + 1)
                results[city][3] += 1
                results[city][2] = max(results[city][2], temperature)
            # line_num += 1
            # if line_num in (50_000_000,100_000_000, 150_000_000, 200_000_000, 250_000_000):
            #     print(f"Line {line_num}")
    return results

def main(max_cpu=6):
    filename = 'measurements.txt'
    cpu_count = min(max_cpu, mp.cpu_count())
    print(f"Using {cpu_count} cpu's")

    file_size = os.path.getsize(filename)
    chunk_size = file_size // cpu_count

    start = 0
    end_position = 0
    offsets = []
    with open(filename) as f:
        for _ in range(cpu_count):
            end_position = start + chunk_size
            f.seek(end_position)
            while end_position < file_size and f.read(1) != "\n":
                f.seek(end_position)
                end_position += 1
            offsets.append((start,end_position))
            start = end_position + 1
    with mp.Pool(cpu_count) as p:
        chunk_results = p.starmap(
            process_chuck,
            offsets,
        )       
    print(chunk_results)        




if __name__ == '__main__':
    from timeit import timeit
    print(timeit(main, number=1))