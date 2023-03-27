import Caesar

''' CBC-----------------------------------'''


def decrypt_CBC(data_c, key, IV):
    data = []
    for c in data_c:
        m = Caesar.decrypt(c, key)
        data.append(m ^ IV)
        IV = c
    return data


def encrypt_CBC(data, key, IV):
    cypher_data = []
    for m in data:
        m = m ^ IV
        x = Caesar.encrypt(m, key)
        IV = x
        cypher_data.append(x)
    return cypher_data


''' OFB-----------------------------------'''


def decrypt_OFB(data, key, IV):
    cypher_data = []
    for m in data:
        x = Caesar.encrypt(IV, key)
        m = m ^ x
        IV = x
        cypher_data.append(m)
    return cypher_data


def encrypt_OFB(data_c, key, IV):
    data = []
    for с in data_c:
        x = Caesar.decrypt(IV, key)
        с = с ^ x
        IV = x
        data.append(с)
    return data


''' CFB-----------------------------------'''


def decrypt_CFB(data_c, key, IV):
    data = []
    for с in data_c:
        x = Caesar.decrypt(IV, key)
        x = x ^ с
        IV = с
        data.append(x)
    return data


def encrypt_CFB(data, key, IV):
    cypher_data = []
    for m in data:
        x = Caesar.encrypt(IV, key)
        x = m ^ x
        IV = x
        cypher_data.append(x)
    return cypher_data


''' CTR-----------------------------------'''


def decrypt_CTR(data, key, IV):
    cypher_data = []
    for m in data:
        x = Caesar.encrypt(IV, key)
        m = m ^ x
        IV += 1
        cypher_data.append(m)
    return cypher_data


def encrypt_CTR(data_с, key, IV):
    data = []
    for с in data_с:
        x = Caesar.decrypt(IV, key)
        x = x ^ с
        IV += 1
        data.append(x)
    return data
