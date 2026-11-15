from random import choice
import string
import time
import tracemalloc

CHARS = string.ascii_letters + string.digits


def menu():
    while True:
        print('\n0. Exit\n' '1. Test memory (yield vs return)\n' '2. Test Find for set/dict\n')
        res = input('Your choice: ')

        match res:
            case '0':
                return 0
            case '1':
                n = int(input('Please enter count symbols: '))
                peak1 = write_tracemalloc_r(n)
                peak2 = write_tracemalloc_y(n)
                print(f'peak_r - peak_y = {peak1 - peak2} bytes')
                if peak2 > 0:
                    print(f'peak_r / peak_y = {peak1 / peak2:.2f}x')
            case '2':
                target = str(input('Please enter find symbol: '))
                benchmark_search(target)
            case _:
                print('Please repeat enter!\n')


def gen_yield(n):
    for _ in range(n):
        yield choice(CHARS)


def gen_return(n):
    return ''.join(choice(CHARS) for _ in range(n))


def write_tracemalloc_y(n):
    tracemalloc.start()
    with open('file.txt', 'w', encoding='utf-8') as file:
        for data in gen_yield(n):
            file.write(data)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f'Пиковая память (yield): {peak} bytes')
    return peak


def write_tracemalloc_r(n):
    tracemalloc.start()
    with open('file.txt', 'w', encoding='utf-8') as file:
        data = gen_return(n)
        file.write(data)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f'Пиковая память (return): {peak} bytes')
    return peak


def benchmark_search(target):
    try:
        with open('file.txt', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print('Сначала выполните пункт 1, чтобы создать файл!')
        return

    data_list = list(content)
    data_set = set(data_list)
    data_dict = {symb: True for symb in data_list}

    for name, container in [
        ('list', data_list),
        ('set', data_set),
        ('dict', data_dict),
    ]:
        start = time.perf_counter()
        _ = target in container
        elapsed = time.perf_counter() - start
        print(f'Поиск в {name:4}: {elapsed:.8f} сек')


def main():
    menu()


if __name__ == '__main__':
    main()