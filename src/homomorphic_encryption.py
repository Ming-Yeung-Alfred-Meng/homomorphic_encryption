import numpy as np
from typing import Union, Tuple, Any
from numpy import signedinteger, long


def private_key_candidate(num_bits: int) -> int:
    return np.random.randint(2 ** (num_bits - 1), 2 ** num_bits)


def somehwat_homomorphic_private_key(num_bits: int) -> int:
    key = private_key_candidate(num_bits)
    while key % 2 == 0:
        key = private_key_candidate(num_bits)
    return key


def private_key(num_bits: int,
                hamming_weight: int) -> np.ndarray:
    return np.random.choice(num_bits, size=hamming_weight, replace=False)


def public_key_candidate(size: int,
                         int_size: int,
                         noise_size: int,
                         private_key: int) -> tuple[np.ndarray, signedinteger[Any] | long]:
    key = (private_key *
           np.random.randint(0, (2 ** int_size) / private_key, size=(size,))
           + noise(noise_size, (size,)))

    max_index = np.argmax(key)

    return key, max_index


def move_max(key: np.ndarray,
             max_index: int) -> None:
    max = key[max_index]
    key[max_index] = key[0]
    key[0] = max


def primary_public_key(int_num: int,
                       int_size: int,
                       noise_size: int,
                       somewhat_homomorphic_private_key: int) -> np.ndarray:
    key, max_index = public_key_candidate(int_num, int_size, noise_size, somewhat_homomorphic_private_key)
    while key[max_index] % 2 == 0 or key[max_index] % somewhat_homomorphic_private_key == 1:
        key, max_index = public_key_candidate(int_num, int_size, noise_size, somewhat_homomorphic_private_key)

    move_max(key, max_index)

    return key


def secondary_public_key(int_num: int,
                         int_size: int,
                         private_key: np.ndarray,
                         somewhat_homomorphic_private_key: int) -> np.ndarray:
    u = np.random.randint(0, 2 ** (int_size + 1), size=int_num)
    u[private_key[-1]] = ((np.sum(u[private_key[:-1]]) % (2 ** (int_size + 1)))
                          - np.round((2 ** int_size) / somewhat_homomorphic_private_key))
    return u / (2 ** int_size)


def public_key(primary_int_num: int,
               primary_int_size: int,
               noise_size: int,
               secondary_int_num: int,
               secondary_int_size: int,
               private_key: np.ndarray,
               somewhat_homomorphic_private_key_length: int) -> Tuple[np.ndarray, np.ndarray]:
    k = somehwat_homomorphic_private_key(somewhat_homomorphic_private_key_length)
    return (primary_public_key(primary_int_num,
                               primary_int_size,
                               noise_size,
                               k),
            secondary_public_key(secondary_int_num,
                                 secondary_int_size,
                                 private_key,
                                 k))


def key(private_key_int_num: int,
        hamming_weight: int,
        somewhat_homomorphic_private_key_length: int,
        primary_public_key_int_num: int,
        primary_public_key_int_size: int,
        noise_size: int,
        secondary_int_size: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    priv_k = private_key(private_key_int_num, hamming_weight)
    return priv_k, *public_key(primary_public_key_int_num,
                               primary_public_key_int_size,
                               noise_size,
                               private_key_int_num,
                               secondary_int_size,
                               priv_k,
                               somewhat_homomorphic_private_key_length)


def noise(noise_size: int,
          shape: Tuple[int, ...]) -> np.ndarray:
    return np.random.randint(1 - (2 ** noise_size), 2 ** noise_size, size=shape)


def selected_sum(numbers: np.ndarray,
                 num: int) -> np.ndarray:
    return np.random.choice([0, 1], size=(num, len(numbers))) @ numbers


def int2binary_array(plaintext: int) -> np.ndarray:
    return np.array(list(map(int, bin(plaintext)[2:])))


def somewhat_homomorphic_encrypt(plaintext: int,
                                 public_key: np.ndarray,
                                 secondary_noise_size: int) -> np.ndarray:
    bits = int2binary_array(plaintext)

    return ((bits
             + 2 * noise(secondary_noise_size, bits.shape)
             + 2 * selected_sum(public_key[1:], len(bits)))
            % public_key[0])


def encrypt(plaintext: int,
            primary_public_key: np.ndarray,
            secondary_noise_size: int,
            secondary_public_key: np.ndarray) -> np.ndarray:
    ciphertext = somewhat_homomorphic_encrypt(plaintext, primary_public_key, secondary_noise_size)


def binary_array2int(bits) -> int:
    return int(''.join(map(str, bits)), 2)


def decrypt(private_key: int,
            ciphertext: np.ndarray) -> int:
    bits = ciphertext % private_key % 2
    return binary_array2int(bits)
