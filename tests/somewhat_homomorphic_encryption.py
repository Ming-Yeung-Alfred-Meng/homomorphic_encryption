import unittest
from src.somewhat_homomorphic_encryption import *


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


class Noise(unittest.TestCase):
    def test_simple(self):
        noise_size = 28
        length = 36
        trials = 1000

        for i in range(trials):
            noises = noise(noise_size, length)
            self.assertTrue(noises.shape == (length,))
            self.assertTrue(np.all(- 268435456 < noises))
            self.assertTrue(np.all(noises < 268435456))

    def test_small_noise_size(self):
        noise_size = 2
        length = 36
        trials = 1000

        for i in range(trials):
            noises = noise(noise_size, length)
            self.assertTrue(noises.shape == (length,))
            self.assertTrue(np.all(- 4 < noises))
            self.assertTrue(np.all(noises < 4))

class SelectedSum(unittest.TestCase):
    def test_simple(self):

        numbers = np.array([25, 13])
        num = 1000

        possibilities = [0, 13, 25, 38]
        sums = selected_sum(numbers, num)

        self.assertTrue(np.all(np.any(sums[:, None] == possibilities, axis=1)))


class MoveMax(unittest.TestCase):
    def test_simple(self):
        array = np.array([-55, -15,  23,  70,  70, -33, -83, -85,   5, -26])
        index = 3
        expected_array = np.array([70, -15,  23,  -55,  70, -33, -83, -85,   5, -26])
        move_max(array, index)
        self.assertTrue(np.allclose(array, expected_array))


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


class PrivateKey(unittest.TestCase):
    def test_simple(self):
        trials = 1000
        num_bits = 56

        for i in range(trials):
            key = private_key(num_bits)
            self.assertTrue(key % 2 == 1)
            self.assertTrue(key < 72057594037927936)
            self.assertTrue(36028797018963968 <= key)

    def test_small_num_bits(self):
        trials = 1000
        num_bits = 3
        possibilities = np.array([5, 7])

        for i in range(trials):
            key = private_key(num_bits)
            self.assertTrue(np.any(key == possibilities))


class PublicKeyCandidate(unittest.TestCase):
    def test_simple(self):
        size = 26
        int_size = 40
        noise_size = 33
        private_key = 36

        trials = 1000

        for i in range(trials):
            key, max_index = public_key_candidate(size, int_size, noise_size, private_key)
            self.assertTrue(np.all(key < 1108101562368))
            self.assertTrue(np.all(- 8589934592 < key))
            self.assertTrue(np.all(key[max_index] >= key))


class PublicKey(unittest.TestCase):
    def test_simple(self):
        int_size = 64
        size = 3
        noise_size = 3
        private_key = 31 # must be odd

        trials = 1000
        for i in range(trials):
            key = public_key(size, int_size, noise_size, private_key)
            self.assertTrue(np.all(key[0] >= key))
            self.assertTrue(key[0] % 2 == 1)
            self.assertTrue((key[0] % private_key) % 2 == 0)


class EncryptDecrypt(unittest.TestCase):

    def setUp(self) -> None:
        # self.security = 5
        # self.private_key_length = self.security ** 2
        # self.public_key_bits = self.security ** 5
        # self.public_key_length = self.public_key_bits + self.security + 1
        # self.primary_noise_size = self.security
        # self.secondary_noise_size = 2 * self.security

        self.trials = 3

        self.private_key_length = 20
        self.public_key_bits = 20
        self.public_key_length = 4
        self.primary_noise_size = 2
        self.secondary_noise_size = 2

        self.private_key, self.public_key = key(self.private_key_length,
                                                self.public_key_length,
                                                self.public_key_bits,
                                                self.primary_noise_size)
    def test_plaintext0(self):
        plaintext = 0

        for i in range(self.trials):
            ciphertext = encrypt(plaintext, self.public_key, self.secondary_noise_size)
            decrypted = decrypt(ciphertext, self.private_key)
            self.assertTrue(plaintext == decrypted)

    def test_plaintext1(self):
        plaintext = 1

        for i in range(self.trials):
            ciphertext = encrypt(plaintext, self.public_key, self.secondary_noise_size)
            decrypted = decrypt(ciphertext, self.private_key)
            self.assertTrue(plaintext == decrypted)

    def test_addition(self):
        plaintext0 = 0
        plaintext1 = 1

        trials = 1000
        for i in range(trials):
            ciphertext0 = encrypt(plaintext0, self.public_key, self.secondary_noise_size)
            ciphertext1 = encrypt(plaintext1, self.public_key, self.secondary_noise_size)

            decrypted = decrypt(ciphertext0 + ciphertext1, self.private_key)
            self.assertTrue(decrypted == 1)

    def test_multiplication(self):
        plaintext0 = 0
        plaintext1 = 1

        trials = 1000
        for i in range(trials):
            ciphertext0 = encrypt(plaintext0, self.public_key, self.secondary_noise_size)
            ciphertext1 = encrypt(plaintext1, self.public_key, self.secondary_noise_size)

            decrypted = decrypt(ciphertext0 * ciphertext1, self.private_key)
            self.assertTrue(decrypted == 0)

if __name__ == '__main__':
    unittest.main()
