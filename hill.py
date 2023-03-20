import numpy as np
import Affine_cipher


def encrypt(m, k, l):
    return np.dot(k, m) % l


def encrypt_data(data, k, l):
    encrypted = []
    for i in range(0, len(data), 2):
        m = data[i: i + 2]
        c = encrypt(m, k, l)
        encrypted.append(c[0])
        encrypted.append(c[1])
    return encrypted


def decrypt(c, k, l):
    return np.dot(k, c) % l


def decrypt_data(data, k, l):
    decrypted = []
    for i in range(0, len(data), 2):
        c = data[i: i + 2]
        m = decrypt(c, k, l)
        decrypted.append(m[0])
        decrypted.append(m[1])
    return decrypted


def inverted_k(k, l):
    det = determinant(k) % l
    modified_k = np.array([[k[1][1], -k[0][1]], [-k[1][0], k[0][0]]])
    return Affine_cipher.findModInverse(det, l) * modified_k % l


def determinant(k):
    return k[0][0] * k[1][1] - k[0][1] * k[1][0]
