import Acrypt as acrypt
from sympy import isprime
import time

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

    ''' Задание 2.1'''
    p = acrypt.find_p_2q_plus_1(12)
    print('find p = {}, is prime (p-1)/2: {}'.format(p, isprime((p - 1) // 2)))

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
