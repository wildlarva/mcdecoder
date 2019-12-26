from dataclasses import dataclass
import re
from typing import List

from mcdecoder import core
# External functions


def emulate(mcfile: str, bit_pattern: str, base: int = 2, byteorder: str = 'big'):
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
                    f'{field_result.decoder.name}: {field_result.value}(0x{field_result.value:x})')
    else:
        print('No instructions detected.')


# Internal classes


@dataclass
class _DecodeContext:
    mcdecoder: core.McDecoder
    code32: int
    code16: int


@dataclass
class _InstructionFieldDecodeResult:
    decoder: core.InstructionFieldDecoder
    value: int


@dataclass
class _InstructionDecodeResult:
    decoder: core.InstructionDecoder
    field_results: List[_InstructionFieldDecodeResult]


# Internal functions

def _emulate(mcfile: str, bit_pattern: str, base: int, byteorder: str) -> List[_InstructionDecodeResult]:
    # Create MC decoder model
    mcdecoder = core.create_mcdecoder_model(mcfile)

    # Parse bit_pattern
    trimmed_bit_pattern = re.sub(r'\s', '', bit_pattern)
    int_bit_pattern = _bit_pattern_to_int(
        trimmed_bit_pattern, base, byteorder)

    # Create decode context
    code32 = int_bit_pattern & _make_mask(32)
    code16 = int_bit_pattern & _make_mask(16)
    decode_context = _DecodeContext(
        mcdecoder=mcdecoder, code32=code32, code16=code16)

    # Emulate decoder
    return _emulate_decoder(decode_context)


def _emulate_decoder(context: _DecodeContext) -> List[_InstructionDecodeResult]:
    matched_decoders = _find_matched_instructions(context)
    return [_decode_instruction(context, instruction_decoder) for instruction_decoder in matched_decoders]


def _decode_instruction(context: _DecodeContext, instruction_decoder: core.InstructionDecoder) -> _InstructionDecodeResult:
    code = _get_appropriate_code(context, instruction_decoder)

    field_results: List[_InstructionFieldDecodeResult] = []
    for field_decoder in instruction_decoder.field_decoders:
        # Decode field
        value = 0
        for sf_decoder in field_decoder.subfield_decoders:
            value |= ((code & sf_decoder.mask) >>
                      sf_decoder.end_bit_in_instruction) << sf_decoder.end_bit_in_field

        field_results.append(_InstructionFieldDecodeResult(
            decoder=field_decoder, value=value))

    return _InstructionDecodeResult(decoder=instruction_decoder, field_results=field_results)


def _find_matched_instructions(context: _DecodeContext) -> List[core.InstructionDecoder]:
    matched_decoders: List[core.InstructionDecoder] = []
    for instruction_decoder in context.mcdecoder.instruction_decoders:
        code = _get_appropriate_code(context, instruction_decoder)
        if (code & instruction_decoder.fixed_bits_mask) == instruction_decoder.fixed_bits:
            matched_decoders.append(instruction_decoder)

    return matched_decoders


def _get_appropriate_code(context: _DecodeContext, instruction_decoder: core.InstructionDecoder) -> int:
    if instruction_decoder.type_bit_size == 16:
        return context.code16
    else:
        return context.code32


def _bit_pattern_to_int(bit_pattern: str, base: int, byteorder: str) -> int:
    # Convert bit pattern to int
    if byteorder == 'big':
        return int(bit_pattern, base)
    else:  # byteorder == 'little'
        # Character length that corresponds to a byte
        byte_chars_len = 8 if base == 2 else 2

        # Pad 0 if bit pattern is fragmented for a byte
        pad_len = len(bit_pattern) - (len(bit_pattern) % byte_chars_len)
        padded_bit_pattern = '0' * pad_len + bit_pattern

        # Little endian to big endian
        converted_bit_pattern = ''.join(bit_pattern[pos:pos+byte_chars_len]
                                        for pos in range(len(padded_bit_pattern) - byte_chars_len, -1, -byte_chars_len))

        return int(converted_bit_pattern, base)


def _make_mask(bit_size: int) -> int:
    return (1 << bit_size) - 1
