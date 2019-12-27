import os
import re
from typing import Literal


# External functions


def convert_to_big_endian(bits: str, base: Literal[2, 16], byteorder: Literal['big', 'little']) -> str:
    if byteorder == 'big':
        return bits
    else:  # byteorder == 'little'
        # String length that corresponds to a byte
        byte_str_len = string_length_for_byte(base)

        # Pad 0 if bit pattern is fragmented for a byte
        pad_len = (len(bits) + byte_str_len - 1) // byte_str_len * \
            byte_str_len - len(bits)
        padded_bits = '0' * pad_len + bits

        # Little endian to big endian
        converted_bits = ''.join(bits[pos:pos+byte_str_len]
                                 for pos in range(len(padded_bits) - byte_str_len, -1, -byte_str_len))

        return converted_bits


def pad_trailing_zeros(bits: str, base: Literal[2, 16], expected_bit_size: int) -> str:
    expected_byte_size = (expected_bit_size + 7) // 8
    byte_str_len = string_length_for_byte(base)
    pad_len = max(byte_str_len * expected_byte_size - len(bits), 0)
    return bits + '0' * pad_len


def string_length_for_byte(base: Literal[2, 16]) -> int:
    """Calculate a string length that corresponds to one byte"""
    return 8 if base == 2 else 2


def bit_length_of_character(base: Literal[2, 16]) -> int:
    """Calculate a bit length that corresponds to one character"""
    return 1 if base == 2 else 4


def trim_whitespace(s: str) -> str:
    return re.sub(r'\s', '', s)


def make_mask(bit_size: int) -> int:
    return (1 << bit_size) - 1


def make_parent_directories(file: str) -> bool:
    dir = os.path.dirname(file)
    if dir != '':
        if not os.path.exists(dir):
            os.makedirs(dir)
        elif not os.path.isdir(dir):
            return False

    return True
