import sdes

from read_write_file import read_data_1byte as read
from read_write_file import write_data_1byte as write

import sys, os

from pathlib import Path


def task7(data=[234, 54, 135, 98, 47], key=int("0111111101", 2)):
    D = sdes.SDes()
    print(D.encrypt_data(data, key))

    print("Task 7 completed")


def task8():
    sys.stdout = open(os.devnull, 'w')
    D = sdes.SDes()
    data = read(Path('resources', '5', 'aa1_sdes_c_all.bmp'))
    decrypt_data = D.decrypt_data(data, key=645)
    write(str(Path('resources', '5', 't8.bmp')), decrypt_data)
    write(str(Path('resources', '5', 't8_50.bmp')), decrypt_data[:50] + data[50:])
    sys.stdout = sys.__stdout__

    print("Task 8 completed")


def task_OFB():
    sys.stdout = open(os.devnull, 'w')
    D = sdes.SDes()
    data = read(Path('resources', '5', 'aa3_sdes_c_ofb_all.bmp'))
    decrypt_data = D.decrypt_OFB(data, key=932, initV=234)
    write(str(Path('resources', '5', 'tOFB.bmp')), decrypt_data)
    write(str(Path('resources', '5', 'tOFB_50.bmp')), decrypt_data[:50] + data[50:])
    sys.stdout = sys.__stdout__

    print("Task completed")


if __name__ == '__main__':
    task7()
    print()
    task8()
    task_OFB()
