import Affine_cipher
import numpy as np
import hill
import read_write_file


def task1():
    ''' Задание 1'''
    data = read_write_file.read_data_1byte('im3_hill_c_all.bmp')
    k = ([[189, 58], [21, 151]])
    k_ = hill.inverted_k(k, 256)
    decrypt_data = hill.decrypt_data(data, k_, 256)
    read_write_file.write_data_1byte('im3_hill_c_all_decrypt.bmp', decrypt_data)
    print("Task 1 completed")


def task2():
    ''' Задание 2'''
    data = read_write_file.read_data_1byte('m18_hill_c_all.bmp')
    k = ([[47, 239], [119, 108]])
    k_ = hill.inverted_k(k, 256)
    decrypt_data = hill.decrypt_data(data, k_, 256)
    read_write_file.write_data_1byte('m18_hill_c_all_decrypt.bmp', decrypt_data)
    data[0:50] = decrypt_data[0:50]
    read_write_file.write_data_1byte('m18_hill_c_all_decrypt_encrypt.bmp', data)
    print("Task 2 completed")


def task3():
    ''' Задание 3'''
    data = read_write_file.read_data_1byte('p1_hill_c_all.png')
    count_keys = 0
    is_PNG = False
    for a in range(256):
        if Affine_cipher.gcd(a, 256) == 1:
            for b in range(256):
                count_keys += 1
                decrypt_data = hill.decrypt_data(data[:2], a, b)
                is_PNG = decrypt_data[0] == 0x89 and decrypt_data[1] == 0x50
                if is_PNG:
                    print('k =', count_keys)
                    print('a =', a)
                    print('b =', b)
                    decrypt_data = hill.decrypt_data(data, a, b)
                    read_write_file.write_data_1byte('p1_hill_c_all_decrypt.png', decrypt_data)
                    break
        if is_PNG:
            break
    print("Task 3 completed")

def task4():
    ''' Задание 4'''
    data = read_write_file.read_data_1byte('b4_hill_c_all.png')
    m = [[137, 78], [80, 71]]
    c = [[data[0], data[2]], [data[1], data[3]]]
    k = np.dot(c, hill.inverted_k(m, 256)) % 256
    decrypt_data = hill.decrypt_data(data, hill.inverted_k(k, 256), 256)
    read_write_file.write_data_1byte('b4_hill_c_all_decrypt.png', decrypt_data)
    print("Task 4 completed")


def task5():
    ''' Задание 5'''
    data = read_write_file.read_data_1byte('text2_hill_c_all.txt')
    m = [[87, 111], [104, 115]]
    c = [[data[0], data[2]], [data[1], data[3]]]
    k = np.dot(c, hill.inverted_k(m, 256)) % 256
    decrypt_data = hill.decrypt_data(data, hill.inverted_k(k, 256), 256)
    read_write_file.write_data_1byte('text2_hill_c_all_decrypt.txt', decrypt_data)
    print("Task 5 completed")


if __name__ == '__main__':
    task1()
    task2()
    task3()
    task4()
    task5()
