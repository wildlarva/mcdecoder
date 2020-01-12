import os
import re
from typing import Literal


# region External functions


def convert_to_big_endian(bits: str, base: Literal[2, 16], byteorder: Literal['big', 'little']) -> str:
    """
    Convert the byte order of bits to big endian.

    If byteorder is big, no conversion will be taken place.

    :param bits: Binary/hex string to be converted
    :param base: Base of integer that specifies the expression of bits
    :param byteorder: Byte order of bits
    :return: Converted binary/hex string that is big endian
    """
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
    """
    Pad trailing zeros to bits if the length of bits is less than expected_bit_size.

    If expected_bit_size is not aligned to a byte alignment, some additional bits are added to a byte alignment.

    :param bits: Binary/hex string to be converted
    :param base: Base of integer that specifies the expression of bits
    :param expected_bit_size: Expected bit size bits should have
    :return: Padded binary/hex string
    """
    expected_byte_size = (expected_bit_size + 7) // 8
    byte_str_len = string_length_for_byte(base)
    pad_len = max(byte_str_len * expected_byte_size - len(bits), 0)
    return bits + '0' * pad_len


def string_length_for_byte(base: Literal[2, 16]) -> int:
    """
    Calculate a string length that corresponds to one byte

    :param base: Base of integer
    :return: A string length for one byte
    """
    return 8 if base == 2 else 2


def bit_length_of_character(base: Literal[2, 16]) -> int:
    """
    Calculate a bit length that corresponds to one character

    :param base: Base of integer
    :return: A bit length for one character
    """
    return 1 if base == 2 else 4


def trim_whitespace(s: str) -> str:
    """
    Trim all the whitespaces from a string

    :param s: String which trims whitespace from
    :return: Whitespace-trimmed string
    """
    return re.sub(r'\s', '', s)


def make_mask(bit_size: int) -> int:
    """
    Make a mask of bit_size bits

    :param bit_size: Bit length of a mask
    :return: A mask with bit_size bits
    """
    return (1 << bit_size) - 1


def make_parent_directories(file: str) -> bool:
    """
    Make parent directories of a file path

    :param file: Path to a file
    :return: True if succeeded in making parent directories. False otherwise.
    """
    dir = os.path.dirname(file)
    if dir != '':
        if not os.path.exists(dir):
            os.makedirs(dir)
        elif not os.path.isdir(dir):
            return False

    return True

# endregion
