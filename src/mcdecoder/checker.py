from dataclasses import dataclass
import itertools
import re
from typing import Callable, FrozenSet, Iterable, List, Literal, Optional, Set

from mcdecoder import common, core


# External functions


def check(mcfile: str, bit_pattern: str, base: Literal[2, 16] = None) -> int:
    # Default
    if base is None:
        base = 16

    # Check and output results
    print('-' * 80)
    print('Checking instructions...')
    result = _check(mcfile, bit_pattern, base, _output_error)
    print('Done.')

    print('-' * 80)
    print('Check result')
    print('-' * 80)
    print(f'''Count of bit patters with undefined instructions: {result.undefined_error_count:,}
Count of bit patters with duplicate instructions: {result.duplicate_error_count:,}
Count of duplicate instruction pairs: {len(result.duplicate_instruction_pairs):,}
Duplicate instructions:''')

    for instruction_pair in result.duplicate_instruction_pairs:
        instruction1, instruction2 = instruction_pair
        print(f'  {instruction1} - {instruction2}')

    return 0


# Internal classes


@dataclass
class _CheckResult:
    undefined_error_count: int
    duplicate_error_count: int
    duplicate_instruction_pairs: Set[FrozenSet[str]]


@dataclass
class _Error:
    type: Literal['undefined', 'duplicate']
    bits_start: int
    bits_end: int


@dataclass
class _VariableBitRange:
    mask: int
    shift: int


@dataclass
class _BitPattern:
    fixed_bits: int
    variable_bit_size: int
    variable_bit_ranges: List[_VariableBitRange]


# Internal functions


def _output_error(error: _Error) -> None:
    if error.type == 'undefined':
        print(
            f'{error.bits_start:#010x} - {error.bits_end:#010x}: Undefined (has no instructions)')
    elif error.type == 'duplicate':
        print(
            f'{error.bits_start:#010x} - {error.bits_end:#010x}: Duplicate (has duplicate instructions)')


def _check(mcfile: str, bit_pattern: str, base: Literal[2, 16], callback: Callable[[_Error], None]) -> _CheckResult:
    # Create MC decoder model
    mcdecoder = core.create_mcdecoder_model(mcfile)

    # Trim whitespaces
    trimmed_bit_pattern = common.trim_whitespace(bit_pattern)

    # Pad 0 if bit pattern < 32 bits
    padded_bit_pattern = common.pad_trailing_zeros(
        trimmed_bit_pattern, base, 32)

    # TODO Convert byteorder
    byte_str_len = common.string_length_for_byte(base)
    converted_bit_pattern = padded_bit_pattern[:byte_str_len * 4]

    # Parse bit pattern
    parsed_bit_pattern = _create_bit_pattern(converted_bit_pattern, base)

    # Check instructions
    return _check_instructions(mcdecoder, parsed_bit_pattern, callback)


def _check_instructions(mcdecoder: core.McDecoder, bit_pattern: _BitPattern, callback: Callable[[_Error], None]) -> _CheckResult:
    undefined_count = 0
    duplicate_count = 0
    duplicate_instruction_pairs: Set[FrozenSet[str]] = set()

    # Iterate over variable bits and emulate decoder
    decode_context = core.DecodeContext(
        mcdecoder=mcdecoder, code16=0, code32=0)

    ongoing_error: Optional[Literal['undefined', 'duplicate']] = None
    error_step_start = 0
    error_bits_start = 0
    prev_bits = 0
    prev_step = 0

    for step in range(0, 1 << bit_pattern.variable_bit_size):
        # Make bits to test
        bits = _make_bits(bit_pattern, step)
        decode_context.code32 = bits
        decode_context.code16 = bits >> 16

        # Emulate decode matching
        instruction_decoders = core.find_matched_instructions(decode_context)

        # Test if error exists
        if len(instruction_decoders) == 0:
            current_error = 'undefined'
        elif len(instruction_decoders) >= 2:
            current_error = 'duplicate'
            # TODO Save duplicate instruction pair
            for instruction_pair in itertools.combinations((instruction.name for instruction in instruction_decoders), 2):
                duplicate_instruction_pairs.add(frozenset(instruction_pair))
        else:
            current_error = None

        # Callback error if error status is changed
        if current_error != ongoing_error:
            if ongoing_error is not None:
                callback(_Error(type=ongoing_error,
                                bits_start=error_bits_start, bits_end=prev_bits))
                if ongoing_error == 'undefined':
                    undefined_count += prev_step - error_step_start + 1
                elif ongoing_error == 'duplicate':
                    duplicate_count += prev_step - error_step_start + 1

            ongoing_error = current_error
            error_step_start = step
            error_bits_start = bits

        # Save Previous status
        prev_step = step
        prev_bits = bits

    # Callback error if error left not reported
    if ongoing_error is not None:
        callback(_Error(type=ongoing_error,
                        bits_start=error_bits_start, bits_end=prev_bits))
        if ongoing_error == 'undefined':
            undefined_count += prev_step - error_step_start + 1
        elif ongoing_error == 'duplicate':
            duplicate_count += prev_step - error_step_start + 1

    # Create result
    return _CheckResult(undefined_error_count=undefined_count, duplicate_error_count=duplicate_count, duplicate_instruction_pairs=duplicate_instruction_pairs)


def _create_bit_pattern(bit_pattern: str, base: Literal[2, 16]) -> _BitPattern:
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


def _make_bits(bit_pattern: _BitPattern, step: int) -> int:
    bits = bit_pattern.fixed_bits
    for bit_range in bit_pattern.variable_bit_ranges:
        bits |= (step & bit_range.mask) << bit_range.shift
    return bits
