from read_write_file import read_data_2byte as read2b
from read_write_file import write_data_2byte as write2b

import sys, os

from pathlib import Path
from saes import SAes

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


def find_inv_matrix(matrix, mod, n):
    for i in range(0, 16):
        for j in range(0, 16):
            for k in range(0, 16):
                for l in range(0, 16):
                    # a = matrix[0][0] * i + matrix[0][1] * k
                    # b = matrix[0][0] * j + matrix[0][1] * l
                    # c = matrix[1][0] * i + matrix[1][1] * k
                    # d = matrix[1][0] * j + matrix[1][1] * l
                    a = gf_multiply_modular(matrix[0][0], i, mod, n) ^ gf_multiply_modular(matrix[0][1], k, mod, n)
                    b = gf_multiply_modular(matrix[0][0], j, mod, n) ^ gf_multiply_modular(matrix[0][1], l, mod, n)
                    c = gf_multiply_modular(matrix[1][0], i, mod, n) ^ gf_multiply_modular(matrix[1][1], k, mod, n)
                    d = gf_multiply_modular(matrix[1][0], j, mod, n) ^ gf_multiply_modular(matrix[1][1], l, mod, n)
                    if a == 1 and b == 0 and c == 0 and d == 1:
                        return [[i, j], [k, l]]


def rcon(cnt, mod, n):
    x = 2 ** (cnt + 2)
    if cnt == 1:
        return x * (2 ** n)
    elif cnt == 2:
        return 0b00110000
    else:
        return -1


def subNib(w):
    subNib = [[0x9, 0x4, 0xA, 0xB],
              [0xD, 0x1, 0x8, 0x5],
              [0x6, 0x2, 0x0, 0x3],
              [0xC, 0xE, 0xF, 0x7]]

    mask4 = 2 ** 4 - 1
    second = w & mask4
    first = w // 16

    mask2 = 3
    first_first = first // 4
    first_second = first & mask2
    second_first = second // 4
    second_second = second & mask2

    first = subNib[first_first][first_second]
    second = subNib[second_first][second_second]

    res = second + first * 16

    return res


def rotNib(w):
    mask = 2 ** 4 - 1
    second = w & mask
    first = w // 16
    res = second * 16 + first
    return res


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


def subNibTmp(w):
    subNib = [[0x9, 0x4, 0xA, 0xB],
              [0xD, 0x1, 0x8, 0x5],
              [0x6, 0x2, 0x0, 0x3],
              [0xC, 0xE, 0xF, 0x7]]
    mask2 = 3
    first_first = w // 4
    first_second = w & mask2
    return subNib[first_first][first_second]


def subNibToMatrix(matrix):
    a = subNibTmp(matrix[0][0])
    b = subNibTmp(matrix[0][1])
    c = subNibTmp(matrix[1][0])
    d = subNibTmp(matrix[1][1])

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


def invSubNibTmp(w):
    invSubNib = [[0xA, 0x5, 0x9, 0xB],
                 [0x1, 0x7, 0x8, 0xF],
                 [0x6, 0x0, 0x2, 0x3],
                 [0xC, 0x4, 0xD, 0xE]]
    mask2 = 3
    first_first = w // 4
    first_second = w & mask2
    return invSubNib[first_first][first_second]


def invSubNibToMatrix(matrix):
    a = invSubNibTmp(matrix[0][0])
    b = invSubNibTmp(matrix[0][1])
    c = invSubNibTmp(matrix[1][0])
    d = invSubNibTmp(matrix[1][1])

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
    w0 = key // (2 ** 8)
    w1 = key & 0b1111_1111

    w2 = w0 ^ rcon(1, mod, n) ^ subNib(rotNib(w1))
    w3 = w2 ^ w1

    w4 = w2 ^ rcon(2, mod, n) ^ subNib(rotNib(w3))
    w5 = w4 ^ w3

    k2 = w2 * (2 ** 8) + w3
    k1 = w4 * (2 ** 8) + w5

    matrix1 = addKeyToMatrix(splitStrToMatrix(data), key)
    matrix1 = subNibToMatrix(matrix1)
    matrix1 = swapEl(matrix1)
    matrix1 = multiMatrix(mixMatrix, matrix1, mod, n)

    matrix2 = addKeyToMatrix(matrix1, k1)
    matrix2 = subNibToMatrix(matrix2)
    matrix2 = swapEl(matrix2)

    return joinMatrixToStr(addKeyToMatrix(matrix2, k2))


def decrypt2b(data, key, mod, n, mixMatrix):
    w0 = key // (2 ** 8)
    w1 = key & 0b1111_1111

    w2 = w0 ^ rcon(1, mod, n) ^ subNib(rotNib(w1))
    w3 = w2 ^ w1

    w4 = w2 ^ rcon(2, mod, n) ^ subNib(rotNib(w3))
    w5 = w4 ^ w3

    k1 = w2 * (2 ** 8) + w3
    k2 = w4 * (2 ** 8) + w5

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
    inv_matrix = find_inv_matrix(matrix, mod, n)
    data = read2b(Path('resources', '6', 'dd1_saes_c_all.bmp'))
    dec_data = []

    for d in data:
        dec = decrypt2b(d, 834, mod, n, inv_matrix)
        dec_data.append(dec)

    write2b(Path('resources', '6', 'dd1_saes_c_all_dec.bmp'), dec_data)
    return


def task2():
    mod = 0b10011
    n = 4
    matrix = [[0xB, 0x4], [0xE, 0xD]]
    inv_matrix = find_inv_matrix(matrix, mod, n)
    data = read2b(Path('resources', '6', 'im43_saes_c_all.bmp'))
    dec_data = []

    for d in data:
        dec = decrypt2b(d, 2318, mod, n, inv_matrix)
        dec_data.append(dec)

    write2b(Path('resources', '6', 'im43_saes_c_all_dec.bmp'), dec_data)
    return

def task3():
    matrix22 = [[0xA, 0xC], [0x8, 0x6]]
    mod = 0b11001
    inv_matrix = find_inv_matrix(matrix22, mod, 4)
    IV = 456
    data = read2b(Path('resources', '6', 'dd5_saes_cbc_c_all.bmp'))
    dec_data = []
    for d in data:
        dec = decrypt2b(d, 1021, mod, 4, inv_matrix)
        dec_data.append(dec ^ IV)
        IV = d

    write2b(Path('resources', '6', 'dd5_saes_cbc_c_all_dec.bmp'), dec_data)
    return

def task4():
    matrix = list([['5', '3'], ['2', 'c']])
    mod = int('11001', 2)
    key = 12345
    saes = SAes(matrix, mod)
    data = read2b(Path('resources', '6', 'dd8_saes_ofb_c_all.bmp'))
    dec_data = []
    IV = 5171
    k0, k1, k2 = saes.key_expansion(key)
    for d in data:
        IV = saes.encrypt(IV, k0, k1, k2)
        dec_data.append(IV ^ d)

    write2b(Path('resources', '6', 'dd8_saes_ofb_c_all_dec.bmp'), dec_data)
    return

def task6():
    matrix = list([['7', 'd'], ['4', '5']])
    mod = int('11001', 2)
    key = 24545
    IV = 9165
    saes = SAes(matrix, mod)
    data = read2b(Path('resources', '6', 'dd10_saes_cfb_c_all.bmp'))
    dec_data = []
    k0, k1, k2 = saes.key_expansion(key)

    for d in data:
        dec = saes.encrypt(IV, k0, k1, k2)
        dec_data.append(dec ^ d)
        IV = d

    write2b(Path('resources', '6', 'dd10_saes_cfb_c_all_dec.bmp'), dec_data)
    return

def task7():
    matrix = list([['7', '3'], ['2', 'e']])
    mod = int('10011', 2)
    key = 2645
    iv = 23184
    data = read2b(Path('resources', '6', 'dd12_saes_ctr_c_all.bmp'))
    dec_data = []
    saes = SAes(matrix, mod)
    counter = 0
    k0, k1, k2 = saes.key_expansion(key)

    for d in data:
        a = saes.encrypt(iv, k0, k1, k2)

        iv += 1
        dec_data.append(a ^ d)

    write2b(Path('resources', '6', 'dd12_saes_ctr_c_all_dec.bmp'), dec_data)
    return

if __name__ == '__main__':

    # task1()
    # task2()
    # task3()
    # task4()
    # task6()
    task7()

    # res = find_inv_matrix(matrix, 0b10011, 4)
    # res2 = rcon(1, 0b10011, 4)
    # print(res)
    # print(res2)
    # res3 = rotNib(0b00111011)
    # print(bin(res3))
    # res4 = subNib(0b10110011)
    # print(bin(res4))
    # res5 = splitStrToMatrix(0b0110111101101011)
    # print(res5)
    # res6 = subNibToMatrix(res5)
    # print(res6)
    # res7 = swapEl(res6)
    # print(res7)
    # res8 = multiMatrix([[1, 4], [4, 1]], [[0xC, 0x1], [0x9, 0x6]], 0b10011, 4)
    # print(res8)

    # inv_matrix = find_inv_matrix(matrix,mod,n)
    # res9 = encrypt2b(0b0110111101101011, 0b1010011100111011, mod, n, matrix)
    # print(bin(res9))
    # res10 = decrypt2b(0b0000011100111000, 0b1010011100111011, mod, n, inv_matrix)
    # print(bin(res10))


# data = read2b(Path('resources', '6', 'd5_spn_c_all.bmp'))
    # write2b(Path('resources', '4', 'ex8_decrypt.bmp'), [])
    # write2b(Path('resources', '4', 'ex8_50.bmp'), decrypt_data[:50] + data[50:])
