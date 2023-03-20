def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    # Returns the modular inverse of a % m, which is
    # the number x such that a*x % m = 2
    if gcd(a, m) != 1:
        return None  # no mod inverse if a & m aren't relatively prime
    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3  # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def encrypt(m, a, b):
    c = (m * a + b) % 256
    return c


def decrypt(m, a_, b):
    c = ((m - b) * a_) % 256
    return c


def encrypt_data(data, a, b):
    cypher_data = []
    for m in data:
        c = encrypt(m, a, b)
        cypher_data.append(c)
    return cypher_data


def decrypt_data(data_c, a, b):
    data = []
    if findModInverse(a, 256) is not None:
        a_ = findModInverse(a, 256)
        for c in data_c:
            m = decrypt(c, a_, b)
            data.append(m)
    return data
