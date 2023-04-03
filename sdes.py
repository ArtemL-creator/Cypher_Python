class SDes():
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    LS1 = [2, 3, 4, 5, 1]
    LS2 = [3, 4, 5, 1, 2]
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    IPinv = [4, 1, 3, 5, 7, 2, 8, 6]
    EP = [4, 1, 2, 3, 2, 3, 4, 1]
    P4 = [2, 4, 3, 1]
    SW = [5, 6, 7, 8, 1, 2, 3, 4]
    # таблицы замен
    S0 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [3, 1, 3, 2]]
    S1 = [[0, 1, 2, 3],
          [2, 0, 1, 3],
          [3, 0, 1, 0],
          [2, 1, 0, 3]]

    def __init__(self):
        """
        раундовые ключи. рассчитываются в функции key_schedule
        """
        self.k1 = 0
        self.k2 = 0

    @staticmethod
    def pbox(x, p, nx):
        # перестановка бит в nx-битовом числе x по таблице перестановок p
        y = 0
        np = len(p)
        for i in reversed(range(np)):
            if (x & (1 << (nx - 0 - p[i]))) != 0:
                y ^= (1 << (np - 1 - i))
        return y

    def p10(self, x):
        return self.pbox(x, self.P10, 10)

    def p8(self, x):
        return self.pbox(x, self.P8, 10)

    def p4(self, x):
        return self.pbox(x, self.P4, 4)

    def ip(self, x):
        return self.pbox(x, self.IP, 8)

    def ipinv(self, x):
        return self.pbox(x, self.IPinv, 8)

    def ep(self, x):
        return self.pbox(x, self.EP, 4)

    def sw(self, x):
        return self.pbox(x, self.SW, 8)

    def ls1(self, x):
        return self.pbox(x, self.LS1, 5)

    def ls2(self, x):
        return self.pbox(x, self.LS2, 5)

    @staticmethod
    def divide_into_two(k, n):
        """
        функция разделяет n-битовое число k на два (n/2)-битовых числа
        """
        n2 = n // 2
        mask = 2 ** n2 - 1
        l1 = (k >> n2) & mask
        l2 = k & mask
        return l1, l2

    @staticmethod
    def mux(l, r, n):
        """
        # l, r - n-битовые числа
        # возвращает число (2n-битовое), являющееся конкатенацией бит этих чисел
        """
        y = 0
        y ^= r
        y ^= l << n
        return y

    @staticmethod
    def apply_subst(x, s):
        """
        замена по таблице s
        """
        r = 2 * (x >> 3) + (x & 1)
        c = 2 * ((x >> 2) & 1) + ((x >> 1) & 1)
        return s[r][c]

    def s0(self, x):
        """
        замена по таблице s0
        """
        return self.apply_subst(x, self.S0)

    def s1(self, x):
        """
        замена по таблице s1
        """
        return self.apply_subst(x, self.S1)

    ################################################################################

    ''' Задание 1'''

    def key_schedule(self, key):
        """
        Алгоритм расширения ключа. Функция формирует из ключа шифрования key два
        раундовых ключа self.k1, self.k2
        """
        print("key_schedule")

        k_p10 = self.p10(key)
        print("p10:  ", bin(k_p10)[2:].zfill(10))

        L, R = self.divide_into_two(k_p10, n=10)
        x1 = self.ls1(L)
        x2 = self.ls1(R)
        k1 = self.mux(x1, x2, n=5)
        print("ls1:  ", k1)

        k1 = self.p8(k1)
        print("p8 k1 ", bin(k1)[2:].zfill(8))

        k2 = self.mux(self.ls2(x1), self.ls2(x2), n=5)
        print("\nls2:  ", k2)

        k2 = self.p8(k2)
        print("p8 k2 ", bin(k2)[2:].zfill(8))
        return [k1, k2]

    ''' Задание 2'''

    def F(self, block, k):
        # Inputs
        # block = 4 bits block data (int number)
        # k = 8 bits subkey (int number)
        # Outputs
        # Out=4 bits block data (int number)
        print("\t\tF")

        x = self.ep(block)
        print("\t\te/p:", bin(x)[2:].zfill(8))

        x = x ^ k
        print("\t\txor:", bin(x)[2:].zfill(8))

        x1, x2 = self.divide_into_two(x, n=8)
        x1 = self.s0(x1)
        x2 = self.s1(x2)
        print("\t\ts0: ", bin(x1)[2:].zfill(2), )
        print("\t\ts1: ", bin(x2)[2:].zfill(2))

        x = self.p4(self.mux(x1, x2, n=2))
        print("\t\tp4: ", bin(x)[2:].zfill(4))
        return x

    ''' Задание 3'''

    def f_k(self, block, SK):
        # Inputs
        # block = 8 bits block data (int number)
        # SK = 8 bits subkey (int number)
        # Outputs
        # Out=8 bits block data (int number)
        print("\tf_k")
        print("\tblock: ", bin(block)[2:].zfill(8))
        print("\tSK: ", bin(SK)[2:].zfill(8))

        L, R = self.divide_into_two(block, n=8)
        print("\tL,R ", L, R)

        x = self.F(block=R, k=SK)
        print("\tF: ", bin(x)[2:])

        x = x ^ L
        print("\tx^L:", bin(x)[2:])

        x = self.mux(x, R, n=4)
        print("\treturn:", bin(x)[2:].zfill(8))
        return x

    ''' Задание 4'''

    def sdes(self, block, k1, k2):
        # Inputs
        # block = 8 bits block data (int number)
        # K1 = 8 bits subkey (int number)
        # K2 = 8 bits subkey (int number)
        # Outputs
        # Out=8 bits block data (int number)

        x = self.ip(block)
        print("after ip:  ", bin(x)[2:].zfill(8))

        x = self.f_k(block=x, SK=k1)
        print("after f_k: ", bin(x)[2:].zfill(8))

        x = self.sw(x)
        print("after SW:  ", bin(x)[2:].zfill(8))

        x = self.f_k(block=x, SK=k2)
        print("after f_k: ", bin(x)[2:].zfill(8))

        x = self.ipinv(x)
        print("after ipinv", bin(x)[2:].zfill(8))

        return x

    ''' Задание 5'''

    def encrypt(self, data, key):
        return self.sdes(data, key[0], key[1])

    ''' Задание 6'''

    def decrypt(self, data, key):
        return self.sdes(data, key[1], key[0])

    ''' Задание 7'''

    def encrypt_data(self, data, key):
        k = self.key_schedule(key)
        dd = []
        for x in data:
            dd.append(self.encrypt(x, k))
        return dd

    def decrypt_data(self, data, key):
        k = self.key_schedule(key)
        dd = []
        for x in data:
            dd.append(self.decrypt(x, k))
        return dd

    def decrypt_OFB(self, data, key, initV):
        k = self.key_schedule(key)
        cypher_data = []
        for m in data:
            x = self.encrypt(initV, k)
            m = m ^ x
            initV = x
            cypher_data.append(m)
        return cypher_data


if __name__ == '__main__':
    e = SDes()

    print("\nДля задания 1")
    x = int("0111111101", 2)
    print(e.key_schedule(key=x))

    print("\nДля задания 2")
    print(e.F(block=int("0011", 2), k=int("01011111", 2)))

    print("\nДля задания 3")
    print(e.f_k(block=int("10110011", 2), SK=int("01011111", 2)))

    print("\nДля задания 4")
    print()
    x = e.sdes(block=int("1110_1010", 2), k1=int("0101_1111", 2), k2=int("1111_1100", 2))
    print(x)

