from read_write_file import read_data_2byte as read2b
from read_write_file import write_data_2byte as write2b

import sys, os

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
    msb = 2**(n - 1)
    # маска на все биты
    mask = 2**n - 1
    # r(x) = x^n mod m(x)
    r = mod ^ (2**n)
    product = 0 # результат умножения
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
    x = 2**(cnt + 2)
    if cnt == 1:
        return x * (2**n)
    elif cnt == 2:
        mask = 2 ** n - 1
        return (mod & mask) * (2**n)
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
    mask = 2**4 - 1
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
    subNib = [[0x9, 0x4, 0xA, 0xB],
              [0xD, 0x1, 0x8, 0x5],
              [0x6, 0x2, 0x0, 0x3],
              [0xC, 0xE, 0xF, 0x7]]


    a = subNibTmp(matrix[0][0])
    b = subNibTmp(matrix[0][1])
    c = subNibTmp(matrix[1][0])
    d = subNibTmp(matrix[1][1])

    return [[a, b], [c, d]]

def swapEl(matrix):
    return [[matrix[0][0], matrix[0][1]], [matrix[1][1], matrix[1][0]]]

def multiMatrix(matrix1, matrix2, mod, n):
    matrix = [[1, 1], [1, 1]]
    for i in range(0, 2):
        for j in range(0, 2):
            
            res = gf_multiply_modular(matrix[0][0], i, mod, n) ^ gf_multiply_modular(matrix[0][1], k, mod, n)




if __name__ == '__main__':
    matrix = [[1, 4], [4, 1]]
    res = find_inv_matrix(matrix, 0b10011, 4)
    res2 = rcon(1, 0b10011, 4)
    print(res)
    print(res2)
    res3 = rotNib(0b00111011)
    print(bin(res3))
    res4 = subNib(0b10110011)
    print(bin(res4))
    res5 = splitStrToMatrix(0b0110111101101011)
    print(res5)
    res6 = subNibToMatrix(res5)
    print(res6)
    res7 = swapEl(res6)
    print(res7)

# data = read2b(Path('resources', '6', 'd5_spn_c_all.bmp'))
    # write2b(Path('resources', '4', 'ex8_decrypt.bmp'), [])
    # write2b(Path('resources', '4', 'ex8_50.bmp'), decrypt_data[:50] + data[50:])
