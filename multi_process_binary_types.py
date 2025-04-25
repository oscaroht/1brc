"""pypy 89.89829069998814  - 362.9802859000047 seconds"""
from typing import List, Dict
import multiprocessing as mp
from gc import disable as gc_disable, enable as gc_enable
import os

def process_chuck(start: int, end: int, filename: str):
    results: Dict[str: List] = {}  # dict array like {'city': [..]} with index 0 minimum temperature, 1 total, 2 maximum, 3 count (needed to calcualte the average)

    with open(filename, 'rb') as f:
        gc_disable()
        f.seek(start)
        current_char = start
        line_num = 0
        for line in f:
            current_char += len(line)
            if current_char > end:
                break
            city_b, temperature_str = line.split(b';')
            city = city_b.decode("utf-8")
            temperature = int(temperature_str.replace(b".", b""))
            city_results = results.get(city, None)
            if city_results is None:
                results[city] = [temperature,temperature,temperature, 1]
            else:
                city_results[0] = min(city_results[0], temperature)  # update the minumun temperature
                city_results[1] += temperature
                city_results[3] += 1
                city_results[2] = max(city_results[2], temperature)
            # line_num += 1
            # if line_num in (50_000_000,100_000_000, 150_000_000, 200_000_000, 250_000_000):
            #     print(f"Line {line_num}")
        gc_enable()
    return results

def main(max_cpu=6):
    filename = 'measurements.txt'
    cpu_count = min(max_cpu, mp.cpu_count())
    print(f"Using {cpu_count} cpu's")

    file_size = os.path.getsize(filename)
    chunk_size = file_size // cpu_count
    print(f"File {filename} of size {file_size}b")

    start = 0
    end_position = 0
    process_chunk_args = []
    with open(filename, 'rb') as f:
        for _ in range(cpu_count):
            end_position = start + chunk_size
            f.seek(end_position)
            while end_position < file_size and f.read(1) != b"\n":
                f.seek(end_position)
                end_position += 1
            process_chunk_args.append((start, end_position, filename))
            start = end_position
    with mp.Pool(cpu_count) as p:
        chunk_results = p.starmap(
            process_chuck,
            process_chunk_args,
        )       

    print("Reduce result")   
    
    combined_result = {}
    for result in chunk_results:
        for city, score in result.items():
            if city not in combined_result:
                combined_result[city] = score
            else:
                current_score = combined_result[city]
                combined_result[city][0] = min(current_score[0], score[0])  # update the minumun temperature
                combined_result[city][1] += score[0]
                combined_result[city][2] = max(current_score[2], score[2])
                combined_result[city][3] += score[3]
    
    print({city: [score[0]/10, (score[1]/score[3])/10, score[2]/10] for city, score in combined_result.items() })


if __name__ == '__main__':
    from timeit import timeit
    time = timeit(main, number=1)
    print("************ Time ******************")
    print(time)