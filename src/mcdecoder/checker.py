from dataclasses import dataclass
import itertools
import re
import textwrap
from typing import Callable, FrozenSet, List, Literal, Optional, Set

from mcdecoder import common, core
import numpy as np

# External functions


def check(mcfile: str, bit_pattern: str, base: Literal[2, 16] = None) -> int:
    """
    Implementation of check sub-command.
    NOTE Currently, mcdecoder does not support little endian bit pattern
    """
    # Default
    if base is None:
        base = 16

    # Check and output progress
    print('-' * 80)
    print('Checking instructions...')
    result = _check(mcfile, bit_pattern, base, _output_error)
    print('Done.')

    # Sort duplicate instruction pairs
    sorted_instruction_pairs = sorted(sorted(pair)
                                      for pair in result.duplicate_instruction_pairs)

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

    if len(sorted_instruction_pairs) > 0:
        for instruction_pair in sorted_instruction_pairs:
            if len(instruction_pair) >= 2:
                instruction1, instruction2 = instruction_pair
            else:
                (instruction1,) = (instruction2,) = instruction_pair

            print(textwrap.indent(f'{instruction1} - {instruction2}', ' ' * 2))
    else:
        print(textwrap.indent('None', ' ' * 2))

    return 0


# Internal classes


@dataclass
class _CheckResult:
    """Final result of checking"""
    no_error_count: int
    undefined_error_count: int
    duplicate_error_count: int
    duplicate_instruction_pairs: Set[FrozenSet[str]]


@dataclass
class _Error:
    """Error reported while checking"""
    type: Literal['undefined', 'duplicate']
    bits_start: int
    bits_end: int


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


# Internal functions


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


def _check_instructions_vectorized(mcdecoder: core.McDecoder, bit_pattern: _BitPattern, callback: Callable[[List[_Error]], None]) -> _CheckResult:
    """
    Check instructions if they have any errors.
    Errors are reported through callback while checking.
    """
    VEC_SIZE = 1 << 16
    total_count = 1 << bit_pattern.variable_bit_size

    undefined_count = 0
    duplicate_count = 0

    # Iterate over variable bits and emulate decoder
    decode_context = core.DecodeContextVectorized(
        mcdecoder=mcdecoder, code16_vec=np.empty(()), code32_vec=np.empty(()))

    # N x M matrix of detected duplicates and instructions holding boolean whether an instruction is matched
    total_duplicate_instruction_mat = np.full(
        (1, len(mcdecoder.instruction_decoders)), False)

    ongoing_undefined_range: Optional[np.ndarray] = None
    ongoing_duplicate_range: Optional[np.ndarray] = None

    for step in range(0, total_count, VEC_SIZE):
        # Make bits to test
        step_end = min(step + VEC_SIZE, total_count) - 1
        step_vec = np.arange(step, step_end + 1)
        bits_vec = np.full((step_vec.shape[0]), bit_pattern.fixed_bits)
        for bit_range in bit_pattern.variable_bit_ranges:
            bits_vec |= (step_vec & bit_range.mask) << bit_range.shift

        decode_context.code32_vec = bits_vec
        decode_context.code16_vec = bits_vec >> 16

        # Emulate decode matching
        test_matrix = core.find_matched_instructions_vectorized(decode_context)
        matched_instruction_count_vec = np.sum(test_matrix, axis=1)

        # Combine step, bits and test result
        # N x (M+2) matrix of codes x (step, bits, test_result)
        test_matrix_with_header = np.hstack((step_vec.reshape(
            step_vec.shape[0], 1), bits_vec.reshape(bits_vec.shape[0], 1), test_matrix))

        # Collect errors
        errors: List[_Error] = []

        # Find undefined
        undefined_matrix = test_matrix_with_header[matched_instruction_count_vec == 0]
        undefined_ranges: Optional[List[np.ndarray]] = None
        if len(undefined_matrix) > 0:
            # Split ranges
            undefined_ranges = np.split(undefined_matrix, np.where(
                np.diff(undefined_matrix[:, 0]) != 1)[0]+1)

            # Concatenate ongoing undefined range
            if ongoing_undefined_range is not None:
                if undefined_ranges[0][0, 0] == ongoing_undefined_range[-1, 0] + 1:
                    undefined_ranges[0] = np.vstack(
                        (ongoing_undefined_range, undefined_ranges[0]))
                else:
                    undefined_ranges.insert(0, ongoing_undefined_range)

                ongoing_undefined_range = None
        else:
            # Use ongoing undefined range
            if ongoing_undefined_range is not None:
                undefined_ranges = [ongoing_undefined_range]
                ongoing_undefined_range = None

        if undefined_ranges is not None:
            # Save ongoing undefined range
            if undefined_ranges[-1][-1, 0] == step_end:
                ongoing_undefined_range = undefined_ranges[-1]
                undefined_ranges = undefined_ranges[:-1]

            # Create errors
            for undefined_range in undefined_ranges:
                error_step_start, error_bits_start = undefined_range[0, 0:2]
                error_step_end, error_bits_end = undefined_range[-1, 0:2]
                undefined_count += error_step_end - error_step_start + 1
                errors.append(
                    _Error(type='undefined', bits_start=error_bits_start, bits_end=error_bits_end))

        # Find duplicates
        duplicate_matrix = test_matrix_with_header[matched_instruction_count_vec >= 2]
        duplicate_ranges: Optional[List[np.ndarray]] = None
        if len(duplicate_matrix) > 0:
            # Save duplicate instruction pairs
            duplicate_instruction_matrix = np.unique(
                duplicate_matrix[:, 2:], axis=0) == 1
            total_duplicate_instruction_mat = np.vstack(
                (total_duplicate_instruction_mat, duplicate_instruction_matrix))

            # Split ranges
            duplicate_ranges = np.split(duplicate_matrix, np.where(
                np.diff(duplicate_matrix[:, 0]) != 1)[0]+1)

            # Concatenate ongoing duplicate range
            if ongoing_duplicate_range is not None:
                if duplicate_ranges[0][0, 0] == ongoing_duplicate_range[-1, 0] + 1:
                    duplicate_ranges[0] = np.vstack(
                        (ongoing_duplicate_range, duplicate_ranges[0]))
                else:
                    duplicate_ranges.insert(0, ongoing_duplicate_range)

                ongoing_duplicate_range = None
        else:
            # Use ongoing duplicate range
            if ongoing_duplicate_range is not None:
                duplicate_ranges = [ongoing_duplicate_range]
                ongoing_duplicate_range = None

        if duplicate_ranges is not None:
            # Save ongoing duplicate range
            if duplicate_ranges[-1][-1, 0] == step_end:
                ongoing_duplicate_range = duplicate_ranges[-1]
                duplicate_ranges = duplicate_ranges[:-1]

            # Create errors
            for duplicate_range in duplicate_ranges:
                error_step_start, error_bits_start = duplicate_range[0, 0:2]
                error_step_end, error_bits_end = duplicate_range[-1, 0:2]
                duplicate_count += error_step_end - error_step_start + 1
                errors.append(
                    _Error(type='duplicate', bits_start=error_bits_start, bits_end=error_bits_end))

        # Report errors
        if len(errors) > 0:
            errors = sorted(errors, key=lambda error: error.bits_start)
            callback(errors)

    # Handle left errors
    errors = []

    # Handle left undefined errors
    if ongoing_undefined_range is not None:
        # Create errors
        error_step_start, error_bits_start = ongoing_undefined_range[0, 0:2]
        error_step_end, error_bits_end = ongoing_undefined_range[-1, 0:2]
        undefined_count += error_step_end - error_step_start + 1
        errors.append(
            _Error(type='undefined', bits_start=error_bits_start, bits_end=error_bits_end))

    # Handle left duplicate errors
    if ongoing_duplicate_range is not None:
        # Create errors
        error_step_start, error_bits_start = ongoing_duplicate_range[0, 0:2]
        error_step_end, error_bits_end = ongoing_duplicate_range[-1, 0:2]
        duplicate_count += error_step_end - error_step_start + 1
        errors.append(
            _Error(type='duplicate', bits_start=error_bits_start, bits_end=error_bits_end))

    # Report errors
    if len(errors) > 0:
        errors = sorted(errors, key=lambda error: error.bits_start)
        callback(errors)

    # Find duplicate instruction pairs
    duplicate_instruction_pairs: Set[FrozenSet[str]] = set()

    total_duplicate_instruction_mat = total_duplicate_instruction_mat[1:]
    if len(total_duplicate_instruction_mat) > 0:
        total_duplicate_instruction_mat = np.unique(
            total_duplicate_instruction_mat, axis=0)
        instruction_name_vec = np.array(
            [instruction.name for instruction in mcdecoder.instruction_decoders])

        for matched_instruction_vec in total_duplicate_instruction_mat:
            instructions = instruction_name_vec[matched_instruction_vec]
            for instruction_pair in itertools.combinations(instructions, 2):
                duplicate_instruction_pairs.add(frozenset(instruction_pair))

    # Create result
    no_error_count = total_count - undefined_count - duplicate_count

    return _CheckResult(no_error_count=no_error_count, undefined_error_count=undefined_count, duplicate_error_count=duplicate_count, duplicate_instruction_pairs=duplicate_instruction_pairs)


def _create_bit_pattern(bit_pattern: str, base: Literal[2, 16]) -> _BitPattern:
    """Parse bit pattern"""
    char_bit_len = common.bit_length_of_character(base)
    fixed_bits = int(bit_pattern.replace('x', '0'), base)

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
