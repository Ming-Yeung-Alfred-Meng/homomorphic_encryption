import numpy as np
from typing import Union, Tuple, Any


def private_key(num_bits: int) -> int:
    """
    Generate an odd num_bits-bit integer from the range [2^{num_bits - 1}, 2^{num_bits}) as private key.
    :param num_bits:
    :return:
    """
    return np.random.randint(2 ** (num_bits - 1), 2 ** num_bits) | 1


def public_key_candidate(size: int,
                         int_size: int,
                         noise_size: int,
                         private_key: int) -> tuple[np.ndarray, int]:
    """
    Generate a public key in which each integer x = p * q + r,
    where p is the private key, q is a random integer from [0, 2^{int_size} / p)
    and r is from (-2^{noise_size}, 2^{noise_size}).
    :param size: number of integers in the public key
    :param int_size: bit size of the integers in the public key
    :param noise_size: bit size of noise
    :param private_key: private key
    :return: 1D array of a public key
    """
    key = (private_key *
           np.random.randint(0, (2 ** int_size) / private_key, size=(size,))
           + noise(noise_size, (size,)))

    max_index = np.argmax(key)

    return key, max_index


def move_max(key: np.ndarray,
             max_index: int) -> None:
    """
    Swap the number at max_index with the number at index 0.
    :param key: 1D numpy array
    :param max_index: index of element to swap.
    """
    max = key[max_index]
    key[max_index] = key[0]
    key[0] = max


def public_key(size: int,
               int_size: int,
               noise_size: int,
               private_key: int) -> np.ndarray:
    """
    Generate a public key. The first integer k0 in the key is the largest and is odd, and k0 % private_key is even.
    :param size: number of integers in the public key
    :param int_size: bit size of the integers in the public key
    :param noise_size: bit size of noise
    :param private_key: private key
    :return: 1D array public key
    """
    key, max_index = public_key_candidate(size, int_size, noise_size, private_key)
    while key[max_index] % 2 == 0 or (key[max_index] % private_key) % 2 == 1:
        key, max_index = public_key_candidate(size, int_size, noise_size, private_key)

    move_max(key, max_index)

    return key


def noise(noise_size: int,
          shape: Tuple[int, ...]) -> np.ndarray:
    """
    Generate random noises from integers in (-2^noise_size, 2^noise_size).
    :param noise_size: bit length of each noise.
    :param shape: shape of the output numpy array
    :return: ndarray of noises.
    """
    return np.random.randint(1 - (2 ** noise_size), 2 ** noise_size, size=shape)


def selected_sum(numbers: np.ndarray,
                 num: int) -> np.ndarray:
    """
    Sum a random subset of "numbers".
    :param numbers: ndarray of scalars
    :param num: number of times to sum subsets of "numbers"
    :return: ndarray of shape (num,) containing sums of random subsets of "numbers".
    """
    return np.random.choice([0, 1], size=(num, len(numbers))) @ numbers


def int2binary_array(integer: int) -> np.ndarray:
    """
    Create a 1D array containing the binary digits of a non-negative integer.
    :param integer: non-negative integer of which the binary digits are to store in a 1D array.
    :return: 1D array of binary digits.
    """
    assert 0 <= integer
    return np.array(list(map(int, bin(integer)[2:])))


def binary_array2int(bits) -> int:
    """
    Create an integer from an array containing its binary digits.
    :param bits: 1D array of binary digits.
    :return: integer bits represents.
    """
    return int(''.join(map(str, bits)), 2)


def key(private_key_length: int,
        public_key_length: int,
        public_key_bits: int,
        primary_noise_size: int) -> Tuple:
    k = private_key(private_key_length)
    return k, public_key(public_key_length, public_key_bits, primary_noise_size, k)


def encrypt(plaintext: int,
            public_key: np.ndarray,
            secondary_noise_size: int) -> np.ndarray:
    bits = int2binary_array(plaintext)

    return ((bits
             + 2 * noise(secondary_noise_size, bits.shape)
             + 2 * selected_sum(public_key[1:], len(bits)))
            % public_key[0])


def decrypt(ciphertext: np.ndarray,
            private_key: int) -> int:
    bits = (ciphertext % private_key) % 2
    return binary_array2int(bits)
