# takes forever..
from typing import List, Dict

def main():
    FILENAME = "measurements.txt"

    results: Dict[str: List[float, float, float, int]] = {}  # dict array like {'city': [..]} with index 0 minimum temperature, 1 average, 2 maximum, 3 the amount (needed to calcualte the average)

    with open(FILENAME, 'r') as file:
        for line in file:
            city, temperature_str = line.split(';')
            temperature = float(temperature_str)
            if city not in results:
                results[city] = [temperature,temperature,temperature, 1]
            else:
                results[city][0] = min(results[city][0], temperature)  # update the minumun temperature for this city
                results[city][1] = (results[city][1] * results[city][3] + temperature) / (results[city][3] + 1)  # update the average for this city
                results[city][2] = max(results[city][2], temperature)  # update the max for this city
                results[city][3] += 1  # increment the count for this city

    print(results)

if __name__ == '__main__':
    from timeit import timeit
    print(timeit(main, number=1))