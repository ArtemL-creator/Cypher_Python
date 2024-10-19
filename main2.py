from pathlib import Path

import numpy as np

import hill
import read_write_file


def task1():
    ''' Задание 1'''
    data = read_write_file.read_data_1byte(Path('resources', '2', 'im3_hill_c_all.bmp'))
    k = ([[189, 58], [21, 151]])
    k_ = hill.inverted_k(k, 256)
    decrypt_data = hill.decrypt_data(data, k_, 256)
    read_write_file.write_data_1byte(Path('resources', '2', 'im3_hill_c_all_decrypt.bmp'), decrypt_data)
    print("Task 2 completed")


def task2():
    ''' Задание 2'''
    data = read_write_file.read_data_1byte(Path('resources', '2', 'm18_hill_c_all.bmp'))
    k = ([[47, 239], [119, 108]])
    k_ = hill.inverted_k(k, 256)
    decrypt_data = hill.decrypt_data(data, k_, 256)
    read_write_file.write_data_1byte(Path('resources', '2', 'm18_hill_c_all_decrypt.bmp'), decrypt_data)
    data[0:50] = decrypt_data[0:50]
    read_write_file.write_data_1byte(Path('resources', '2', 'm18_hill_c_all_decrypt_encrypt.bmp'), data)
    print("Task 2 completed")


def task3():
    ''' Задание 3'''
    data = read_write_file.read_data_1byte(Path('resources', '2', 'p1_hill_c_all.png'))
    m = [[137, 78], [80, 71]]
    c = [[data[0], data[2]], [data[1], data[3]]]
    k = np.dot(c, hill.inverted_k(m, 256)) % 256
    decrypt_data = hill.decrypt_data(data, hill.inverted_k(k, 256), 256)
    read_write_file.write_data_1byte(Path('resources', '2', 'p1_hill_c_all_decrypt.png'), decrypt_data)
    print("Task 3 completed")


def task4():
    ''' Задание 4'''
    data = read_write_file.read_data_1byte(Path('resources', '2', 'b4_hill_c_all.png'))
    m = [[137, 78], [80, 71]]
    c = [[data[0], data[2]], [data[1], data[3]]]
    k = np.dot(c, hill.inverted_k(m, 256)) % 256
    decrypt_data = hill.decrypt_data(data, hill.inverted_k(k, 256), 256)
    read_write_file.write_data_1byte(Path('resources', '2', 'b4_hill_c_all_decrypt.png'), decrypt_data)
    print("Task 4 completed")


def task5():
    ''' Задание 5'''
    data = read_write_file.read_data_1byte(Path('resources', '2', 'text2_hill_c_all.txt'))
    m = [[87, 111], [104, 115]]
    c = [[data[0], data[2]], [data[1], data[3]]]
    k = np.dot(c, hill.inverted_k(m, 256)) % 256
    decrypt_data = hill.decrypt_data(data, hill.inverted_k(k, 256), 256)
    read_write_file.write_data_1byte(Path('resources', '2', 'text2_hill_c_all_decrypt.txt'), decrypt_data)
    print("Task 5 completed")


if __name__ == '__main__':
    task1()
    task2()
    task3()
    task4()
    task5()

