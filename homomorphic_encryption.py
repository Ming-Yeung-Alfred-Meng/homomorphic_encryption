import numpy as np
from typing import Union, Tuple, Any

from numpy import signedinteger, long


def private_key_candidate(num_bits: int) -> int:
    return np.random.randint(2 ** (num_bits - 1), 2 ** num_bits)


def private_key(num_bits: int) -> int:
    key = private_key_candidate(num_bits)
    while key % 2 == 0:
        key = private_key_candidate(num_bits)
    return key


def public_key_candidate(size: int,
                         int_size: int,
                         noise_size: int,
                         private_key: int) -> tuple[np.ndarray, signedinteger[Any] | long]:
    key = (private_key *
           np.random.randint(0, (2 ** int_size) / private_key, size=(size + 1,))
           + np.random.randint(1 - (2 ** noise_size), 2 ** noise_size, size=(size + 1,)))

    max_index = np.argmax(key)

    return key, max_index


def move_max(key: np.ndarray,
             max_index: int) -> None:
    max = key[max_index]
    key[max_index] = key[0]
    key[0] = max


def public_key(size: int,
               int_size: int,
               noise_size: int,
               private_key: int) -> np.ndarray:
    key, max_index = public_key_candidate(size, int_size, noise_size, private_key)
    while key[max_index] % 2 == 0 or key[max_index] % private_key == 1:
        key, max_index = public_key_candidate(size, int_size, noise_size, private_key)

    move_max(key, max_index)

    return key


def noise(noise_size: int,
          shape: Tuple[int, ...]) -> np.ndarray:
    return np.random.randint(1 - (2 ** noise_size), 2 ** noise_size, size=shape)

def selected_sum(numbers: np.ndarray,
                 num: int) -> np.ndarray:
    return np.random.choice([0, 1], size=(num, len(numbers))) @ numbers


def int2binary_array(plaintext: int) -> np.ndarray:
    return np.array(list(map(int, bin(plaintext)[2:])))


def encrypt(plaintext: int,
            public_key: np.ndarray,
            secondary_noise_size: int) -> np.ndarray:

    bits = int2binary_array(plaintext)

    return ((bits
            + 2 * noise(secondary_noise_size, bits.shape)
            + 2 * selected_sum(public_key[1:], len(bits)))
            % public_key[0])


def decrypt(private_key: int,
            ciphertext: np.ndarray) -> int:
    pass