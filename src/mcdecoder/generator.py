from dataclasses import dataclass
import os
import re
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, TypedDict, cast

import jinja2
import yaml

# MC description models loaded from yaml files


class InstructionDescrition(TypedDict):
    name: str
    format: str


class MachineDecoderDescription(TypedDict):
    namespace: Optional[str]


class MachineDescription(TypedDict):
    decoder: Optional[MachineDecoderDescription]


class McDescription(TypedDict):
    machine: MachineDescription
    instructions: List[InstructionDescrition]


# Decoder models
@dataclass
class InstructionSubfieldDecoder:
    index: int
    mask: int
    start_bit_in_instruction: int
    end_bit_in_instruction: int
    end_bit_in_field: int


@dataclass
class InstructionFieldDecoder:
    name: str
    start_bit: int
    type_bit_size: int
    subfield_decoders: List[InstructionSubfieldDecoder]


@dataclass
class InstructionDecoder:
    name: str
    fixed_bits_mask: int
    fixed_bits: int
    type_bit_size: int
    field_decoders: List[InstructionFieldDecoder]


@dataclass
class MachineDecoder:
    namespace: Optional[str]


@dataclass
class McDecoder:
    machine_decoder: MachineDecoder
    instruction_decoders: List[InstructionDecoder]


# Instruction format
@dataclass
class BitRange:
    start: int
    end: int


@dataclass
class InstructionFieldFormat:
    name: Optional[str]
    bits_format: str
    bit_ranges: List[BitRange]


@dataclass
class InstructionFormat:
    field_formats: List[InstructionFieldFormat]


# External functions


def generate(mcfile_path: str) -> bool:
    """Generate MC decoder files from MC description file"""
    mcdecoder_model = _create_mcdecoder_model(mcfile_path)
    return _generate(mcdecoder_model)


# Internal functions


def _create_mcdecoder_model(mcfile_path: str) -> McDecoder:
    """Create a model which contains information of MC decoder"""
    with open(mcfile_path, 'rb') as file:
        mc_desc_model = cast(
            McDescription, yaml.load(file, Loader=yaml.Loader))

    machine_decoder = _create_machine_decoder_model(mc_desc_model['machine'])
    instruction_decoders = [_create_instruction_decoder_model(
        instruction_desc_model) for instruction_desc_model in mc_desc_model['instructions']]
    return McDecoder(
        machine_decoder=machine_decoder,
        instruction_decoders=instruction_decoders,
    )


def _create_machine_decoder_model(machine_desc_model: MachineDescription) -> MachineDecoder:
    namespace: Optional[str] = None
    if 'decoder' in machine_desc_model:
        decoder_desc_model = machine_desc_model['decoder']
        if 'namespace' in decoder_desc_model:
            namespace = decoder_desc_model['namespace']

    return MachineDecoder(namespace=namespace)


def _create_instruction_decoder_model(instruction_desc_model: InstructionDescrition) -> InstructionDecoder:
    """Create a model which contains information of individual instruction decoder"""
    # Parse instruction format
    instruction_format = _parse_instruction_format(
        instruction_desc_model['format'])
    instruction_bit_size = sum(map(lambda field_format: len(
        field_format.bits_format), instruction_format.field_formats))

    # Build fixed bits information
    fixed_bits_mask, fixed_bits = _build_fixed_bits_info(instruction_format)

    # Save the start bit positions of field formats
    ff_start_bit_in_instruction = instruction_bit_size - 1
    ff_index_to_start_bit: Dict[int, int] = {}

    for field_format in instruction_format.field_formats:
        field_bit_size = len(field_format.bits_format)
        ff_index_to_start_bit[instruction_format.field_formats.index(
            field_format)] = ff_start_bit_in_instruction
        ff_start_bit_in_instruction -= field_bit_size

    # Create field decoders
    field_names = set(map(lambda field: cast(str, field.name), filter(
        lambda field: field.name is not None, instruction_format.field_formats)))
    field_decoders = [_create_field_decoder(
        field_name, instruction_format, ff_index_to_start_bit) for field_name in field_names]

    # Sort field decoders according to start bit position
    field_decoders = sorted(
        field_decoders, key=lambda field: field.start_bit, reverse=True)

    # Create instruction decoder model
    return InstructionDecoder(
        name=instruction_desc_model['name'],
        fixed_bits_mask=fixed_bits_mask,
        fixed_bits=fixed_bits,
        type_bit_size=_calc_type_bit_size(instruction_bit_size),
        field_decoders=field_decoders,
    )


def _build_fixed_bits_info(instruction_format: InstructionFormat) -> Tuple[int, int]:
    """Build fixed bits information and returns fixed_bits_mask and fixed_bits"""
    fixed_bits_mask = 0
    fixed_bits = 0

    for field_format in instruction_format.field_formats:
        for bit_format in field_format.bits_format:
            if bit_format == 'x':
                fixed_bits_mask = (fixed_bits_mask << 1) | 0
                fixed_bits = (fixed_bits << 1) | 0
            else:
                fixed_bits_mask = (fixed_bits_mask << 1) | 1
                fixed_bits = (fixed_bits << 1) | int(bit_format)

    return fixed_bits_mask, fixed_bits


def _create_field_decoder(field_name: str, instruction_format: InstructionFormat, ff_index_to_start_bit: Dict[int, int]) -> InstructionFieldDecoder:
    """Create a model which contains information of a instruction field decoder"""
    # Find related field formats
    field_formats = filter(lambda field: field.name ==
                           field_name, instruction_format.field_formats)

    # Create subfield decoders
    start_bit_in_field = 0
    field_start_bit_in_instruction = 0

    sf_decoders: List[InstructionSubfieldDecoder] = []
    sf_index = 0

    for field_format in field_formats:
        # Calculate bit position for the field format
        sf_start_bit_in_instruction = ff_index_to_start_bit[instruction_format.field_formats.index(
            field_format)]
        field_start_bit_in_instruction = max(
            field_start_bit_in_instruction, sf_start_bit_in_instruction)

        for bit_range in field_format.bit_ranges:
            # Calculate bit size and position for the subfield
            sf_bit_size = bit_range.start - bit_range.end + 1
            sf_end_bit_in_instruction = sf_start_bit_in_instruction - sf_bit_size + 1

            # Build subfield mask
            sf_mask = 0
            for _ in range(0, sf_bit_size):
                sf_mask = (sf_mask << 1) | 1

            sf_mask <<= sf_end_bit_in_instruction

            # Create subfield decoder
            sf_decoder = InstructionSubfieldDecoder(
                index=sf_index, mask=sf_mask, start_bit_in_instruction=sf_start_bit_in_instruction, end_bit_in_instruction=sf_end_bit_in_instruction, end_bit_in_field=bit_range.end)
            sf_decoders.append(sf_decoder)

            # Update the field start bit position
            start_bit_in_field = max(start_bit_in_field, bit_range.start)

            # Change status for the next subfield position
            sf_index += 1
            sf_start_bit_in_instruction -= sf_bit_size

    # Create field decoder
    return InstructionFieldDecoder(
        name=field_name,
        start_bit=field_start_bit_in_instruction,
        type_bit_size=_calc_type_bit_size(start_bit_in_field + 1),
        subfield_decoders=sf_decoders)


def _calc_type_bit_size(bit_size: int) -> int:
    """Calculate the bit size of a data type which can express the given bit size"""
    if bit_size <= 8:
        return 8
    elif bit_size <= 16:
        return 16
    else:
        return 32


def _parse_instruction_format(instruction_format: str) -> InstructionFormat:
    """Parse an instruction format and returns an array of field formats"""
    field_formats = instruction_format.split('|')
    return InstructionFormat(
        field_formats=[_parse_field_format(field_format) for field_format in field_formats])


def _parse_field_format(field_format: str) -> InstructionFieldFormat:
    """Parse an field format and returns an field format dictionary"""
    # Parse each construct of field format
    # <field_bits>:<field_name>[field_start:field_end, ...]
    matched = re.match(r'([01x]+)(:(\w+)(\[([\d:,]+)\])?)?', field_format)

    bits_format = matched.group(1)
    field_name = matched.group(3)
    field_bit_ranges_str = matched.group(5)

    # Parse bit ranges
    bit_ranges: List[BitRange] = []
    if field_bit_ranges_str is not None:
        field_bit_range_strs = field_bit_ranges_str.split(',')
        for field_bit_range_str in field_bit_range_strs:
            field_bit_start, field_bit_end = (
                cast(List[Optional[str]], field_bit_range_str.split(':')) + [None, None])[:2]
            if field_bit_end is not None:
                bit_range = BitRange(
                    start=int(cast(str, field_bit_start)), end=int(cast(str, field_bit_end)))
            else:
                bit_range = BitRange(start=int(cast(str, field_bit_start)), end=int(
                    cast(str, field_bit_start)))
            bit_ranges.append(bit_range)
    else:
        # If there are no bit ranges, treat as a single bit range
        bit_ranges.append(BitRange(start=len(bits_format) - 1, end=0))

    # Build field format model
    return InstructionFieldFormat(
        name=field_name,
        bits_format=bits_format,
        bit_ranges=bit_ranges,
    )


def _generate(mcdecoder_model: McDecoder) -> bool:
    """Generate MC decoder files from a MC decoder model"""
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('mcdecoder', 'templates')
    )
    decoder_header_template = env.get_template('mcdecoder.h')
    decoder_source_template = env.get_template('mcdecoder.c')

    if not os.path.exists('out'):
        os.mkdir('out')
    elif not os.path.isdir('out'):
        return False

    ns_prefix = _make_namespace_prefix(
        mcdecoder_model.machine_decoder.namespace)
    template_args = {
        'ns': ns_prefix,
        'instruction_decoders': mcdecoder_model.instruction_decoders
    }

    with open(f'out/{ns_prefix}mcdecoder.h', 'w') as file:
        file.write(decoder_header_template.render(template_args))

    with open(f'out/{ns_prefix}mcdecoder.c', 'w') as file:
        file.write(decoder_source_template.render(template_args))

    return True


def _make_namespace_prefix(namespace: Optional[str]) -> str:
    return namespace + '_' if namespace is not None else ''
