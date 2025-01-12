import Acrypt as acrypt
import math
import time
import random

from pathlib import Path

import read_write_file
from read_write_file import read_data_1byte as read


if __name__ == '__main__':
    ''' Задание 2'''
    print(f'euler_fun(n):\np = 29, res = {acrypt.euler_fun(29)}\np = 701, res = {acrypt.euler_fun(701)} \n')

    ''' Задание 3'''
    p, q, k = 17, 113, 3
    print(f'fi(pq) = (p-1)(q-1): {acrypt.euler_fun(p * q)} = {(p - 1) * (q - 1)}')
    print(f'fi(p^k) = (p^k)-(p^(k-1)): {acrypt.euler_fun(p ** k)} = {(p ** k) - (p ** (k - 1))}')
    print('\n')

    ''' Задание 4'''
    print(f'Z9 = {acrypt.z_nz_group(9)}')
    print(f'Z7 = {acrypt.z_nz_group(7)}')
    print('\n')

    ''' Задание 5'''
    z17 = 17
    for i in range(1, z17):
        print(f'ord({i}) in (Z/Z17)* = {acrypt.multiplicative_order(i, z17)}')
    print('\n')

    ''' Задание 6'''
    print(f'Z11 = {acrypt.primitive_roots(11)}')
    print(f'Z4 = {acrypt.primitive_roots(4)}')
    print(f'Z7 = {acrypt.primitive_roots(7)}')
    print(f'Z29 = {acrypt.primitive_roots(29)}')
    print(f'Z18 = {acrypt.primitive_roots(18)}')
    # print(f'Z227 = {acrypt.primitive_roots(227)}')
    print('\n')

    ''' Задание 7'''
    print(f'a = 7814, Z = 17449 => a^(-1) = {acrypt.inverse_el(7814, 17449)}')
    print('\n')

    ''' Задание 8'''
    print(f'a = 5, b = 12 => {5 ** acrypt.euler_fun(12) % 12}')
    print(f'a = 2, b = 21 => {2 ** acrypt.euler_fun(21) % 21}')
    print('\n')

    ''' Задание 2.1'''
    p = acrypt.find_p_2q_plus_1(12)
    print('find p = {}, is prime (p-1)/2: {}'.format(p, acrypt.is_prime((p - 1) // 2)))

    ''' Задание 2.2'''
    g = acrypt.find_g(p)
    print('find g = {}'.format(g))

    ''' Задание 2.3'''
    p = acrypt.find_p_2q_plus_1(8)
    # p = 253679

    t0 = time.perf_counter()
    g = acrypt.find_g(p)
    t1 = time.perf_counter()
    print(f'p = {p}, g = {g}, time = {t1 - t0}')

    # print(acrypt.find_factors(77))

    t0 = time.perf_counter()
    g = acrypt.find_first_primitive_root(p)
    t1 = time.perf_counter()
    print(f'p = {p}, g = {g}, time = {t1 - t0}')
    print('\n')

    print(f'Задание 2.4')
    ''' Задание 2.4'''
    t0 = time.perf_counter()
    p, g = acrypt.find_p_g(17)
    t1 = time.perf_counter()
    print(f'p = {p}, g = {g}, time = {t1 - t0}')
    print('\n')

    print(f'Задание 2.5')
    ''' Задание 2.5'''
    for_5 = []

    for i in range(2, 100):
        if acrypt.is_prime(i):
            for_5.append(i)

    print(for_5)
    for p_i in for_5:
        if acrypt.find_g(p_i) == 2:
            print(f'p = {p_i}')
    print('\n')

    ''' Задание 2.6'''
    print(f'Задание 2.6')
    for _ in range(10):
        while True:
            n = random.randrange(13000, 14000)
            if acrypt.is_prime(n):
                print(n)
                break
    print('\n')

    print(f'p = 1000000000061 : is prime? -> {acrypt.is_prime(1000000000061)}')
    print(f'p = 1000000000063 : is prime? -> {acrypt.is_prime(1000000000063)}')
    # print(f'p = 1000000000063 : is prime? -> {acrypt.is_prime(1000000000062)}')
    print('\n')

    thousand_one = 1001
    n = math.factorial(thousand_one)
    for i in range(2, thousand_one + 1):
        print(f'1001! + {i} : {acrypt.is_prime(n + i)}')
    print('\n')

    ''' Задание 2.7'''
    print(f'Задание 2.7')
    n = acrypt.generate_large_prime(32)
    print('{} = {} содержит {} бит'.format(n, bin(n)[2:], len(bin(n)[2:])))
    print('\n')

    ''' Задание 3.1'''
    print(f'Задание 3.1')
    num = acrypt.txt2IntNums(message='Hello world!', block_size=12)
    print('message is a number: {}'.format(num))

    num = acrypt.txt2IntNums(message='Hello world!', block_size=7)
    print('message is a number: {}'.format(num))

    num = acrypt.txt2IntNums(message='Hello world!', block_size=4)
    print('message is a number: {}'.format(num))
    print('\n')

    ''' Задание 3.2'''
    print(f'Задание 3.2')
    msg = acrypt.IntNums2txt([10334410032606748633331426632], message_length=12, block_size=12)
    print('message is {}'.format(msg))
    msg = acrypt.IntNums2txt([33531185161069896, 143418749551], message_length=12, block_size=7)
    print('message is {}'.format(msg))
    print('\n')

    ''' Задание 3.3'''
    print(f'Задание 3.3')
    data = [72, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 33]
    num = acrypt.dat2IntNums(data, block_size=12)
    print('message is a number: {}'.format(num))
    print('\n')

    msg = acrypt.IntNums2dat(num, message_length=12, block_size=12)
    print('message is {}'.format(msg))
    print('\n')

    ''' Задание 3.4'''
    print(f'Задание 3.4')
    data = read_write_file.read_data_1byte(Path('resources', '8', 'text.txt'))
    print('message is : {}'.format(data))
    num = acrypt.dat2IntNums(data, block_size=3)
    print('message is a number: {}'.format(num))
    decrypt_data = acrypt.IntNums2dat(num, len(data), 3)
    print("decrypt_data = ", decrypt_data)
    read_write_file.write_data_1byte(Path('resources', '8', 'decrypt_text.txt'), decrypt_data)