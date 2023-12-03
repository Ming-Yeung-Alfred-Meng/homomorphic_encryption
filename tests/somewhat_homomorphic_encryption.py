import unittest
from src.somewhat_homomorphic_encryption import *


class Noise(unittest.TestCase):
    def test_simple(self):
        noise_size = 28
        shape = (36,)
        trials = 1000

        for i in range(trials):
            noises = noise(noise_size, shape)
            self.assertTrue(noises.shape == shape)
            self.assertTrue(np.all(- 268435456 < noises))
            self.assertTrue(np.all(noises < 268435456))

    def test_small_noise_size(self):
        noise_size = 2
        shape = (36,)
        trials = 1000

        for i in range(trials):
            noises = noise(noise_size, shape)
            self.assertTrue(noises.shape == shape)
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
        self.security = 3
        self.private_key_length = self.security ** 2
        self.public_key_bits = self.security ** 5
        self.public_key_length = self.public_key_bits + self.security + 1
        self.primary_noise_size = self.security
        self.secondary_noise_size = 2 * self.security

        self.private_key, self.public_key = key(self.private_key_length,
                                                self.public_key_length,
                                                self.public_key_bits,
                                                self.primary_noise_size)
    def test_plaintext0(self):
        plaintext = 0

        trials = 10
        for i in range(trials):
            ciphertext = encrypt(plaintext, self.public_key, self.secondary_noise_size)
            decrypted = decrypt(ciphertext, self.private_key)
            self.assertTrue(plaintext == decrypted)

    def test_plaintext1(self):
        plaintext = 1

        trials = 1000
        for i in range(trials):
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

    def test_addition(self):
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
