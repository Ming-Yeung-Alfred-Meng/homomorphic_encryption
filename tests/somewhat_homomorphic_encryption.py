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
    def test_something(self):
        self.assertTrue(np.allclose())


class PublicKey(unittest.TestCase):
    def test_something(self):
        self.assertTrue(np.allclose())


class Encrypt(unittest.TestCase):
    def test_something(self):
        self.assertTrue(np.allclose())


class Decrypt(unittest.TestCase):
    def test_something(self):
        self.assertTrue(np.allclose())


if __name__ == '__main__':
    unittest.main()
