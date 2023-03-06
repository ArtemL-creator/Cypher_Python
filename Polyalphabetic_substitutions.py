def encrypt_data(data, key):
    cypher_data = []
    k = [ord(s) for s in key]
    for m in data:
        c = (m + k) % 26
        cypher_data.append(c)
    return cypher_data


def decrypt_data(data_c, key):
    data = []
    k = [ord(s) for s in key]
    for c in data_c:
        m = (c - k) % 26
        data.append(m)
    return data
