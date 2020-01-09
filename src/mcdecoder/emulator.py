from typing import List, Literal

from . import common, core

# External functions


def emulate(mcfile: str, bit_pattern: str, base: Literal[2, 16] = None, byteorder: Literal['big', 'little'] = None) -> int:
    """
    Implementation of the sub-command 'emulate'.

    Emulate a decoder and output the decoding result.

    If base is not specified, base 16 is used by default.
    If byteorder is not specified, big endian is used by default.

    :param mcfile: Path to an MC description
    :param bit_pattern: Binary/hex string to be decoded
    :param base: Base of integer that specifies the expression of bit_pattern
    :param byteorder: Byte order of bit_pattern
    :return: Exit code of mcdecoder
    """
    # Default
    if base is None:
        base = 16
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


# Internal functions

def _emulate(mcfile: str, bit_pattern: str, base: Literal[2, 16],
             byteorder: Literal['big', 'little']) -> List[core.InstructionDecodeResult]:
    # Create MC decoder model
    mcdecoder = core.create_mcdecoder_model(mcfile)

    # Trim whitespaces
    trimmed_bit_pattern = common.trim_whitespace(bit_pattern)

    # Pad 0 if bit pattern < 32 bits
    padded_bit_pattern = common.pad_trailing_zeros(
        trimmed_bit_pattern, base, 32)

    # Convert bit pattern to int based on the specified byteorder
    byte_str_len = common.string_length_for_byte(base)

    code16 = _bit_pattern_to_int(
        padded_bit_pattern[:byte_str_len * 2], base, byteorder)
    code32 = _bit_pattern_to_int(
        padded_bit_pattern[:byte_str_len * 4], base, byteorder)

    # Create decode context
    decode_context = core.DecodeContext(
        mcdecoder=mcdecoder, code16=code16, code32=code32)

    # Emulate decoder
    return _emulate_decoder(decode_context)


def _emulate_decoder(context: core.DecodeContext) -> List[core.InstructionDecodeResult]:
    matched_decoders = core.find_matched_instructions(context)
    return [core.decode_instruction(context, instruction_decoder) for instruction_decoder in matched_decoders]


def _bit_pattern_to_int(bit_pattern: str, base: Literal[2, 16], byteorder: Literal['big', 'little']) -> int:
    return int(common.convert_to_big_endian(bit_pattern, base, byteorder), base)
