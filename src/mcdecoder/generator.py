import os
from typing import Any, Dict, List, NamedTuple, Optional, TypedDict, cast

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
class InstructionSubfieldDecoder(NamedTuple):
    index: int
    mask: int
    start_bit_in_instruction: int
    end_bit_in_instruction: int
    end_bit_in_field: int


class InstructionFieldDecoder(NamedTuple):
    name: str
    type_bit_size: int
    subfield_decoders: List[InstructionSubfieldDecoder]


class InstructionDecoder(NamedTuple):
    name: str
    fixed_bits_mask: int
    fixed_bits: int
    type_bit_size: int
    field_decoders: List[InstructionFieldDecoder]


class MachineDecoder(NamedTuple):
    namespace: Optional[str]


class McDecoder(NamedTuple):
    machine_decoder: MachineDecoder
    instruction_decoders: List[InstructionDecoder]


# Instruction format


class InstructionFieldFormat(NamedTuple):
    name: Optional[str]
    bits_format: str


class InstructionFormat(NamedTuple):
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

    # Create field decoders and build fixed bits information
    field_decoders: List[InstructionFieldDecoder] = []
    start_bit = instruction_bit_size - 1
    fixed_bits_mask = 0
    fixed_bits = 0

    for field_format in instruction_format.field_formats:
        # Calculate bit size and position
        field_bit_size = len(field_format.bits_format)
        end_bit = start_bit - field_bit_size + 1

        # Build field mask and fixed bits information
        field_mask = 0
        for bit_format in field_format.bits_format:
            if bit_format == 'x':
                fixed_bits_mask = (fixed_bits_mask << 1) | 0
                fixed_bits = (fixed_bits << 1) | 0
            else:
                fixed_bits_mask = (fixed_bits_mask << 1) | 1
                fixed_bits = (fixed_bits << 1) | int(bit_format)

            field_mask = (field_mask << 1) | 1

        field_mask <<= end_bit

        # Build field decoder for a named field
        if field_format.name is not None:
            field_decoder = InstructionFieldDecoder(
                name=field_format.name,
                type_bit_size=_calc_type_bit_size(field_bit_size),
                subfield_decoders=[InstructionSubfieldDecoder(index=0, mask=field_mask, start_bit_in_instruction=start_bit, end_bit_in_instruction=end_bit, end_bit_in_field=0)])
            field_decoders.append(field_decoder)

        # Change start bit to next field position
        start_bit -= field_bit_size

    # Create OP decoder model
    return InstructionDecoder(
        name=instruction_desc_model['name'],
        fixed_bits_mask=fixed_bits_mask,
        fixed_bits=fixed_bits,
        type_bit_size=_calc_type_bit_size(instruction_bit_size),
        field_decoders=field_decoders,
    )


def _calc_type_bit_size(bit_size: int) -> int:
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
    field_formats: List[Optional[str]] = field_format.split(':')
    bits_format, field_name = (field_formats + [None])[:2]
    return InstructionFieldFormat(
        name=field_name,
        bits_format=cast(str, bits_format),
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
