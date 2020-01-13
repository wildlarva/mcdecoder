from dataclasses import dataclass
import itertools
import re
import textwrap
from typing import Callable, FrozenSet, List, Literal, Optional, Set

import numpy as np

from . import common, core

# region External functions


def check(mcfile: str, bit_pattern: str, base: Literal[2, 16] = None) -> int:
    """
    Implementation of the sub-command 'check'.

    Check the integrity of an MC description and output errors.

    If base is not specified, base 16 is used by default.

    NOTE Currently, mcdecoder does not support little endian bit pattern.

    :param mcfile: Path to an MC description file
    :param bit_pattern: Binary data to be input
    :param base: Base of integer that specifies the expression of binary data
    :return: Exit code of mcdecoder
    """
    # Default
    if base is None:
        base = 16

    # Check and output progress
    print('-' * 80)
    print('Checking instructions...')
    result = _check(mcfile, bit_pattern, base, _output_error)
    print('Done.')

    # Output check results
    print('-' * 80)
    print('Check result')
    print('-' * 80)
    print(textwrap.dedent(f'''\
        Count of bit patterns:
          Undefined: {result.undefined_error_count:,} (with no instructions)
          Duplicate: {result.duplicate_error_count:,} (with duplicate instructions)
          No error: {result.no_error_count:,}
        Count of duplicate instruction pairs: {len(result.duplicate_instruction_pairs):,}
        Duplicate instructions:\
        '''))

    if len(result.duplicate_instruction_pairs) > 0:
        for instruction_pair in result.duplicate_instruction_pairs:
            if len(instruction_pair) >= 2:
                instruction1, instruction2 = instruction_pair
            else:
                (instruction1,) = (instruction2,) = instruction_pair

            print(textwrap.indent(f'{instruction1} - {instruction2}', ' ' * 2))
    else:
        print(textwrap.indent('None', ' ' * 2))

    return 0


# endregion

# region Internal classes


@dataclass
class _VariableBitRange:
    """Variable bit range information in a bit pattern"""
    mask: int
    shift: int


@dataclass
class _BitPattern:
    """Bit pattern to be checked"""
    fixed_bits: int
    variable_bit_size: int
    variable_bit_ranges: List[_VariableBitRange]


@dataclass
class _CheckContext:
    """A context information while checking"""
    bit_pattern: _BitPattern
    """Bit pattern to be checked"""
    decode_context: core.DecodeContextVectorized
    """A context information while decoding"""
    duplicate_instruction_mat: np.ndarray
    """
    N x M matrix of duplicate detections and instructions.
    Each row expresses a detection instance.
    Each element holds a bool test result whether an instruction is matched for a code

    NOTE The first row is a dummy to keep a dimension of a matrix.
    """
    undefined_count: int = 0
    """Detected count of undefined instructions"""
    duplicate_count: int = 0
    """Detected count of duplicate instructions"""
    ongoing_undefined_range_vec: Optional[np.ndarray] = None
    """
    Ongoing detection range of an undefined instruction.
    This is 4-vector of step start, bits start, step end and bits end
    """
    ongoing_duplicate_range_vec: Optional[np.ndarray] = None
    """Ongoing detection range of a duplicate instruction. This is 4-vector of step start, bits start, step end and bits end"""


@dataclass
class _CheckResult:
    """Final result of checking"""
    no_error_count: int
    undefined_error_count: int
    duplicate_error_count: int
    duplicate_instruction_pairs: List[List[str]]


@dataclass
class _Error:
    """Error reported while checking"""
    type: Literal['undefined', 'duplicate']
    bits_start: int
    bits_end: int


# endregion

# region Internal global variables


_VEC_SIZE = 1 << 16
"""Max size of vectors and rows of matrices used for checking"""


# endregion

# region Internal functions


def _output_error(errors: List[_Error]) -> None:
    for error in errors:
        if error.type == 'undefined':
            print(
                f'{error.bits_start:#010x} - {error.bits_end:#010x}: Undefined (has no instructions)')
        elif error.type == 'duplicate':
            print(
                f'{error.bits_start:#010x} - {error.bits_end:#010x}: Duplicate (has duplicate instructions)')


def _check(mcfile: str, bit_pattern: str, base: Literal[2, 16], callback: Callable[[List[_Error]], None]) -> _CheckResult:
    """Testable implementation of check sub-command"""
    # Create MC decoder model
    mcdecoder = core.create_mcdecoder_model(mcfile)

    # Trim whitespaces
    trimmed_bit_pattern = common.trim_whitespace(bit_pattern)

    # Pad 0 if bit pattern < 32 bits
    padded_bit_pattern = common.pad_trailing_zeros(
        trimmed_bit_pattern, base, 32)

    # Strip to 32 bits
    byte_str_len = common.string_length_for_byte(base)
    converted_bit_pattern = padded_bit_pattern[:byte_str_len * 4]

    # Parse bit pattern
    parsed_bit_pattern = _create_bit_pattern(converted_bit_pattern, base)

    # Check instructions
    return _check_instructions_vectorized(mcdecoder, parsed_bit_pattern, callback)


def _check_instructions_vectorized(mcdecoder: core.McDecoder, bit_pattern: _BitPattern,
                                   callback: Callable[[List[_Error]], None]) -> _CheckResult:
    """
    Check instructions if they have any errors.
    Errors are reported through callback while checking.
    """
    total_count = 1 << bit_pattern.variable_bit_size

    # Create check context
    decode_context = core.DecodeContextVectorized(
        mcdecoder=mcdecoder, code16_vec=np.empty(()), code32_vec=np.empty(()))

    # N x M matrix of detected duplicates and instructions holding boolean whether an instruction is matched
    duplicate_instruction_mat = np.full(
        (1, len(mcdecoder.instruction_decoders)), False)

    context = _CheckContext(bit_pattern=bit_pattern, decode_context=decode_context,
                            duplicate_instruction_mat=duplicate_instruction_mat)

    # Iterate over variable bits and emulate decoder
    for step_start in range(0, total_count, _VEC_SIZE):
        step_end = min(step_start + _VEC_SIZE, total_count) - 1

        # Make bits to test
        step_vec = np.arange(step_start, step_end + 1)
        bits_vec = _make_bits(context, step_vec)

        context.decode_context.code32_vec = bits_vec
        context.decode_context.code16_vec = bits_vec >> 16

        # Emulate decode matching
        test_mat = core.find_matched_instructions_vectorized(
            context.decode_context)
        matched_instruction_count_vec = np.sum(test_mat, axis=1)

        # Combine step, bits and test result
        # N x 2 matrix of codes x (step, bits)
        header_mat = np.hstack((step_vec.reshape(
            step_vec.shape[0], 1), bits_vec.reshape(bits_vec.shape[0], 1)))

        # Collect errors
        errors: List[_Error] = []

        # Find undefined
        undefined_errors = _detect_undefined_errors(
            context, header_mat, matched_instruction_count_vec, step_end)
        errors.extend(undefined_errors)

        # Find duplicates
        duplicate_errors = _detect_duplicate_errors(
            context, header_mat, test_mat, matched_instruction_count_vec, step_end)
        errors.extend(duplicate_errors)

        # Report errors
        if len(errors) > 0:
            errors = sorted(errors, key=lambda error: error.bits_start)
            callback(errors)

    # Handle left errors
    errors = _create_left_errors(context)

    # Report errors
    if len(errors) > 0:
        errors = sorted(errors, key=lambda error: error.bits_start)
        callback(errors)

    # Find duplicate instruction pairs
    duplicate_instruction_pairs = _detect_duplicate_instruction_pairs(context)

    # Create result
    no_error_count = total_count - context.undefined_count - context.duplicate_count

    return _CheckResult(no_error_count=no_error_count, undefined_error_count=context.undefined_count,
                        duplicate_error_count=context.duplicate_count, duplicate_instruction_pairs=duplicate_instruction_pairs)


def _create_bit_pattern(bit_pattern: str, base: Literal[2, 16]) -> _BitPattern:
    """Parse bit pattern"""
    char_bit_len = common.bit_length_of_character(base)
    fixed_bits = int(bit_pattern.replace('x', '0'), base=base)

    # Calculate variable bit size
    variable_bit_size = len(
        [bit for bit in bit_pattern if bit == 'x']) * char_bit_len

    # Create variable bit ranges
    start_bit_in_variable_bits = variable_bit_size - 1

    variable_bit_ranges: List[_VariableBitRange] = []
    for mo in re.finditer('x+', bit_pattern):
        # Calculate bit positions and length
        bit_len = (mo.end() - mo.start()) * char_bit_len
        start_bit_in_bits = (len(bit_pattern) - mo.start()) * char_bit_len - 1
        end_bit_in_bits = start_bit_in_bits - bit_len + 1
        end_bit_in_variable_bits = start_bit_in_variable_bits - bit_len + 1

        # Make mask and shift bits
        mask = common.make_mask(bit_len) << end_bit_in_variable_bits
        shift = end_bit_in_bits - end_bit_in_variable_bits

        # Create VariableBitRange
        variable_bit_range = _VariableBitRange(
            shift=shift, mask=mask)
        variable_bit_ranges.append(variable_bit_range)

        # Move start bit position to next variable bit range
        start_bit_in_variable_bits -= bit_len

    # Create bit pattern
    return _BitPattern(fixed_bits=fixed_bits, variable_bit_size=variable_bit_size, variable_bit_ranges=variable_bit_ranges)


def _detect_undefined_errors(context: _CheckContext, header_mat: np.ndarray, matched_instruction_count_vec: np.ndarray,
                             step_end: int) -> List[_Error]:
    errors = []

    undefined_header_mat = header_mat[matched_instruction_count_vec == 0]
    # N x M matrix of ranges x (step start, bits start, step end and bits end). Each row expresses a range
    undefined_range_mat: Optional[np.ndarray] = None
    if len(undefined_header_mat) > 0:
        # Split ranges
        start_index_vec = np.hstack((np.array([0]), np.where(
            np.diff(undefined_header_mat[:, 0]) != 1)[0] + 1))
        end_index_vec = np.hstack(
            (np.where(np.diff(undefined_header_mat[:, 0]) != 1)[0], np.array([-1])))
        undefined_range_mat = np.hstack(
            (undefined_header_mat[start_index_vec], undefined_header_mat[end_index_vec]))

        # Concatenate ongoing undefined range
        if context.ongoing_undefined_range_vec is not None:
            if undefined_range_mat[0, 0] == context.ongoing_undefined_range_vec[2] + 1:
                undefined_range_mat[0,
                                    0:2] = context.ongoing_undefined_range_vec[0:2]
            else:
                undefined_range_mat = np.vstack(
                    (context.ongoing_undefined_range_vec, undefined_range_mat))

            context.ongoing_undefined_range_vec = None

    else:
        # Use ongoing undefined range
        if context.ongoing_undefined_range_vec is not None:
            undefined_range_mat = context.ongoing_undefined_range_vec.reshape(
                1, 4)
            context.ongoing_undefined_range_vec = None

    if undefined_range_mat is not None:
        # Save ongoing undefined range
        if undefined_range_mat[-1, 2] == step_end:
            context.ongoing_undefined_range_vec = undefined_range_mat[-1]
            undefined_range_mat = undefined_range_mat[:-1]

        # Create errors
        for undefined_range_vec in undefined_range_mat:
            error_step_start, error_bits_start = undefined_range_vec[0:2]
            error_step_end, error_bits_end = undefined_range_vec[2:4]
            context.undefined_count += error_step_end - error_step_start + 1
            errors.append(
                _Error(type='undefined', bits_start=error_bits_start, bits_end=error_bits_end))

    return errors


def _detect_duplicate_errors(context: _CheckContext, header_mat: np.ndarray, test_mat: np.ndarray,
                             matched_instruction_count_vec: np.ndarray, step_end: int) -> List[_Error]:
    errors = []

    duplicate_header_mat = header_mat[matched_instruction_count_vec >= 2]
    # N x M matrix of ranges x (step start, bits start, step end and bits end). Each row expresses a range
    duplicate_range_mat: Optional[np.ndarray] = None
    if len(duplicate_header_mat) > 0:
        # Save duplicate instruction pairs
        duplicate_test_mat = test_mat[matched_instruction_count_vec >= 2]
        duplicate_instruction_mat = np.unique(
            duplicate_test_mat, axis=0)
        context.duplicate_instruction_mat = np.vstack(
            (context.duplicate_instruction_mat, duplicate_instruction_mat))

        # Split ranges
        start_index_vec = np.hstack((np.array([0]), np.where(
            np.diff(duplicate_header_mat[:, 0]) != 1)[0] + 1))
        end_index_vec = np.hstack(
            (np.where(np.diff(duplicate_header_mat[:, 0]) != 1)[0], np.array([-1])))
        duplicate_range_mat = np.hstack(
            (duplicate_header_mat[start_index_vec], duplicate_header_mat[end_index_vec]))

        # Concatenate ongoing duplicate range
        if context.ongoing_duplicate_range_vec is not None:
            if duplicate_range_mat[0, 0] == context.ongoing_duplicate_range_vec[2] + 1:
                duplicate_range_mat[0,
                                    0:2] = context.ongoing_duplicate_range_vec[0:2]
            else:
                duplicate_range_mat = np.vstack(
                    (context.ongoing_duplicate_range_vec, duplicate_range_mat))

            context.ongoing_duplicate_range_vec = None

    else:
        # Use ongoing duplicate range
        if context.ongoing_duplicate_range_vec is not None:
            duplicate_range_mat = context.ongoing_duplicate_range_vec.reshape(
                1, 4)
            context.ongoing_duplicate_range_vec = None

    if duplicate_range_mat is not None:
        # Save ongoing duplicate range
        if duplicate_range_mat[-1, 2] == step_end:
            context.ongoing_duplicate_range_vec = duplicate_range_mat[-1]
            duplicate_range_mat = duplicate_range_mat[:-1]

        # Create errors
        for duplicate_range_vec in duplicate_range_mat:
            error_step_start, error_bits_start = duplicate_range_vec[0:2]
            error_step_end, error_bits_end = duplicate_range_vec[2:4]
            context.duplicate_count += error_step_end - error_step_start + 1
            errors.append(
                _Error(type='duplicate', bits_start=error_bits_start, bits_end=error_bits_end))

    return errors


def _create_left_errors(context: _CheckContext) -> List[_Error]:
    errors = []

    # Handle left undefined errors
    if context.ongoing_undefined_range_vec is not None:
        # Create error
        error_step_start, error_bits_start = context.ongoing_undefined_range_vec[0:2]
        error_step_end, error_bits_end = context.ongoing_undefined_range_vec[2:4]
        context.undefined_count += error_step_end - error_step_start + 1
        errors.append(
            _Error(type='undefined', bits_start=error_bits_start, bits_end=error_bits_end))

    # Handle left duplicate errors
    if context.ongoing_duplicate_range_vec is not None:
        # Create error
        error_step_start, error_bits_start = context.ongoing_duplicate_range_vec[0:2]
        error_step_end, error_bits_end = context.ongoing_duplicate_range_vec[2:4]
        context.duplicate_count += error_step_end - error_step_start + 1
        errors.append(
            _Error(type='duplicate', bits_start=error_bits_start, bits_end=error_bits_end))

    return errors


def _make_bits(context: _CheckContext, step_vec: np.ndarray) -> np.ndarray:
    bits_vec = np.full((step_vec.shape[0]), context.bit_pattern.fixed_bits)
    for bit_range in context.bit_pattern.variable_bit_ranges:
        bits_vec |= (step_vec & bit_range.mask) << bit_range.shift
    return bits_vec


def _detect_duplicate_instruction_pairs(context: _CheckContext) -> List[List[str]]:
    duplicate_instruction_pairs: Set[FrozenSet[str]] = set()

    # Remove the dummy row
    duplicate_instruction_mat = context.duplicate_instruction_mat[1:]

    # Make unique instruction pair combinations
    if len(duplicate_instruction_mat) > 0:
        instruction_name_vec = np.array(
            [instruction.name for instruction in context.decode_context.mcdecoder.instruction_decoders])

        duplicate_instruction_mat = np.unique(
            duplicate_instruction_mat, axis=0)

        for matched_instruction_vec in duplicate_instruction_mat:
            instructions = instruction_name_vec[matched_instruction_vec]
            for instruction_pair in itertools.combinations(instructions, 2):
                duplicate_instruction_pairs.add(frozenset(instruction_pair))

    # Sort duplicate instruction pairs
    sorted_instruction_pairs = sorted(sorted(pair)
                                      for pair in duplicate_instruction_pairs)
    return sorted_instruction_pairs


# endregion
