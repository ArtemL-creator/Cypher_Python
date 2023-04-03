###############
# SPN1
###############


class SPN1():
    # p-box
    p = [0, 4, 8, 12, 1, 5,
         9, 13, 2, 6, 10, 14,
         3, 7, 11, 15]

    # S-box
    s = [14, 4, 13, 1, 2, 15, 11, 8,
         3, 10, 6, 12, 5, 9, 0, 7]

    # s-box
    def sbox(self, x):
        return self.s[x]

    # p-box
    def pbox(self, x):
        y = 0
        for i in range(len(self.p)):
            if (x & (1 << i)) != 0:
                y ^= (1 << self.p[i])
        return y

    # break into 4-bit chunks
    def demux(self, x):
        y = []
        for i in range(0, 4):
            y.append((x >> (i * 4)) & 0xf)
        return y

    # x=0011    1011    1101   1100
    # y=[12, 13, 11, 3]
    #   1100   1101   1011  0011

    # convert back into 16-bit state
    def mux(self, x):
        y = 0
        for i in range(0, 4):
            y ^= (x[i] << (i * 4))
        return y

    # x = [9, 11, 4, 2]
    # y=0010    0100    1011   1001
    #   2       4        11      9

    def round_keys(self, k):
        rk = []
        rk.append((k >> 16) & (2 ** 16 - 1))
        rk.append((k >> 12) & (2 ** 16 - 1))
        rk.append((k >> 8) & (2 ** 16 - 1))
        rk.append((k >> 4) & (2 ** 16 - 1))
        rk.append(k & (2 ** 16 - 1))
        return rk

    # Key mixing
    def mix(self, p, k):
        v = p ^ k
        return v

    # round function
    def round(self, p, k):
        # XOR key
        u = self.mix(p, k)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.sbox(x))
        # run through permutation layer
        w = self.pbox(self.mux(v))
        return w

    def last_round(self, p, k1, k2):
        # XOR key
        u = self.mix(p, k1)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.sbox(x))
        # XOR key
        u = self.mix(self.mux(v), k2)
        return u

    def encrypt(self, p, rk, rounds):
        x = p
        for i in range(rounds - 1):
            x = self.round(x, rk[i])
        x = self.last_round(x, rk[rounds - 1], rk[rounds])
        return x

    #####################################################################

    def encrypt_data(self, data, key, rounds):
        rk = self.round_keys(key)
        en_d = []
        for di in data:
            en_d.append(self.encrypt(di, rk, rounds))
        return en_d

    def asbox(self, x):
        return self.s.index(x)

    def apbox(self, x):
        y = 0
        for i in range(len(self.p)):
            if (x & (1 << self.p[i])) != 0:
                y ^= (1 << i)
        return y

    def round_keys_to_decrypt(self, key):
        K = self.round_keys(key)
        L = []
        # код
        L.append(int(K[4]))
        L.append((int(self.pbox(K[3]))))
        L.append(((int(self.pbox(K[2])))))
        L.append((int(self.pbox(K[1]))))
        L.append((int(K[0])))
        return L

    # Шифруем одно число
    def decrypt(self, x, rl, rounds):
        for i in range(rounds - 1):
            x = self.round_decrypt(x, rl[i])
        x = self.last_round_decrypt(x, rl[rounds - 1], rl[rounds])
        return x

    def round_decrypt(self, p, k):
        # XOR key
        u = self.mix(p, k)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.asbox(x))
        # run through permutation layer
        w = self.apbox(self.mux(v))
        return w

    def last_round_decrypt(self, p, k1, k2):
        # XOR key
        u = self.mix(p, k1)
        v = []
        # run through substitution layer
        for x in self.demux(u):
            v.append(self.asbox(x))
        # XOR key
        u = self.mix(self.mux(v), k2)
        return u

    def decrypt_data(self, data, key, rounds):

        rk = self.round_keys_to_decrypt(key)
        en_d = []
        for di in data:
            en_d.append(self.decrypt(di, rk, rounds))
        return en_d

    def decrypt_cbc(self, data_c, key, rounds, initV):
        rk = self.round_keys_to_decrypt(key)
        data = []
        for c in data_c:
            m = self.decrypt(c, rk, rounds)
            data.append(m ^ initV)
            initV = c
        return data

    def decrypt_ctr(self, data_c, key, rounds, initV):
        rk = self.round_keys(key)
        data = []
        for m in data_c:
            x = self.encrypt(initV, rk, rounds)
            x = x ^ m
            initV += 1
            data.append(x)

        return data

    def encrypt_CFB(self, data, key, rounds, initV):
        rk = self.round_keys(key)
        cypher_data = []
        for m in data:
            x = self.encrypt(initV, rk, rounds)
            x = m ^ x
            initV = x
            cypher_data.append(x)
        return cypher_data

    def decrypt_CFB(self, data, key, rounds, initV):
        rk = self.round_keys(key)
        cypher_data = []
        for m in data:
            x = self.encrypt(initV, rk, rounds)
            initV = m
            x = x ^ m

            cypher_data.append(x)
        return cypher_data

    def decrypt_OFB(self, data, key, rounds, initV):
        cypher_data = []
        rk = self.round_keys(key)
        for m in data:
            x = self.encrypt(initV, rk, rounds)
            m = m ^ x
            initV = x
            cypher_data.append(m)
        return cypher_data


def main():
    e = SPN1()
    x = int('1010010100010111', 2)
    rounds = 4
    k = int('01101100011101010100111100100001', 2)
    rk = e.round_keys(k)
    y = e.encrypt(x, rk, rounds)
    print('y={}'.format(bin(y)[2:].zfill(16)))


if __name__ == '__main__':
    main()
