import Affine_cipher as ac

''' Задание 1'''


def euler_fun(n):
    res = 0
    for i in range(n):
        if ac.gcd(i, n) == 1:
            res += 1
    return res


def z_nz_group(n):
    group = []
    for i in range(1, n):
        if ac.gcd(i, n) == 1:
            group.append(i)
    return group


def primitive_roots(n):
    if n <= 1:
        return []  # Нет первообразных корней для 0 и 1

    res = []
    for i in range(1, n):
        deg_i = 1
        while pow(i, deg_i, n) != 1:
            deg_i += 1
            if deg_i > euler_fun(n):  # Добавляем условие выхода
                break
        if deg_i == euler_fun(n):
            res.append(i)
    return res


def multiplicative_order(g, n):
    m = 1
    while (g ** m) % n != 1:
        m += 1
    return m


def inverse_el(a, p):
    return pow(a, p - 2, p)


if __name__ == '__main__':
    ''' Задание 2'''
    print(f'euler_fun(n):\np = 29, res = {euler_fun(29)}\np = 701, res = {euler_fun(701)} \n')

    ''' Задание 3'''
    p, q, k = 17, 113, 3
    print(f'fi(pq) = (p-1)(q-1): {euler_fun(p * q)} = {(p - 1) * (q - 1)}')
    print(f'fi(p^k) = (p^k)-(p^(k-1)): {euler_fun(p ** k)} = {(p ** k) - (p ** (k - 1))}')
    print('\n')

    ''' Задание 4'''
    print(f'Z9 = {z_nz_group(9)}')
    print(f'Z7 = {z_nz_group(7)}')
    print('\n')

    ''' Задание 5'''
    z17 = 17
    for i in range(1, z17):
        print(f'ord({i}) in (Z/Z17)* = {multiplicative_order(i, z17)}')
    print('\n')

    ''' Задание 6'''
    print(f'Z11 = {primitive_roots(11)}')
    print(f'Z4 = {primitive_roots(4)}')
    print(f'Z7 = {primitive_roots(7)}')
    print(f'Z29 = {primitive_roots(29)}')
    print(f'Z18 = {primitive_roots(18)}')
    print('\n')

    ''' Задание 7'''
    print(f'a = 7814, Z = 17449 => a^(-1) = {inverse_el(7814, 17449)}')
    print('\n')

    ''' Задание 8'''
    print(f'a = 5, b = 12 => {5 ** euler_fun(12) % 12}')
    print(f'a = 2, b = 21 => {2 ** euler_fun(21) % 21}')
