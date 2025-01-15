import Acrypt as acrypt
import math
import time
import random
from sympy import discrete_log

from pathlib import Path

import read_write_file


def parse_encrypted_data(raw_bytes):
    # Преобразуем байты в строку
    raw_string = ''.join(chr(b) for b in raw_bytes)
    # Разделяем строку на числа
    return list(map(int, raw_string.split()))


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
    print(f'a = 7814, Z = 17449 => a^(-1) = {acrypt.inverse_el_for_prime(7814, 17449)}')
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
    nums = acrypt.dat2IntNums(data, block_size=3)
    print('message is a number: {}'.format(nums))
    decrypt_data = acrypt.IntNums2dat(nums, len(data), 3)
    print("decrypt_data = ", decrypt_data)
    read_write_file.write_data_1byte(Path('resources', '8', '3.4_decrypt_text.txt'), decrypt_data)

    m = 331
    p = 467
    g = 2
    a = 153
    A = pow(g, a, p)
    print(f'Pub key = {A}')
    c1, c2 = acrypt.elgamal_encrypt_element(A, g, p, m)
    print(f'c1 = {c1}, c2 = {c2}')

    m_ = acrypt.elgamal_decrypt_element(a, p, c1, c2)
    print(f'm_ = {m_}')
    print('\n')

    ''' Задание 4.2'''
    print(f'Задание 4.2')
    m1mk = [89, 97]
    ma = acrypt.crt(2345, m1mk)
    print(f'ma = {ma}')
    print('\n')

    ''' Задание 4.3'''
    print(f'Задание 4.3')
    A = acrypt.crt_inv(ma, m1mk)
    print(f'A = {A}')
    print('\n')

    ''' Задание 4.4'''
    print(f'Задание 4.4')
    m1mk = [5, 8, 19]
    ma = [1, 2, 3]
    A = acrypt.crt_inv(ma, m1mk)
    print(f'A = {A}')
    print('\n')

    ''' Задание 4.5'''
    print(f'Задание 4.5')
    m1mk = [5, 9]
    ma = [3, 7]
    A = acrypt.crt_inv(ma, m1mk)
    print(f'A = {A}')
    print('\n')

    ''' Задание 4.7'''
    print(f'Задание 4.7')
    p = 901679
    g = 7
    pub_key = 386434
    t0 = time.perf_counter()
    priv_key = acrypt.dlog(g, pub_key, p)
    t1 = time.perf_counter()
    print(f'priv key = {priv_key}, time: {t1 - t0}')
    print(f'pub key -> {pow(g, priv_key, p)}')
    print('\n')

    ''' Задание 4.9'''
    print(f'Задание 4.9')
    p = 901679
    g = 7
    pub_key = 386434
    t0 = time.perf_counter()
    priv_key = acrypt.dlog(g, pub_key, p)
    t1 = time.perf_counter()
    print(f'Shanks method: priv key = {priv_key}, time: {t1 - t0}')
    print(f'pub key -> {pow(g, priv_key, p)}')
    print('\n')

    ''' Задание 4.8'''
    print(f'Задание 4.8')
    p, g = acrypt.find_p_g(22)
    t0 = time.perf_counter()
    a = pow(g, p - 2, p)
    t1 = time.perf_counter()
    print('{}^{} mod {}={} за время {}'.format(g, p - 2, p, a, t1 - t0))
    print('\n')

    ''' Задание 4.10'''
    print(f'Задание 4.10')
    print(f'Протокол Диффи-Хеллмана')
    p, g = acrypt.find_p_g(150)
    print(
        f'Алиса и Боб договорились использовать 150 битовое простое число p = {p}\nи первообразный корень мультипликативной группы по модулю p -> g = {g} ')
    a = random.randint(2, p - 2)
    print(f'Алиса выбирает a = {a}')
    b = random.randint(2, p - 2)
    print(f'Боб выбирает b = {b}')
    A = pow(g, a, p)
    print(f'Алиса вычисляет A = {A} и передаёт Бобу')
    B = pow(g, b, p)
    print(f'Боб вычисляет B = {B} и передаёт Алисе')
    k1 = pow(B, a, p)
    print(f'Алиса вычисляет k = {k1}')
    k2 = pow(A, b, p)
    print(f'Боб вычисляет k = {k2}')
    print('\n')

    ''' Задание 4.11'''
    print(f'Задание 4.11')
    print(f'Протокол шифра Шамира')
    p = acrypt.find_p_2q_plus_1(50)
    fi_p = p - 1
    print(f'Алиса и Боб договорились использовать 50 битовое простое число p = {p}')

    while True:
        c_A = random.randint(2, fi_p - 1)
        if acrypt.extended_gcd(c_A, fi_p)[0] == 1:
            break
    d_A = acrypt.inverse_el(c_A, fi_p)
    print(f'Алиса выбирает \tc_A = {c_A}, d_A = {d_A}')
    # print(f'(c_A * d_A) % fi_p = {(c_A * d_A) % fi_p}')

    while True:
        c_B = random.randint(2, fi_p - 1)
        if acrypt.extended_gcd(c_B, fi_p)[0] == 1:
            break
    d_B = acrypt.inverse_el(c_B, fi_p)
    print(f'Боб выбирает \t\tc_B = {c_B}, d_B = {d_B}')
    # print(f'(c_B * d_B) % fi_p = {(c_B * d_B) % fi_p}')

    m = 15
    print(f'Алиса хочет передать m = {m}')
    x = pow(m, c_A, p)
    print(f'Алиса вычисляет x = {x} и передаёт Бобу')

    y = pow(x, c_B, p)
    print(f'Боб вычисляет y = {y} и передаёт Алисе')

    z = pow(y, d_A, p)
    print(f'Алиса вычисляет z = {z} и передаёт Бобу')

    m_ = pow(z, d_B, p)
    print(f'Боб вычисляет m_ = {m_}')
    print('\n')

######################################################
    ''' Задание 4.12'''
    print(f'Задание 4.12')
    print(f'Протокол шифра Шамира')
    ms = 'Фёдор Фёдорович Фёдоров'
    ms_bytes = ms.encode('utf-8')
    # ms = 'Arbiten!!!!!'
    length_ms = len(ms_bytes)
    m_arr = acrypt.dat2IntNums(ms_bytes, length_ms)
    m = m_arr[0]
    print(f'Передаваемое сообщение: {ms}, \nm = {m}')

    bitfield_width = math.floor(math.log2(m)) + 2
    p = acrypt.find_p_2q_plus_1(bitfield_width)
    fi_p = p - 1
    print(f'Алиса и Боб договорились использовать {bitfield_width} битовое простое число p = {p}')

    while True:
        c_A = random.randint(2, fi_p - 1)
        if acrypt.extended_gcd(c_A, fi_p)[0] == 1:
            break
    d_A = acrypt.inverse_el(c_A, fi_p)
    print(f'Алиса выбирает \tc_A = {c_A}, d_A = {d_A}')
    # print(f'(c_A * d_A) % fi_p = {(c_A * d_A) % fi_p}')

    while True:
        c_B = random.randint(2, fi_p - 1)
        if acrypt.extended_gcd(c_B, fi_p)[0] == 1:
            break
    d_B = acrypt.inverse_el(c_B, fi_p)
    print(f'Боб выбирает \t\tc_B = {c_B}, d_B = {d_B}')
    # print(f'(c_B * d_B) % fi_p = {(c_B * d_B) % fi_p}')

    print(f'Алиса хочет передать m = {m}')
    x = pow(m, c_A, p)
    print(f'Алиса вычисляет x = {x} и передаёт Бобу')

    y = pow(x, c_B, p)
    print(f'Боб вычисляет y = {y} и передаёт Алисе')

    z = pow(y, d_A, p)
    print(f'Алиса вычисляет z = {z} и передаёт Бобу')

    m_ = pow(z, d_B, p)
    print(f'Боб вычисляет m_ = {m_}')

    recovered_bytes = bytes(acrypt.IntNums2dat([m_], length_ms, length_ms))
    print(acrypt.IntNums2dat([m_], length_ms, length_ms))
    ms_ = recovered_bytes.decode('utf-8')
    print(f'Боб расшифровал сообщение: {ms_}')
    print('\n')

    ''' Задание 5.1'''
    print(f'Задание 5.1')
    data = read_write_file.read_data_1byte(Path('resources', '8', 'text.txt'))
    length = len(data)
    block_size = 3
    print('message is : {}'.format(data))
    nums = acrypt.dat2IntNums(data, block_size)
    priv_key = 4356
    pub_key, p, encrypt_nums = acrypt.elgamal_encrypt(nums, priv_key)
    read_write_file.write_numbers(Path('resources', '8', 'encrypt_file.txt'), encrypt_nums)

    decrypt_data = acrypt.elgamal_decrypt(encrypt_nums, priv_key, p)
    print(f'nums = {nums}')
    print(f'decrypt data = {decrypt_data}')
    recovered_data = acrypt.IntNums2dat(decrypt_data, length, block_size)
    read_write_file.write_data_1byte(Path('resources', '8', 'decrypt_file.txt'), recovered_data)
    print("recovered data = ", recovered_data)
    print('\n')

    ''' Задание 5.2'''
    print(f'Задание 5.2')
    p = 9887455967
    # g = 5
    # pub_key = 3359661584
    priv_key = 543
    block_size = 4
    message_length = 24776

    raw_encrypted_data = read_write_file.read_data_1byte(Path('resources', '8', 'b4_ElG_c.png'))
    encrypt_nums = parse_encrypted_data(raw_encrypted_data)

    decrypted_nums = acrypt.elgamal_decrypt_without2arrays(encrypt_nums, priv_key, p)
    recovered_data = acrypt.IntNums2dat(decrypted_nums, message_length, block_size)

    output_path = Path('resources', '8', 'dec_b4_ElG_c.png')
    read_write_file.write_data_1byte(output_path, recovered_data)
    print(f"Файл успешно расшифрован и сохранён в {output_path}")
    print('\n')

    ''' Задание 5.3'''
    print(f'Задание 5.3')
    p = pow(2, 31) - 1
    g = 7
    pub_key = 833287206
    c1 = 1457850878
    c2 = 2110264777

    priv_key = discrete_log(p, pub_key, g)
    print(f'a = {priv_key}')

    m = acrypt.elgamal_decrypt_element(priv_key, p, c1, c2)
    print(f'm = {m}')
    print('\n')

    ''' Задание 5.4'''
    print(f'Задание 5.4')
    p = 42872085028600815685899302367146749920403071157571857811961258220079
    # g = 17
    priv_key = 7608566734640113926049241095953347821765109080939503038867986728182
    block_size = 28
    message_length = 28
    c1 = 9993855169559627290785990688705841570114656880026382687658675476757
    c2 = 21825170162147362019183963692601304583442479734446937458746973254460

    decrypt_data = acrypt.elgamal_decrypt_element(priv_key, p, c1, c2)
    print(f'decrypt data = {decrypt_data}')
    recovered_bytes = bytes(acrypt.IntNums2dat([decrypt_data], message_length, block_size))
    recovered_string = recovered_bytes.decode('utf-8')
    print("recovered data = ", recovered_string)
    print('\n')

    ''' Задание 5.5'''
    print(f'Задание 5.5')
    p = 20598563
    g = 2
    pub_key = 12762739
    block_size = 3
    message_length = 1849

    priv_key = discrete_log(p, pub_key, g)
    print(f'a = {priv_key}')

    raw_encrypted_data = read_write_file.read_data_1byte(Path('resources', '8', 't24_ElG_c.txt'))
    encrypt_nums = parse_encrypted_data(raw_encrypted_data)

    decrypted_nums = acrypt.elgamal_decrypt_without2arrays(encrypt_nums, priv_key, p)
    recovered_data = acrypt.IntNums2dat(decrypted_nums, message_length, block_size)

    output_path = Path('resources', '8', 'dec_t24_ElG_c.txt')
    read_write_file.write_data_1byte(output_path, recovered_data)
    print(f"Файл успешно расшифрован и сохранён в {output_path}")
    print('\n')
