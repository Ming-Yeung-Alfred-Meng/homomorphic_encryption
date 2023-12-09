import unittest
from src.private_key_somewhat_homomorphic_encryption import *


class RandInt(unittest.TestCase):

    def test_single_int_type(self):
        start = 7
        stop = 18
        integer = randint(start, stop)
        self.assertTrue(type(integer) is int)

    def test_single_int_step1(self):
        start = 2
        stop = 6
        trials = 1000

        for i in range(trials):
            integer = randint(start, stop)
            self.assertTrue(2 <= integer <= 5)

    def test_single_even_int(self):
        start = 0
        stop = 7
        trials = 1000

        for i in range(trials):
            integer = randint(start, stop, step=2)
            self.assertTrue(integer % 2 == 0)
            self.assertTrue(0 <= integer <= 6)

    def test_single_odd_int(self):
        start = 1
        stop = 7
        trials = 1000

        for i in range(trials):
            integer = randint(start, stop, step=2)
            self.assertTrue(integer % 2 == 1)
            self.assertTrue(1 <= integer <= 5)

    def test_multiple_int_length(self):
        start = 12
        stop = 16
        length = 4
        array = randint(start, stop, length=length)
        self.assertTrue(array.shape == (length,))

    def test_multiple_int_type(self):
        start = 13
        stop = 19
        length = 4
        index = 2
        array = randint(start, stop, length=length)
        self.assertTrue(type(array[index]) is int)

    def test_multiple_step1(self):
        start = 2
        stop = 6
        length = 11
        trials = 1000

        for i in range(trials):
            array = randint(start, stop, length=length)
            self.assertTrue(np.all(2 <= array))
            self.assertTrue(np.all(array <= 5))

    def test_multiple_even_int(self):
        start = 0
        stop = 7
        length = 6
        trials = 1000

        for i in range(trials):
            integer = randint(start, stop, step=2, length=length)
            self.assertTrue(np.all((integer % 2) == 0))
            self.assertTrue(np.all(0 <= integer))
            self.assertTrue(np.all(integer <= 6))

    def test_multiple_odd_int(self):
        start = 1
        stop = 7
        trials = 1000

        for i in range(trials):
            integer = randint(start, stop, step=2)
            self.assertTrue((integer % 2) == 1)
            self.assertTrue(np.all(1 <= integer))
            self.assertTrue(np.all(integer <= 5))

    def test_large_single_int(self):
        start = 1496577676626844588240573268701473812127674924007424
        stop = 55213970774324510299478046898216203619608871777363092441300193790394368
        trials = 1000

        for i in range(trials):
            integer = randint(start, stop)
            self.assertTrue(np.all(start <= integer))
            self.assertTrue(np.all(integer < stop))


class BinaryArray2Int(unittest.TestCase):
    def test_simple(self):
        bits = np.array([1, 1, 1, 0, 0, 0, 1, 0, 0, 0])

        expected_int = 0b1110001000
        actual_int = binary_array2int(bits)
        self.assertEqual(expected_int, actual_int)


class Int2BinaryArray(unittest.TestCase):
    def test_simple(self):
        integer = 47
        expected_array = np.array([1, 0, 1, 1, 1, 1])
        actual_array = int2binary_array(integer)
        self.assertTrue(np.allclose(expected_array, actual_array))


class KeyMultiple(unittest.TestCase):

    def test_single_int(self):
        num_bits = 11
        length = 0
        q = key_multiple(num_bits, length)
        self.assertTrue(type(q) is int)

    def test_multiple_int(self):
        num_bits = 11
        length = 19
        q = key_multiple(num_bits, length)
        self.assertTrue(q.shape == (length,))

    def test_single_int_simple_range(self):
        trials = 1000
        num_bits = 2
        length = 0
        q = key_multiple(num_bits, length)

        for _ in range(trials):
            self.assertTrue(0 <= q)
            self.assertTrue(q < 4)

    def test_multiple_int_simple_range(self):
        trials = 1000
        num_bits = 10
        length = 7
        q = key_multiple(num_bits, length)

        for _ in range(trials):
            self.assertTrue(np.all(0 <= q))
            self.assertTrue(np.all(q < 1024))


class Noise(unittest.TestCase):
    pass


class Key(unittest.TestCase):

    def test_large_range(self):
        num_bits = 209
        trials = 1000

        for _ in range(trials):
            k = key(num_bits)
            self.assertTrue(411376139330301510538742295639337626245683966408394965837152256 <= k)
            self.assertTrue(k < 822752278660603021077484591278675252491367932816789931674304512)

    def test_odd(self):
        num_bits = 172
        trials = 1000

        for _ in range(trials):
            k = key(num_bits)
            self.assertTrue(k % 2 == 1)


class EncryptDecryptCorrectness(unittest.TestCase):

    def test_single0(self):
        plaintext = 0
        trials = 1000

        for _ in range(trials):
            q_num_bits = randint(64, 128)
            key_num_bits = randint(64, 128)

            k = key(key_num_bits)
            ciphertext = encrypt(plaintext, k, q_num_bits)
            decrypted = decrypt(ciphertext, k)

            self.assertTrue(plaintext == decrypted)

    def test_single1(self):
        plaintext = 1
        trials = 1000

        for _ in range(trials):
            q_num_bits = randint(64, 128)
            key_num_bits = randint(64, 128)

            k = key(key_num_bits)
            ciphertext = encrypt(plaintext, k, q_num_bits)
            decrypted = decrypt(ciphertext, k)

            self.assertTrue(plaintext == decrypted)

    def test_general(self):
        trials = 1000

        for _ in range(trials):
            plaintext = randint(0, 2 ** 128)
            q_num_bits = randint(64, 128)
            key_num_bits = randint(64, 128)

            k = key(key_num_bits)
            ciphertext = encrypt(plaintext, k, q_num_bits)
            decrypted = decrypt(ciphertext, k)

            self.assertTrue(plaintext == decrypted)


class HomomorphicDecryptionCorrectness(unittest.TestCase):

    def test_addition_single_00(self):
        m0 = 0
        m1 = 0
        trials = 1000

        for _ in range(trials):
            key_num_bits = np.random.randint(64, 128)
            q_num_bits = np.random.randint(64, 128)
            k = key(key_num_bits)
            c0 = encrypt(m0, k, q_num_bits)
            c1 = encrypt(m1, k, q_num_bits)
            c_sum = c0 + c1
            xor = decrypt(c_sum, k)
            self.assertTrue(xor == 0)

    def test_addition_single_10(self):
        m0 = 0
        m1 = 1
        trials = 1000

        for _ in range(trials):
            key_num_bits = np.random.randint(64, 128)
            q_num_bits = np.random.randint(64, 128)
            k = key(key_num_bits)
            c0 = encrypt(m0, k, q_num_bits)
            c1 = encrypt(m1, k, q_num_bits)
            c_sum = c0 + c1
            xor = decrypt(c_sum, k)
            self.assertTrue(xor == 1)

    def test_addition_single_11(self):
        m0 = 1
        m1 = 1
        trials = 1000

        for _ in range(trials):
            key_num_bits = np.random.randint(64, 128)
            q_num_bits = np.random.randint(64, 128)
            k = key(key_num_bits)
            c0 = encrypt(m0, k, q_num_bits)
            c1 = encrypt(m1, k, q_num_bits)
            c_sum = c0 + c1
            xor = decrypt(c_sum, k)
            self.assertTrue(xor == 0)

    def test_multiplication_single_00(self):
        m0 = 0
        m1 = 0
        trials = 1000

        for _ in range(trials):
            key_num_bits = np.random.randint(64, 128)
            q_num_bits = np.random.randint(64, 128)
            k = key(key_num_bits)
            c0 = encrypt(m0, k, q_num_bits)
            c1 = encrypt(m1, k, q_num_bits)
            c_product = c0 * c1
            product = decrypt(c_product, k)
            self.assertTrue(product == 0)

    def test_multiplication_single_10(self):
        m0 = 0
        m1 = 1
        trials = 1000

        for _ in range(trials):
            key_num_bits = np.random.randint(64, 128)
            q_num_bits = np.random.randint(64, 128)
            k = key(key_num_bits)
            c0 = encrypt(m0, k, q_num_bits)
            c1 = encrypt(m1, k, q_num_bits)
            c_product = c0 * c1
            product = decrypt(c_product, k)
            self.assertTrue(product == 0)

    def test_multiplication_single_11(self):
        m0 = 1
        m1 = 1
        trials = 1000

        for _ in range(trials):
            key_num_bits = np.random.randint(64, 128)
            q_num_bits = np.random.randint(64, 128)
            k = key(key_num_bits)
            c0 = encrypt(m0, k, q_num_bits)
            c1 = encrypt(m1, k, q_num_bits)
            c_product = c0 * c1
            product = decrypt(c_product, k)
            self.assertTrue(product == 1)

    def test_addition_multiple_bits_simple(self):
        trials = 1000

        for _ in range(trials):
            m0 = np.random.randint(4, 8)
            m1 = np.random.randint(4, 8)
            # key_num_bits = np.random.randint(64, 128)
            # q_num_bits = np.random.randint(64, 128)
            key_num_bits = 5
            q_num_bits = 5
            k = key(key_num_bits)
            c0 = encrypt(m0, k, q_num_bits)
            c1 = encrypt(m1, k, q_num_bits)
            c_sum = c0 + c1
            xor = decrypt(c_sum, k)
            self.assertTrue(xor == (m0 ^ m1))

    def test_multiplication_multiple_bits_simple(self):
        trials = 1000

        for _ in range(trials):
            m0 = np.random.randint(512, 1024)
            m1 = np.random.randint(512, 1024)
            key_num_bits = np.random.randint(64, 128)
            q_num_bits = np.random.randint(64, 128)
            k = key(key_num_bits)
            c0 = encrypt(m0, k, q_num_bits)
            c1 = encrypt(m1, k, q_num_bits)
            c_product = c0 * c1
            product = decrypt(c_product, k)
            self.assertTrue(product == (m0 & m1))


if __name__ == '__main__':
    unittest.main()
