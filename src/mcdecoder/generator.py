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


# Parser models


class ArgParser(NamedTuple):
    name: str
    mask: int
    start_bit: int
    end_bit: int
    type_bit_size: int


class OpParser(NamedTuple):
    name: str
    fixed_bits_mask: int
    fixed_bits: int
    type_bit_size: int
    arg_parsers: List[ArgParser]


class MachineParser(NamedTuple):
    namespace: Optional[str]


class McParser(NamedTuple):
    machine_parser: MachineParser
    op_parsers: List[OpParser]


# Instruction format


class ArgFormat(NamedTuple):
    name: Optional[str]
    bits_format: str


class InstructionFormat(NamedTuple):
    arg_formats: List[ArgFormat]


# External functions


def generate(mcfile_path: str) -> bool:
    """Generate MC parser files from MC description file"""
    mcparser_model = _create_mcparser_model(mcfile_path)
    return _generate(mcparser_model)


# Internal functions


def _create_mcparser_model(mcfile_path: str) -> McParser:
    """Create a model which contains information of MC parser"""
    with open(mcfile_path, 'rb') as file:
        mc_desc_model = cast(
            McDescription, yaml.load(file, Loader=yaml.Loader))

    machine_parser = _create_machine_parser_model(mc_desc_model['machine'])
    op_parsers = [_create_opparser_model(
        instruction_desc_model) for instruction_desc_model in mc_desc_model['instructions']]
    return McParser(
        machine_parser=machine_parser,
        op_parsers=op_parsers,
    )


def _create_machine_parser_model(machine_desc_model: MachineDescription) -> MachineParser:
    namespace: Optional[str] = None
    if 'decoder' in machine_desc_model:
        decoder_desc_model = machine_desc_model['decoder']
        if 'namespace' in decoder_desc_model:
            namespace = decoder_desc_model['namespace']

    return MachineParser(namespace=namespace)


def _create_opparser_model(instruction_desc_model: InstructionDescrition) -> OpParser:
    """Create a model which contains information of individual OP parser"""
    # Parse instruction format
    instruction_format = _parse_instruction_format(
        instruction_desc_model['format'])

    instruction_bit_size = sum(map(lambda arg_format: len(
        arg_format.bits_format), instruction_format.arg_formats))

    # Create arg parsers and build fixed bits information
    arg_parsers: List[ArgParser] = []
    start_bit = instruction_bit_size - 1
    fixed_bits_mask = 0
    fixed_bits = 0

    for arg_format in instruction_format.arg_formats:
        # Calculate bit size and position
        arg_bit_size = len(arg_format.bits_format)
        end_bit = start_bit - arg_bit_size + 1

        # Build arg mask and fixed bits information
        arg_mask = 0
        for bit_format in arg_format.bits_format:
            if bit_format == 'x':
                fixed_bits_mask = (fixed_bits_mask << 1) | 0
                fixed_bits = (fixed_bits << 1) | 0
            else:
                fixed_bits_mask = (fixed_bits_mask << 1) | 1
                fixed_bits = (fixed_bits << 1) | int(bit_format)

            arg_mask = (arg_mask << 1) | 1

        arg_mask <<= end_bit

        # Build arg parser for a named arg
        if arg_format.name is not None:
            arg_parser = ArgParser(
                name=arg_format.name,
                mask=arg_mask,
                start_bit=start_bit,
                end_bit=end_bit,
                type_bit_size=_calc_type_bit_size(arg_bit_size))
            arg_parsers.append(arg_parser)

        # Change start bit to next arg position
        start_bit -= arg_bit_size

    # Create OP parser model
    return OpParser(
        name=instruction_desc_model['name'],
        fixed_bits_mask=fixed_bits_mask,
        fixed_bits=fixed_bits,
        type_bit_size=_calc_type_bit_size(instruction_bit_size),
        arg_parsers=arg_parsers,
    )


def _calc_type_bit_size(bit_size: int) -> int:
    if bit_size <= 8:
        return 8
    elif bit_size <= 16:
        return 16
    else:
        return 32


def _parse_instruction_format(instruction_format: str) -> InstructionFormat:
    """Parse an instruction format and returns an array of arg formats"""
    arg_formats = instruction_format.split('|')
    return InstructionFormat(
        arg_formats=[_parse_arg_format(arg_format) for arg_format in arg_formats])


def _parse_arg_format(arg_format: str) -> ArgFormat:
    """Parse an arg format and returns an arg format dictionary"""
    arg_formats: List[Optional[str]] = arg_format.split(':')
    bits_format, arg_name = (arg_formats + [None])[:2]
    return ArgFormat(
        name=arg_name,
        bits_format=cast(str, bits_format),
    )


def _generate(mcparser_model: McParser) -> bool:
    """Generate MC parser files from a MC parser model"""
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('mcparser_gen', 'templates')
    )
    parser_header_template = env.get_template('mcparser.h')
    parser_source_template = env.get_template('mcparser.c')

    if not os.path.exists('out'):
        os.mkdir('out')
    elif not os.path.isdir('out'):
        return False

    ns_prefix = _make_namespace_prefix(mcparser_model.machine_parser.namespace)
    template_args = {
        'ns': ns_prefix,
        'op_parsers': mcparser_model.op_parsers
    }

    with open(f'out/{ns_prefix}mcparser.h', 'w') as file:
        file.write(parser_header_template.render(template_args))

    with open(f'out/{ns_prefix}mcparser.c', 'w') as file:
        file.write(parser_source_template.render(template_args))

    return True

def _make_namespace_prefix(namespace: Optional[str]) -> str:
    return namespace + '_' if namespace is not None else ''