from typing import Union
import numpy as np
import random
import math


def randint(start: int,
            stop: int,
            step: int = 1,
            length: int = 0,
            dtype=object) -> Union[int, np.ndarray]:
    """
    Generate an array of random integers from [start, stop).
    :param start: start of the sample space (inclusive)
    :param stop: end of the sample space (exclusive)
    :param step: sample space includes every "step" number starting form "stop"
    :param length: length of the output array. If 0, an int is returned.
    :param dtype: dtype of the output array
    :return: 1D numpy array of random integers from [start, stop).
    """
    if length == 0:
        return random.randrange(start, stop, step)
    else:
        return np.array([random.randrange(start, stop, step) for _ in range(length)], dtype=dtype)


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
    :return: integer "bits" represents.
    """
    return int(''.join(map(str, bits)), 2)


def key_multiple(num_bits: int,
                 num: int) -> Union[int, np.ndarray]:
    """
    Sample q from [0, 2 ** num_bits), where q is intended for the encryption c = qp + 2r + m.
    :param num_bits: number of bits of q.
    :param num: number of q to generate
    :return: an integer if num = 0, a 1D numpy array of shape (num,) if num > 0.
    """
    return randint(0, 2 ** num_bits, length=num)


def noise(key: int,
          num: int) -> Union[int, np.ndarray]:
    """
    Sample positive noise r, where r is intended for the encryption c = qp + 2r + m. The magnitude of r ensures
    homomorphism of addition or multiplication of ciphertexts for at least once.
    :param key: encryption key, i.e. p in c = qp + 2r + m
    :param num: number of r to generate
    :return: an integer if num = 0, a 1D numpy array of shape (num,) if num > 0.
    """
    return randint(0, math.floor((-1 + math.sqrt(key - 1)) / 2), length=num)


def key(num_bits: int) -> int:
    """
    Generate an odd num_bits-bit integer from the range [2^{num_bits - 1}, 2^{num_bits}) as private key.
    :param num_bits: number of bits of the private key.
    :return: an odd integer private key
    """
    return randint(2 ** (num_bits - 1) + 1, 2 ** num_bits, step=2)


def encrypt(plaintext: int,
            key: int,
            q_num_bits: int) -> np.ndarray:
    """
    Encrypt a plaintext as c = qp + 2r + m, where m is a bit in the plaintext, p is a key, q is a factor of p,
    r is a noise, and c, an integer, is an encryption of m.
    :param plaintext: an integer to encrypt
    :param key: an encryption key
    :param q_num_bits: number of bits of q
    :return: 1D numpy array of encryption of each bit of plaintext
    """
    plaintext_binary = int2binary_array(plaintext)

    return (key_multiple(q_num_bits, len(plaintext_binary)) * key
            + 2 * noise(key, len(plaintext_binary))
            + plaintext_binary)


def decrypt(ciphertext: np.ndarray,
            key: int) -> int:
    """
    Decrypt.
    :param ciphertext: 1D numpy array of encryption of each bit of plaintext
    :param key: encryption key
    :return: plaintext as an integer
    """
    plaintext_binary = ciphertext % key % 2
    return binary_array2int(plaintext_binary)
