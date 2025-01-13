import math

import Affine_cipher as ac
import random

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


def find_factors(n):
    """Находит все простые делители числа n."""
    factors = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


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

        if is_prime(p):
            q = (p - 1) // 2

            # Проверяем, что q - простое число
            if is_prime(q):
                return p


''' Задание 2.2'''


def find_g(p):
    q = (p - 1) // 2
    for g in range(2, p - 1):
        if pow(g, q, p) != 1:
            return g


def find_first_primitive_root(p):
    if p == 2:
        return 1

    phi_p = p - 1
    factors = find_factors(phi_p)

    for g in range(2, p):
        is_primitive = True
        for q in factors:
            if pow(g, phi_p // q, p) == 1:
                is_primitive = False
                break
        if is_primitive:
            return g


''' Задание 2.4'''


def find_p_g(bitfield_width):
    p = find_p_2q_plus_1(bitfield_width)
    g = find_g(p)
    return p, g


''' Задание 2.5'''


def rabin_miller(n):
    # Returns True if num is a prime number.
    q = n - 1
    k = 0
    while q % 2 == 0:
        # keep halving s until it is even (and use t
        # to count how many times we halve s)
        q = q // 2
        k += 1
    t = 5
    for trials in range(t):  # try to falsify num's primality 5 times
        a = random.randrange(2, n - 1)
        v = pow(a, q, n)
        if v != 1:  # this test does not apply if v is 1.
            i = 0
            while v != (n - 1):
                if i == k - 1:
                    return False, 0
                else:
                    i = i + 1
                    v = (v ** 2) % n
    probability_of_prime = 1 - 1.0 / (4 ** t)
    return True, probability_of_prime


''' Задание 2.6'''


def is_prime(n):
    # Return True if n is a prime number. This function does a quicker
    # prime number check before calling rabin_miller().
    if n < 2:
        return False  # 0, 1, and negative numbers are not prime
    # About 1/3 of the time we can quickly determine if n is not prime
    # by dividing by the first few dozen prime numbers. This is quicker
    # than rabin_miller().
    low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                  103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                  211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                  331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                  449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                  587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                  709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                  853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                  991, 997]
    if n in low_primes:
        return True
    # See if any of the low prime numbers can divide n
    for prime in low_primes:
        if n % prime == 0:
            return False
    # If all else fails, call rabin_miller() to determine if n is a prime.
    return rabin_miller(n)


''' Задание 2.7'''


def generate_large_prime(bitfield_width):
    while True:
        candidate = random.getrandbits(bitfield_width)
        if candidate & 1 == 0:
            candidate += 1
        candidate |= (1 << bitfield_width - 1)
        candidate |= (2 << bitfield_width - 3)
        if is_prime(candidate):
            return candidate


''' Задание 3.1'''


def txt2IntNums(message, block_size):
    # Разбиваем сообщение на блоки
    blocks = [message[i:i + block_size] for i in range(0, len(message), block_size)]

    # Преобразуем каждый блок в число
    result = []
    for block in blocks:
        block_num = 0
        for i, char in enumerate(block):
            block_num += ord(char) * (256 ** i)
        result.append(block_num)

    return result


''' Задание 3.2'''


def IntNums2txt(block_ints, message_length, block_size):
    result_message = []

    for block_int in block_ints:
        block_message = []
        for _ in range(block_size):
            char = chr(block_int % 256)
            block_message.append(char)
            block_int //= 256

        result_message.extend(block_message)

    return ''.join(result_message)[:message_length]


def dat2IntNums(data, block_size):
    blocks = [data[i:i + block_size] for i in range(0, len(data), block_size)]

    result = []
    for block in blocks:
        block_num = 0
        for i, value in enumerate(block):
            block_num += value * (256 ** i)
        result.append(block_num)

    return result


def IntNums2dat(block_ints, message_length, block_size):
    result_data = []

    for block_int in block_ints:
        block_data = []
        for _ in range(block_size):
            value = block_int % 256
            block_data.append(value)
            block_int //= 256

        result_data.extend(block_data)

    return result_data[:message_length]


# A = pub_key
def elgamal_encrypt_element(pub_key, g, p, m):
    k = random.randint(1, p - 1)
    c1 = pow(g, k, p)
    c2 = (m * pow(pub_key, k, p)) % p
    return c1, c2


def elgamal_decrypt_element(a, p, c1, c2):
    inv_c1_pow_a = inverse_el(pow(c1, a, p), p)
    return (c2 * inv_c1_pow_a) % p


def elgamal_encrypt(nums, priv_key):
    max_el = max(nums)
    bitfield_width = math.floor(math.log2(max_el)) + 2
    p, g = find_p_g(bitfield_width)
    pub_key = pow(g, priv_key, p)

    encrypt_nums = []
    for element in nums:
        encrypt_nums.append(elgamal_encrypt_element(pub_key, g, p, element))

    return pub_key, p, encrypt_nums


def elgamal_decrypt(encrypt_nums, a, p):
    decrypt_nums = []
    for element in encrypt_nums:
        decrypt_nums.append(elgamal_decrypt_element(a, p, element[0], element[1]))

    return decrypt_nums


def elgamal_decrypt_without2arrays(encrypt_nums, a, p):
    decrypt_nums = []
    for i in range(0, len(encrypt_nums), 2):
        decrypt_nums.append(elgamal_decrypt_element(a, p, encrypt_nums[i], encrypt_nums[i + 1]))

    return decrypt_nums
