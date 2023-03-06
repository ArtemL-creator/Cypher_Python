import random

import Caesar
import Affine_cipher
import read_write_file
import detectEnglish


def main():
    '''
    m = 24
    key = 37
    c = Caesar.encrypt(m, key)
    print("c = ", c)
    m1 = Caesar.decrypt(c, key)
    print("m1 = ", m1)
    data = [34, 67, 123, 79, 201]
    encrypt_data = Caesar.encrypt_data(data, key)
    print("encrypt_data = ", encrypt_data)
    decrypt_data = Caesar.decrypt_data(encrypt_data, key)
    print("descrypt_data = ", decrypt_data)
    '''

    '''
    data = read_write_file.read_data_1byte("f1.txt")
    print("data = ", data[0:15])
    txt = ''.join([chr(s) for s in data[0:15]])
    print("text = ", txt)
    '''

    '''
    data = read_write_file.read_data_1byte("f1.txt")
    print("data = ", data[0:15])

    encrypt_data = Caesar.encrypt_data(data, key = 67)
    print("encrypt_data = ", encrypt_data[0:15])

    txt = ''.join([chr(s) for s in data[0:15]])
    print("encrypt_text = ", txt)

    read_write_file.write_data_1byte("f1_encrypt.txt", encrypt_data)
    '''

    '''
    encrypt_data = read_write_file.read_data_1byte("f1_encrypt.txt")
    print("encrypt_data = ", encrypt_data[0:15])

    decrypt_data = Caesar.decrypt_data(encrypt_data, key = 67)
    print("decrypt_data = ", decrypt_data[0:15])

    txt = ''.join([chr(s) for s in decrypt_data[0:15]])
    print("decrypt_text = ", txt)

    read_write_file.write_data_1byte("f1_decrypt.txt", decrypt_data)
    '''

    '''
    encrypt_data = read_write_file.read_data_1byte("f1_encrypt.txt")
    print("encrypt_data = ", encrypt_data[0:15])

    k = 0
    while True :
        decrypt_data = Caesar.decrypt_data(encrypt_data[0:15], key = k)
        txt = ''.join([chr(s) for s in decrypt_data])
        print("decrypt_text = ", txt)
        is_english = detectEnglish.isEnglish(txt)
        if is_english == True :
            break
        k = k + 1

    '''

    ''' Задание 1
    data = read_write_file.read_data_1byte('f2.png')
    encrypt_data = Caesar.encrypt_data(data, key = 143)
    read_write_file.write_data_1byte('f2_encrypt.png', encrypt_data)

    data = read_write_file.read_data_1byte('f2_encrypt.png')
    k = 0
    while True :
        decrypt_data = Caesar.encrypt_data(data, key = k)
        if decrypt_data[0] == 0x89 and decrypt_data[1] == 0x50 :
            break
        print('k = ', k)
        k += 1
    read_write_file.write_data_1byte('f2_decrypt.png', decrypt_data)
    '''

    ''' Задание 2
    encrypt_data = read_write_file.read_data_1byte("t3_caesar_c_all.txt")
    print("encrypt_data = ", encrypt_data)

    k = 0
    while True :
        decrypt_data = Caesar.decrypt_data(encrypt_data, key = k)
        txt = ''.join([chr(s) for s in decrypt_data])
        is_english = detectEnglish.isEnglish(txt)
        if is_english == True :
            break
        k = k + 1
    print("decrypt_text:\n", txt)
    '''

    ''' Задание 3.1
    data = read_write_file.read_data_1byte('c4_caesar_c_all.bmp')
    k = 0
    while True :
        decrypt_data = Caesar.decrypt_data(data, key = k)
        if decrypt_data[0] == 0x42 and decrypt_data[1] == 0x4D :
            break
        print('k = ', k)
        k += 1
    read_write_file.write_data_1byte('c4_caesar_c_all_decrypt.bmp', decrypt_data)
    '''
    ''' Задание 3.2 
    data_en = read_write_file.read_data_1byte('c4_caesar_c_all.bmp')
    data_dec = read_write_file.read_data_1byte('c4_caesar_c_all_decrypt.bmp')
    data_en[0:50] = data_dec[0:50]
    read_write_file.write_data_1byte('c4_caesar_c_all_decrypt_encrypt.bmp', data_en)
    '''

    ''' Задание 4
    k = [179, 109, 157, 182, 126, 141, 251, 220, 169, 237, 188, 131, 207, 22, 32, 242, 208, 68, 216, 170, 249, 199, 44,
         198, 206, 8, 148, 197, 136, 195, 159, 98, 175, 53, 123, 212, 233, 150, 6, 243, 38, 79, 156, 153, 2, 134, 47,
         215, 102,
         15, 57, 110, 236, 24, 184, 72, 137, 113, 171, 70, 161, 64, 252, 247, 49, 103, 105, 138, 119, 213, 87, 130, 203,
         90,
         167, 238, 231, 116, 78, 86, 173, 250, 200, 239, 178, 97, 114, 94, 166, 142, 104, 31, 75, 89, 106, 56, 128, 69,
         164, 67,
         26, 228, 61, 181, 125, 227, 54, 96, 168, 107, 17, 14, 37, 190, 219, 211, 121, 112, 35, 18, 143, 158, 193, 129,
         71, 23,
         101, 191, 41, 241, 82, 201, 223, 120, 59, 177, 58, 63, 151, 42, 36, 183, 226, 127, 172, 202, 84, 132, 3, 45,
         73, 30,
         235, 50, 189, 4, 1, 43, 221, 205, 83, 232, 46, 147, 93, 192, 124, 244, 12, 21, 80, 55, 160, 145, 245, 209, 88,
         204, 176,
         13, 253, 11, 99, 165, 140, 19, 224, 111, 27, 185, 65, 62, 16, 163, 210, 115, 217, 34, 92, 187, 152, 155, 108,
         5, 122,
         229, 174, 118, 162, 95, 100, 7, 66, 29, 230, 144, 149, 52, 9, 91, 117, 214, 76, 48, 33, 194, 254, 10, 234, 218,
         40, 133,
         196, 139, 135, 240, 60, 25, 225, 85, 255, 246, 51, 28, 146, 74, 222, 186, 39, 77, 0, 20, 180, 154, 81, 248]

    encrypt_data = read_write_file.read_data_1byte("c3_subst_c_all.png")
    decrypt_data = Caesar.decrypt_data_for_4(encrypt_data, k)
    read_write_file.write_data_1byte('c3_subst_c_all_decrypt.png', decrypt_data)
    '''

    ''' Задание 5.1
    encrypt_data = read_write_file.read_data_1byte("ff2_affine_c_all.bmp")
    a = 0
    b = 0
    k = 0
    f = False
    for a in range(255):
        if not f:
            if Affine_cipher.gcd(a, 256) == 1:
                for b in range(255):
                    decrypt_data = Affine_cipher.decrypt_data(encrypt_data, a, b)
                    if decrypt_data[0] == 0x42 and decrypt_data[1] == 0x4D:
                        f = True
                        break
                    b += 1
                    k += 1
                    print('k = ', k)
            else:
                a += 1
        else:
            break
    read_write_file.write_data_1byte('ff2_affine_c_all_decrypt.bmp', decrypt_data)
    '''

    ''' Задание 5.2
    data_en = read_write_file.read_data_1byte('ff2_affine_c_all.bmp')
    data_dec = read_write_file.read_data_1byte('ff2_affine_c_all_decrypt.bmp')
    data_en[0:50] = data_dec[0:50]
    read_write_file.write_data_1byte('ff2_affine_c_all_decrypt_encrypt.bmp', data_en)
    '''

    ''' Задание 6
    encrypt_data = read_write_file.read_data_1byte("text10_affine_c_all.txt")
    print("encrypt_data = ", encrypt_data)

    a = 0
    b = 0
    k = 0
    f = False
    for a in range(255):
        if not f:
            if Affine_cipher.gcd(a, 256) == 1:
                for b in range(255):
                    decrypt_data = Affine_cipher.decrypt_data(encrypt_data, a, b)
                    txt = ''.join([chr(s) for s in decrypt_data])
                    is_english = detectEnglish.isEnglish(txt)
                    if is_english:
                        f = True
                        break
                    b += 1
                    k += 1
                    print('k = ', k)
            else:
                a += 1
        else:
            break
    print("decrypt_text:\n", txt)
    '''

    ''' Задание 8'''
    key = 'magistr'
    encrypt_data = read_write_file.read_data_1byte("c3_subst_c_all.png")
    decrypt_data = Caesar.decrypt_data_for_4(encrypt_data, key)
    read_write_file.write_data_1byte('c3_subst_c_all_decrypt.png', decrypt_data)

if __name__ == "__main__":
    main()
