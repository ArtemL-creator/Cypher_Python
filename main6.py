from read_write_file import read_data_2byte as read2b
from read_write_file import write_data_2byte as write2b
from read_write_file import read_data_1byte as read1b
from read_write_file import write_data_1byte as write1b

import sys, os
import detectEnglish

from pathlib import Path


def gf_multiply_modular(a, b, mod, n):
    """
    INPUTS
    a - полином (множимое)
    b - полином (множитель)
    mod - неприводимый полином
    n - порядок неприводимого полинома
    OUTPUTS:
    product - результат перемножения двух полиномов a и b
    """
    # маска для наиболее значимого бита в слове
    msb = 2 ** (n - 1)
    # маска на все биты
    mask = 2 ** n - 1
    # r(x) = x^n mod m(x)
    r = mod ^ (2 ** n)
    product = 0  # результат умножения
    mm = 1
    for i in range(n):
        if b & mm > 0:
            # если у множителя текущий бит 1
            product ^= a
        # выполняем последовательное умножение на х
        if a & msb == 0:
            # если старший бит 0, то просто сдвигаем на 1 бит
            a <<= 1
        else:
            # если старший бит 1, то сдвиг на 1 бит
            a <<= 1
            # и сложение по модулю 2 с r(x)
            a ^= r
            # берем только n бит
            a &= mask
        # формируем маску для получения очередного бита в множителе
        mm += mm
    return product


def divide_into_two(k, n):
    """
    функция разделяет n-битовое число k на два (n/2)-битовых числа
    """
    n2 = n // 2
    mask = 2 ** n2 - 1
    l1 = (k >> n2) & mask
    l2 = k & mask

    return l1, l2


def mux(l, r, n):
    """
    # l, r - n-битовые числа
    # возвращает число (2n-битовое), являющееся конкатенацией бит этих чисел
    """
    y = 0
    y ^= r
    y ^= l << n

    return y


def sbox(value):
    SBOX_TABLE = [
        0x9, 0x4, 0xA, 0xB,
        0xD, 0x1, 0x8, 0x5,
        0x6, 0x2, 0x0, 0x3,
        0xC, 0xE, 0xF, 0x7
    ]
    return SBOX_TABLE[value]


def inv_sbox(value):
    INV_SBOX_TABLE = [
        0xA, 0x5, 0x9, 0xB,
        0x1, 0x7, 0x8, 0xF,
        0x6, 0x0, 0x2, 0x3,
        0xC, 0x4, 0xD, 0xE
    ]
    return INV_SBOX_TABLE[value]


def g(w, i, rcon1, rcon2, sbox):
    """
    g функция в алгоритме расширения ключа.
    w: входное слово (8 бит)
    i: номер раунда (1 или 2)
    """
    n00, n11 = divide_into_two(w, 8)
    n0 = sbox(n00)
    n1 = sbox(n11)
    n1n0 = mux(n1, n0, 4)
    if i == 1:
        res = n1n0 ^ rcon1
    else:
        res = n1n0 ^ rcon2
    return res


def key_expansion(key, rcon1, rcon2, sbox):
    """
    Алгоритм расширения ключа.
    """
    w0, w1 = divide_into_two(key, 16)
    w2 = w0 ^ g(w1, 1, rcon1, rcon2, sbox)
    w3 = w1 ^ w2
    w4 = w2 ^ g(w3, 2, rcon1, rcon2, sbox)
    w5 = w3 ^ w4
    return key, mux(w2, w3, 8), mux(w4, w5, 8)


def find_inv_matrix(matrix, mod, n):
    for i in range(0, 16):
        for j in range(0, 16):
            for k in range(0, 16):
                for l in range(0, 16):
                    a = gf_multiply_modular(matrix[0][0], i, mod, n) ^ gf_multiply_modular(matrix[0][1], k, mod, n)
                    b = gf_multiply_modular(matrix[0][0], j, mod, n) ^ gf_multiply_modular(matrix[0][1], l, mod, n)
                    c = gf_multiply_modular(matrix[1][0], i, mod, n) ^ gf_multiply_modular(matrix[1][1], k, mod, n)
                    d = gf_multiply_modular(matrix[1][0], j, mod, n) ^ gf_multiply_modular(matrix[1][1], l, mod, n)
                    if a == 1 and b == 0 and c == 0 and d == 1:
                        return [[i, j], [k, l]]


def rcon(cnt):
    if cnt == 1:
        return 0b10000000
    elif cnt == 2:
        return 0b00110000
    else:
        return -1


def splitStrToMatrix(w):
    mask1 = 0b1111_0000_0000_0000
    mask2 = 0b0000_1111_0000_0000
    mask3 = 0b0000_0000_1111_0000
    mask4 = 0b0000_0000_0000_1111

    a = (w & mask1) // (2 ** 12)
    b = (w & mask2) // (2 ** 8)
    c = (w & mask3) // (2 ** 4)
    d = (w & mask4)

    return [[a, c], [b, d]]


def joinMatrixToStr(matrix):
    res = 0
    res += matrix[0][0] * (2 ** 12)
    res += matrix[1][0] * (2 ** 8)
    res += matrix[0][1] * (2 ** 4)
    res += matrix[1][1]
    return res


def subNibToMatrix(matrix):
    a = sbox(matrix[0][0])
    b = sbox(matrix[0][1])
    c = sbox(matrix[1][0])
    d = sbox(matrix[1][1])

    return [[a, b], [c, d]]


def swapEl(matrix):
    return [[matrix[0][0], matrix[0][1]], [matrix[1][1], matrix[1][0]]]


def multiMatrix(matrix1, matrix2, mod, n):
    matrix = [[0, 0], [0, 0]]
    for i in range(0, 2):
        for j in range(0, 2):
            for k in range(0, 2):
                matrix[i][j] ^= gf_multiply_modular(matrix1[i][k], matrix2[k][j], mod, n)
    return matrix


def invSubNibToMatrix(matrix):
    a = inv_sbox(matrix[0][0])
    b = inv_sbox(matrix[0][1])
    c = inv_sbox(matrix[1][0])
    d = inv_sbox(matrix[1][1])

    return [[a, b], [c, d]]


def addKeyToMatrix(matrix, key):
    key1 = key // (2 ** 12)
    key2 = (key & 0b0000_1111_0000_0000) // (2 ** 8)
    key3 = (key & 0b0000_0000_1111_0000) // (2 ** 4)
    key4 = key & 0b0000_0000_0000_1111

    a = matrix[0][0] ^ key1
    b = matrix[1][0] ^ key2
    c = matrix[0][1] ^ key3
    d = matrix[1][1] ^ key4

    return [[a, c], [b, d]]


def encrypt2b(data, key, mod, n, mixMatrix):
    k0, k1, k2 = key_expansion(key, rcon(1), rcon(2), sbox)

    matrix1 = addKeyToMatrix(splitStrToMatrix(data), key)
    matrix1 = subNibToMatrix(matrix1)
    matrix1 = swapEl(matrix1)
    matrix1 = multiMatrix(mixMatrix, matrix1, mod, n)

    matrix2 = addKeyToMatrix(matrix1, k1)
    matrix2 = subNibToMatrix(matrix2)
    matrix2 = swapEl(matrix2)

    return joinMatrixToStr(addKeyToMatrix(matrix2, k2))


def decrypt2b(data, key, mod, n, mixMatrix):
    k0, k1, k2 = key_expansion(key, rcon(1), rcon(2), sbox)

    matrix1 = addKeyToMatrix(splitStrToMatrix(data), k2)
    matrix1 = swapEl(matrix1)
    matrix1 = invSubNibToMatrix(matrix1)

    matrix2 = addKeyToMatrix(matrix1, k1)
    matrix2 = multiMatrix(mixMatrix, matrix2, mod, n)
    matrix2 = swapEl(matrix2)
    matrix2 = invSubNibToMatrix(matrix2)

    return joinMatrixToStr(addKeyToMatrix(matrix2, key))


def task1():
    mod = 0b10011
    n = 4
    matrix = [[1, 4], [4, 1]]
    key = 834
    inv_matrix = find_inv_matrix(matrix, mod, n)
    data = read2b(Path('resources', '6', 'dd1_saes_c_all.bmp'))
    dec_data = []

    for d in data:
        dec = decrypt2b(d, key, mod, n, inv_matrix)
        dec_data.append(dec)

    write2b(Path('resources', '6', 'dd1_saes_c_all_dec.bmp'), dec_data)

    no_encrypt_size = 50
    encrypt_data = []
    for i in range(len(dec_data)):
        if i < no_encrypt_size:
            # Оставляем первые 50 байт без изменений
            encrypt_data.append(dec_data[i])
        else:
            # Для оставшихся байтов шифруем в режиме ECB
            encrypted_block = encrypt2b(dec_data[i], key, mod, 4, matrix)
            encrypt_data.append(encrypted_block)

    write2b(Path('resources', '6', 'dd1_saes_c_all_dec_re_encrypted.bmp'), encrypt_data)
    return


def task2():
    mod = 0b10011
    n = 4
    key = 2318
    matrix = [[0xB, 0x4], [0xE, 0xD]]
    inv_matrix = find_inv_matrix(matrix, mod, n)
    data = read2b(Path('resources', '6', 'im43_saes_c_all.bmp'))
    dec_data = []

    for d in data:
        dec = decrypt2b(d, key, mod, n, inv_matrix)
        dec_data.append(dec)

    write2b(Path('resources', '6', 'im43_saes_c_all_dec.bmp'), dec_data)

    no_encrypt_size = 50
    encrypt_data = []

    for i in range(len(dec_data)):
        if i < no_encrypt_size:
            # Оставляем первые 50 байт без изменений
            encrypt_data.append(dec_data[i])
        else:
            # Для оставшихся байтов шифруем в режиме ECB
            encrypted_block = encrypt2b(dec_data[i], key, mod, 4, matrix)
            encrypt_data.append(encrypted_block)

    write2b(Path('resources', '6', 'im43_saes_c_all_dec_re_encrypted.bmp'), encrypt_data)
    return


def task3():
    matrix22 = [[0xA, 0xC], [0x8, 0x6]]
    mod = 0b11001
    inv_matrix = find_inv_matrix(matrix22, mod, 4)
    IV = 456
    key = 1021
    data = read2b(Path('resources', '6', 'dd5_saes_cbc_c_all.bmp'))
    dec_data = []
    for d in data:
        dec = decrypt2b(d, key, mod, 4, inv_matrix)
        dec_data.append(dec ^ IV)
        IV = d

    write2b(Path('resources', '6', 'dd5_saes_cbc_c_all_dec.bmp'), dec_data)

    no_encrypt_size = 50
    encrypt_data = []

    for i in range(len(dec_data)):
        if i < no_encrypt_size:
            # Оставляем первые 50 байт без изменений
            encrypt_data.append(dec_data[i])
        else:
            # Для оставшихся байтов шифруем в режиме CBC
            current_byte = dec_data[i]
            previous_block = encrypt_data[-1] if len(encrypt_data) > 0 else IV
            encrypted_block = encrypt2b(previous_block, key, mod, 4, matrix22)
            encrypt_data.append(encrypted_block ^ current_byte)

    write2b(Path('resources', '6', 'dd5_saes_cbc_c_all_dec_re_encrypted.bmp'), encrypt_data)
    return


def task4():
    matrix = [[5, 3], [2, 12]]
    mod = int('11001', 2)
    key = 12345
    IV = 5171

    data = read2b(Path('resources', '6', 'dd8_saes_ofb_c_all.bmp'))
    dec_data = []

    for d in data:
        IV = encrypt2b(IV, key, mod, 4, matrix)
        dec_data.append(IV ^ d)

    write2b(Path('resources', '6', 'dd8_saes_ofb_c_all_dec.bmp'), dec_data)

    no_encrypt_size = 50
    encrypt_data = []

    for i in range(len(dec_data)):
        if i < no_encrypt_size:
            # Оставляем первые 50 байт без изменений
            encrypt_data.append(dec_data[i])
        else:
            # Для оставшихся байтов шифруем в режиме OFB
            current_IV = IV
            encrypted_IV = encrypt2b(current_IV, key, mod, 4, matrix)
            encrypted_block = encrypted_IV ^ dec_data[i]
            encrypt_data.append(encrypted_block)

            IV = encrypted_IV

    write2b(Path('resources', '6', 'dd8_saes_ofb_c_all_dec_re_encrypted.bmp'), encrypt_data)
    return


def task5():
    matrix = [[3, 8], [2, 11]]
    mod = int('10011', 2)
    partial_key = int('011110110', 2)
    iv = 3523

    data = read1b(Path('resources', '6', 't20_saes_ofb_c_all.txt'))

    k = 0
    while True:
        # Формируем полный ключ из текущего значения k и известных младших битов
        key = (k << 9) | partial_key

        dec_data = []
        current_iv = iv

        for d in data:
            current_iv = encrypt2b(current_iv, key, mod, 4, matrix)
            dec_byte = (current_iv ^ d) & 0xFF  # Ограничиваем до 1 байта
            dec_data.append(dec_byte)

        # Преобразуем расшифрованные данные в текст
        try:
            txt = ''.join(chr(b) for b in dec_data)
        except ValueError:
            txt = ''.join(chr(b) if 0 <= b <= 255 else '?' for b in dec_data)

        print(f"Trying key: {key} (k={k})")
        print(f"Decrypted text: {txt[:50]}")

        if detectEnglish.isEnglish(txt):
            print(f"Found key: {key} (k={k})")
            write1b(Path('resources', '6', 't20_saes_ofb_c_all_dec.txt'), dec_data)
            break

        k += 1

        if k >= 128:
            print("Ключ не найден")
            break
    return


def task6():
    matrix = [[7, 13], [4, 5]]
    mod = int('11001', 2)
    key = 24545
    IV = 9165

    data = read2b(Path('resources', '6', 'dd10_saes_cfb_c_all.bmp'))
    dec_data = []

    for d in data:
        dec = encrypt2b(IV, key, mod, 4, matrix)
        dec_data.append(dec ^ d)
        IV = d

    write2b(Path('resources', '6', 'dd10_saes_cfb_c_all_dec.bmp'), dec_data)

    no_encrypt_size = 50
    encrypt_data = []

    for i in range(len(dec_data)):
        if i < no_encrypt_size:
            # Оставляем первые 50 байт без изменений
            encrypt_data.append(dec_data[i])
        else:
            # Для оставшихся байтов шифруем в режиме CFB
            current_IV = IV
            encrypted_IV = encrypt2b(current_IV, key, mod, 4, matrix)
            encrypted_block = encrypted_IV ^ dec_data[i]
            encrypt_data.append(encrypted_block)

            IV = encrypted_IV

    write2b(Path('resources', '6', 'dd10_saes_cfb_c_all_dec_re_encrypted.bmp'), encrypt_data)
    return


def task7():
    matrix = [[7, 3], [2, 14]]
    mod = int('10011', 2)
    key = 2645
    IV = 23184

    data = read2b(Path('resources', '6', 'dd12_saes_ctr_c_all.bmp'))
    dec_data = []

    for d in data:
        a = encrypt2b(IV, key, mod, 4, matrix)
        IV += 1
        dec_data.append(a ^ d)

    write2b(Path('resources', '6', 'dd12_saes_ctr_c_all_dec.bmp'), dec_data)

    no_encrypt_size = 50
    encrypt_data = []

    for i in range(len(dec_data)):
        if i < no_encrypt_size:
            # Оставляем первые 50 байт без изменений
            encrypt_data.append(dec_data[i])
        else:
            # Для оставшихся байтов шифруем в режиме CTR
            current_IV = IV
            encrypted_IV = encrypt2b(current_IV, key, mod, 4, matrix)
            encrypted_block = encrypted_IV ^ dec_data[i]
            encrypt_data.append(encrypted_block)

            IV += 1

    write2b(Path('resources', '6', 'dd12_saes_ctr_c_all_dec_re_encrypted.bmp'), encrypt_data)
    return


if __name__ == '__main__':
    print('\n')
    # task1()
    # task2()
    # task3()
    # task4()
    # task5()
    # task6()
    # task7()
