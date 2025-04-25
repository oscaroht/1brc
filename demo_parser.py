from timeit import timeit

def string_replace():
    string = '10.7'
    return int(string.replace(".", ''))

def float_times_ten():
    return int(float('10.7') * 10)

def remove_index():
    string = '10.7'
    return int(string[:-2] + string[-1])

def split_join():
    string = '10.7'
    return int( ''.join(string.split('.')) )

def skip_index():
    string = '10.7'
    return int(string[:len(string)-2] + string[-1])


if __name__ == '__main__':
    print(timeit(string_replace))
    print(timeit(float_times_ten))
    print(timeit(remove_index))
    print(timeit(split_join))
    print(timeit(skip_index))