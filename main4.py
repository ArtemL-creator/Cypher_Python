from pathlib import Path

import spn1

from read_write_file import read_data_2byte as read2b
from read_write_file import write_data_2byte as write2b

''' Задание 1'''


def task1a():
    e = spn1.SPN1()
    x = 15324
    print('x={}'.format(bin(x)[2:].zfill(16)))
    y = e.demux(x)
    print('y={}'.format(y))

    print("Task 1a completed")


# 0011    1011    1101   1100
# x=0011101111011100
# y=[12, 13, 11, 3]

def task1b():
    e = spn1.SPN1()
    x = [9, 11, 4, 2]
    y = e.mux(x)
    print('y={}'.format(bin(y)[2:].zfill(16)))

    print("Task 1b completed")


# y=0010010010111001

''' Задание 2'''


def task2():
    data = [15324, 3453, 34, 12533]
    k = 734533245
    e = spn1.SPN1()
    cypher_data = e.encrypt_data(data, key=k, rounds=4)
    print('cypher_data={}'.format(cypher_data))

    print("Task 2 completed")


''' Задание 3'''


def task3a():
    e = spn1.SPN1()
    x = 9
    sx = e.sbox(x)
    print('x={}--->s[{}]={}'.format(x, x, sx))
    x_ = e.asbox(sx)
    print('as[{}]={}'.format(sx, x_))

    print("Task 3a completed")


def task3b():
    e = spn1.SPN1()
    x = int('0010011010110111', 2)
    px = e.pbox(x)
    print('x={}--->px={}'.format(bin(x)[2:].zfill(16), bin(px)[2:].zfill(16)))
    x_ = e.apbox(px)
    print('px={}--->x_={}'.format(bin(px)[2:].zfill(16), bin(x_)[2:].zfill(16)))

    print("Task 3b completed")


def task3c():
    x = int(bin(int(15324))[2:].zfill(16), 2)
    y = int(bin(int(24681))[2:].zfill(16), 2)
    e = spn1.SPN1()
    px = e.pbox(x ^ y)
    print('x={}--->px={}'.format(bin(x)[2:].zfill(16), bin(px)[2:].zfill(16)))
    x_ = e.apbox(x) ^ e.apbox(y)
    print('px={}--->x_={}'.format(bin(px)[2:].zfill(16), bin(x_)[2:].zfill(16)))


''' Задание 4'''


def task4(k=734533245):
    e = spn1.SPN1()
    print(e.round_keys_to_decrypt(k))
    print()
    print(e.round_keys(k))

    print("Task 4 completed")


''' Задание 5'''


def task5():
    e = spn1.SPN1()
    x = 9911
    k = 982832703
    print('x={}'.format(bin(x)[2:].zfill(16)))
    rk = e.round_keys(k)
    y = e.encrypt(x, rk, rounds=4)
    lk = e.round_keys_to_decrypt(k)
    x_ = e.decrypt(y, lk, rounds=4)
    print('y={}'.format(bin(y)[2:].zfill(16)))
    print('x_={}'.format(bin(x_)[2:].zfill(16)))

    print("Task 5 completed")


''' Задание 6'''


def task6():
    e = spn1.SPN1()
    x = [9911, 12432, 456, 21]
    k = 982832703
    print('x={}'.format(x))
    y = e.encrypt_data(x, k, rounds=4)
    x_ = e.decrypt_data(y, k, rounds=4)
    print('y={}'.format(y))
    print('x_={}'.format(x_))

    print("Task 6 completed")


''' Задание 7'''


def task7():
    e = spn1.SPN1()
    # шифрование
    data = read2b(Path('resources', '4', '123.txt'))
    cypher_data = e.encrypt_data(data, key=452342216, rounds=4)
    write2b(Path('resources', '4', '123_encrypt.txt'), cypher_data)
    # расшифрование
    data = read2b(Path('resources', '4', '123_encrypt.txt'))
    decrypt_data = e.decrypt_data(data, key=452342216, rounds=4)
    write2b(Path('resources', '4', '123_decrypt.txt'), decrypt_data)

    print("Task 7 completed")


''' Задание 8'''


def task8():
    e = spn1.SPN1()
    data = read2b(Path('resources', '4', 'd5_spn_c_all.bmp'))
    decrypt_data = e.decrypt_data(data, key=34523456231, rounds=4)
    write2b(Path('resources', '4', 'ex8_decrypt.bmp'), decrypt_data)
    write2b(Path('resources', '4', 'ex8_50.bmp'), decrypt_data[:50] + data[50:])

    print("Task 8 completed")


''' Задание 9'''


def task9():
    e = spn1.SPN1()
    data = read2b(Path('resources', '4', 'd9_spn_c_cbc_all.bmp'))
    decrypt_data = e.decrypt_cbc(data, key=345238754631, rounds=4, initV=9)
    write2b(Path('resources', '4', 'ex9_decrypt.bmp'), decrypt_data)
    write2b(Path('resources', '4', 'ex9_50.bmp'), decrypt_data[:50] + data[50:])

    print("Task 9 completed")


def task_ofb():
    e = spn1.SPN1()
    data = read2b(Path('resources', '4', 'im28_spn_c_ofb_all.bmp'))
    decrypt_data = e.decrypt_OFB(data, key=898387587921, rounds=4, initV=3253)
    write2b(Path('resources', '4', 'ex_ofb_decrypt.bmp'), decrypt_data)
    write2b(Path('resources', '4', 'ex_ofb_50.bmp'), decrypt_data[:50] + data[50:])

    print("Task completed")


if __name__ == '__main__':
    # task1a()
    # task1b()
    # task2()
    # task3a()
    # task3b()
    # task3c()
    # task4()
    # task5()
    # task6()
    # task7()
    # task8()
    # task9()
    # task_ofb()

    e = spn1.SPN1()
    # 1111 1111  1111 1111  0111 1111  1111 1111
    # 1111_1010_1010_1110

    Key = int('01111_11111', 2)
    print(Key)
    decrypt_data = e.decrypt_data(data=[int("10001111", 2)], key=Key, rounds=4)
    print(decrypt_data)
    txt = ''.join([chr(s) for s in decrypt_data])
    print('decrypt_text=', txt)
    write2b(Path('resources', '4', 'extxt.txt'), decrypt_data)
