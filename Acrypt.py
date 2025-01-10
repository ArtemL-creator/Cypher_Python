import Affine_cipher as ac
import random
from sympy import isprime

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

    phi_n = euler_fun(n)  # Вычисляем φ(n) один раз
    res = []

    for i in range(1, n):
        if ac.gcd(i, n) != 1:  # Пропускаем числа, не взаимно простые с n
            continue

        seen = set()
        value = 1
        for _ in range(phi_n):
            value = (value * i) % n
            if value in seen:  # Если цикл зациклился, i не является первообразным корнем
                break
            seen.add(value)

        if len(seen) == phi_n:
            res.append(i)

    return res


def multiplicative_order(g, n):
    m = 1
    while (g ** m) % n != 1:
        m += 1
    return m


def inverse_el(a, p):
    return pow(a, p - 2, p)


''' Задание 2.1'''


def find_p_2q_plus_1(bitfield_width):
    # Границы диапазона для числа p
    lower_bound = 2 ** (bitfield_width - 1)
    upper_bound = 2 ** bitfield_width - 1

    while True:
        p = random.randint(lower_bound, upper_bound)

        if isprime(p):
            q = (p - 1) // 2

            # Проверяем, что q - простое число
            if isprime(q):
                return p


''' Задание 2.2'''


def find_g(q2_plus_1):
    p = q2_plus_1
    q = (q2_plus_1 - 1) // 2
    for g in range(2, p - 1):
        if ((g ** q) % p != 1):
            return g


def find_first_primitive_root(p):
    if p == 2:
        return 1

    arr_p = primitive_roots(p)

    for g in range(2, p):
        for i in range(len(arr_p)):
            if (g ** ((p - 1) // arr_p[i])) % p == 1:
                break
            if i == len(arr_p) - 1:
                return g
