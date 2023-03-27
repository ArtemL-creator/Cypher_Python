from pathlib import Path

import read_write_file
import Encryption_modes
import Caesar


def task1():
    ''' Задание 1'''
    data = read_write_file.read_data_1byte(Path('resources', '3', 'z1_caesar_cbc_c_all.bmp'))
    decrypt_data = Encryption_modes.decrypt_CBC(data, 223, 59)
    read_write_file.write_data_1byte(Path('resources', '3', 'z1_caesar_cbc_c_all_decrypt.bmp'), decrypt_data)
    data[0:50] = decrypt_data[0:50]
    read_write_file.write_data_1byte(Path('resources', '3', 'z1_caesar_cbc_c_all_decrypt_encrypt.bmp'), data)
    data2 = decrypt_data
    encrypt_data2 = Caesar.encrypt_data(data2, 223)
    encrypt_data2[0:50] = decrypt_data[0:50]
    read_write_file.write_data_1byte(Path('resources', '3', 'z1_caesar_cbc_c_all_decrypt_encrypt_ECB.bmp'),
                                     encrypt_data2)
    print("Task 1 completed")


def task2():
    ''' Задание 2'''
    data = read_write_file.read_data_1byte(Path('resources', '3', 'im8_caesar_ofb_c_all.bmp'))
    decrypt_data = Encryption_modes.decrypt_OFB(data, 56, 9)
    read_write_file.write_data_1byte(Path('resources', '3', 'im8_caesar_ofb_c_all_decrypt.bmp'), decrypt_data)
    data[0:50] = decrypt_data[0:50]
    read_write_file.write_data_1byte(Path('resources', '3', 'im8_caesar_ofb_c_all_decrypt_encrypt.bmp'), data)
    data2 = decrypt_data
    encrypt_data2 = Caesar.encrypt_data(data2, 56)
    encrypt_data2[0:50] = decrypt_data[0:50]
    read_write_file.write_data_1byte(Path('resources', '3', 'im8_caesar_ofb_c_all_decrypt_encrypt_ECB.bmp'),
                                     encrypt_data2)
    print("Task 2 completed")


def task3():
    ''' Задание 3'''
    data = read_write_file.read_data_1byte(Path('resources', '3', 'z2_caesar_cfb_c_all.bmp'))
    decrypt_data = Encryption_modes.decrypt_CFB(data, 174, 9)
    read_write_file.write_data_1byte(Path('resources', '3', 'z2_caesar_cfb_c_all_decrypt.bmp'), decrypt_data)
    data[0:50] = decrypt_data[0:50]
    read_write_file.write_data_1byte(Path('resources', '3', 'z2_caesar_cfb_c_all_decrypt_encrypt.bmp'), data)
    data2 = decrypt_data
    encrypt_data2 = Caesar.encrypt_data(data2, 174)
    encrypt_data2[0:50] = decrypt_data[0:50]
    read_write_file.write_data_1byte(Path('resources', '3', 'z2_caesar_cfb_c_all_decrypt_encrypt_ECB.bmp'),
                                     encrypt_data2)
    print("Task 3 completed")


def task4():
    ''' Задание 4'''
    data = read_write_file.read_data_1byte(Path('resources', '3', 'z3_caesar_ctr_c_all.bmp'))
    decrypt_data = Encryption_modes.decrypt_CTR(data, 223, 78)
    read_write_file.write_data_1byte(Path('resources', '3', 'z3_caesar_ctr_c_all_decrypt.bmp'), decrypt_data)
    data[0:50] = decrypt_data[0:50]
    read_write_file.write_data_1byte(Path('resources', '3', 'z3_caesar_ctr_c_all_decrypt_encrypt.bmp'), data)
    print("Task 4 completed")
    data2 = decrypt_data
    encrypt_data2 = Caesar.encrypt_data(data2, 223)
    encrypt_data2[0:50] = decrypt_data[0:50]
    read_write_file.write_data_1byte(Path('resources', '3', 'z3_caesar_ctr_c_all_decrypt_encrypt_ECB.bmp'),
                                     encrypt_data2)


if __name__ == '__main__':
    task4()
