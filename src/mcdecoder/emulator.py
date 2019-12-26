from dataclasses import dataclass
import re
from typing import List, Literal

from mcdecoder import core
# External functions


def emulate(mcfile: str, bit_pattern: str, base: Literal[2, 16] = None, byteorder: Literal['big', 'little'] = None) -> int:
    # Default
    if base is None:
        base = 2
    if byteorder is None:
        byteorder = 'big'

    # Emulate
    instruction_results = _emulate(mcfile, bit_pattern, base, byteorder)

    # Output results
    if len(instruction_results) > 0:
        # Output summary
        print(f'{len(instruction_results)} instructions detected.')

        for instruction_result in instruction_results:
            # Output about instruction
            print('-' * 80)
            print(f'instruction: {instruction_result.decoder.name}\n')

            # Output about fields
            for field_result in instruction_result.field_results:
                print(
                    f'{field_result.decoder.name}: {field_result.value}, {field_result.value:#x}, {field_result.value:#b}')
    else:
        print('No instructions detected.')
    
    return 0


# Internal classes


@dataclass
class _DecodeContext:
    mcdecoder: core.McDecoder
    code16: int
    code32: int


@dataclass
class _InstructionFieldDecodeResult:
    decoder: core.InstructionFieldDecoder
    value: int


@dataclass
class _InstructionDecodeResult:
    decoder: core.InstructionDecoder
    field_results: List[_InstructionFieldDecodeResult]


# Internal functions

def _emulate(mcfile: str, bit_pattern: str, base: Literal[2, 16], byteorder: Literal['big', 'little']) -> List[_InstructionDecodeResult]:
    # Create MC decoder model
    mcdecoder = core.create_mcdecoder_model(mcfile)

    # Trim whitespaces
    trimmed_bit_pattern = re.sub(r'\s', '', bit_pattern)

    # Pad 0 if bit pattern < 32 bits
    byte_str_len = _string_length_for_byte(base)
    pad_len = max(byte_str_len * 4 - len(trimmed_bit_pattern), 0)
    padded_bit_pattern = trimmed_bit_pattern + '0' * pad_len

    # Convert bit pattern to int based on the specified byteorder
    code16 = _bit_pattern_to_int(
        padded_bit_pattern[:byte_str_len * 2], base, byteorder)
    code32 = _bit_pattern_to_int(
        padded_bit_pattern[:byte_str_len * 4], base, byteorder)

    # Create decode context
    decode_context = _DecodeContext(
        mcdecoder=mcdecoder, code16=code16, code32=code32)

    # Emulate decoder
    return _emulate_decoder(decode_context)


def _emulate_decoder(context: _DecodeContext) -> List[_InstructionDecodeResult]:
    matched_decoders = _find_matched_instructions(context)
    return [_decode_instruction(context, instruction_decoder) for instruction_decoder in matched_decoders]


def _decode_instruction(context: _DecodeContext, instruction_decoder: core.InstructionDecoder) -> _InstructionDecodeResult:
    code = _get_appropriate_code(context, instruction_decoder)

    field_results: List[_InstructionFieldDecodeResult] = []
    for field_decoder in instruction_decoder.field_decoders:
        value = _decode_field(code, field_decoder)
        field_results.append(_InstructionFieldDecodeResult(
            decoder=field_decoder, value=value))

    return _InstructionDecodeResult(decoder=instruction_decoder, field_results=field_results)


def _decode_field(code: int, field_decoder: core.InstructionFieldDecoder) -> int:
    value = 0
    for sf_decoder in field_decoder.subfield_decoders:
        value |= ((code & sf_decoder.mask) >>
                  sf_decoder.end_bit_in_instruction) << sf_decoder.end_bit_in_field
    return value


def _find_matched_instructions(context: _DecodeContext) -> List[core.InstructionDecoder]:
    matched_decoders: List[core.InstructionDecoder] = []

    for instruction_decoder in context.mcdecoder.instruction_decoders:
        code = _get_appropriate_code(context, instruction_decoder)
        if (code & instruction_decoder.fixed_bits_mask) != instruction_decoder.fixed_bits:
            continue
        if not _test_instruction_conditions(code, instruction_decoder):
            continue

        matched_decoders.append(instruction_decoder)

    return matched_decoders


def _test_instruction_conditions(code: int, instruction_decoder: core.InstructionDecoder) -> bool:
    for condition in instruction_decoder.conditions:
        if not _test_instruction_condition(code, condition, instruction_decoder):
            return False

    return True


def _test_instruction_condition(code: int, condition: core.InstructionDecodeCondition, instruction_decoder: core.InstructionDecoder) -> bool:
    if isinstance(condition, core.EqualityInstructionDecodeCondition):
        field_decoder = next((field for field in instruction_decoder.field_decoders if field.name ==
                              condition.field), None)
        if field_decoder is None:
            return False

        value = _decode_field(code, field_decoder)
        if condition.operator == '!=':
            return value != condition.value
        elif condition.operator == '<':
            return value < condition.value
        elif condition.operator == '<=':
            return value <= condition.value
        elif condition.operator == '>':
            return value > condition.value
        elif condition.operator == '>=':
            return value >= condition.value
        else:
            return False

    elif isinstance(condition, core.InRangeInstructionDecodeCondition):
        field_decoder = next((field for field in instruction_decoder.field_decoders if field.name ==
                              condition.field), None)
        if field_decoder is None:
            return False

        value = _decode_field(code, field_decoder)
        return value >= condition.value_start and value <= condition.value_end

    else:
        return False


def _get_appropriate_code(context: _DecodeContext, instruction_decoder: core.InstructionDecoder) -> int:
    if instruction_decoder.type_bit_size == 16:
        return context.code16
    else:
        return context.code32


def _bit_pattern_to_int(bit_pattern: str, base: Literal[2, 16], byteorder: Literal['big', 'little']) -> int:
    # Convert bit pattern to int
    if byteorder == 'big':
        return int(bit_pattern, base)
    else:  # byteorder == 'little'
        # Character length that corresponds to a byte
        byte_str_len = _string_length_for_byte(base)

        # Pad 0 if bit pattern is fragmented for a byte
        pad_len = (len(bit_pattern) // byte_str_len *
                   byte_str_len + byte_str_len - len(bit_pattern)) % byte_str_len
        padded_bit_pattern = '0' * pad_len + bit_pattern

        # Little endian to big endian
        converted_bit_pattern = ''.join(bit_pattern[pos:pos+byte_str_len]
                                        for pos in range(len(padded_bit_pattern) - byte_str_len, -1, -byte_str_len))

        return int(converted_bit_pattern, base)


def _string_length_for_byte(base: Literal[2, 16]) -> int:
    """Calculate a string length that corresponds to a byte"""
    return 8 if base == 2 else 2


def _make_mask(bit_size: int) -> int:
    return (1 << bit_size) - 1
