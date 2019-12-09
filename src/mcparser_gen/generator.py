import os
import yaml
import jinja2
from typing import Any, Dict, List, NamedTuple, Optional


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
    arg_parsers: List[ArgParser]


class McParser(NamedTuple):
    op_parsers: List[OpParser]


def generate(mcfile_path: str) -> bool:
    """Generate MC parser files from MC description file"""
    mcparser_model: McParser = _create_mcparser_model(mcfile_path)
    return _generate(mcparser_model)


def _create_mcparser_model(mcfile_path: str) -> McParser:
    """Create a model which contains information of MC parser"""
    with open(mcfile_path, 'rb') as file:
        mc_desc_model: Any = yaml.load(file, Loader=yaml.Loader)

    op_parsers: List[OpParser] = list(map(lambda instruction_desc_model: _create_opparser_model(
        instruction_desc_model), mc_desc_model['instructions']))
    return McParser(
        op_parsers=op_parsers,
    )


def _create_opparser_model(instruction_desc_model: Dict[str, Any]) -> OpParser:
    """Create a model which contains information of individual OP parser"""
    # Parse instruction format
    instruction_format: List[Dict[str, Any]] = _parse_instruction_format(
        instruction_desc_model['format'])

    instruction_bit_size: int = sum(map(lambda arg_format: len(
        arg_format['bits_format']), instruction_format))

    # Create arg parsers and build fixed bits information
    arg_parsers: List[ArgParser] = []
    start_bit: int = instruction_bit_size - 1
    fixed_bits_mask: int = 0
    fixed_bits: int = 0

    for arg_format in instruction_format:
        # Calculate bit size and position
        bit_size: int = len(arg_format['bits_format'])
        end_bit: int = start_bit - bit_size + 1

        # Build arg mask and fixed bits information
        arg_mask: int = 0
        for bit_format in arg_format['bits_format']:
            if bit_format == 'x':
                fixed_bits_mask = (fixed_bits_mask << 1) | 0
                fixed_bits = (fixed_bits << 1) | 0
            else:
                fixed_bits_mask = (fixed_bits_mask << 1) | 1
                fixed_bits = (fixed_bits << 1) | int(bit_format)

            arg_mask = (arg_mask << 1) | 1

        arg_mask <<= end_bit

        # Build arg parser for a named arg
        if arg_format['arg_name'] is not None:
            if bit_size <= 8:
                type_bit_size = 8
            elif bit_size <= 16:
                type_bit_size = 16
            else:
                type_bit_size = 32

            arg_parser = ArgParser(
                name=arg_format['arg_name'],
                mask=arg_mask,
                start_bit=start_bit,
                end_bit=end_bit,
                type_bit_size=type_bit_size)
            arg_parsers.append(arg_parser)

        # Change start bit to next arg position
        start_bit -= bit_size

    # Create OP parser model
    return OpParser(
        name=instruction_desc_model['name'],
        fixed_bits_mask=fixed_bits_mask,
        fixed_bits=fixed_bits,
        arg_parsers=arg_parsers,
    )


def _parse_instruction_format(instruction_format: str) -> List[Dict[str, Any]]:
    """Parse an instruction format and returns an array of arg formats"""
    arg_formats: List[str] = instruction_format.split('|')
    return list(map(lambda arg_format: _parse_arg_format(arg_format), arg_formats))


def _parse_arg_format(arg_format: str) -> Dict[str, Any]:
    """Parse an arg format and returns an arg format dictionary"""
    arg_formats: List[Optional[str]] = arg_format.split(':')
    bits_format, arg_name = (arg_formats + [None])[:2]
    return {
        'bits_format': bits_format,
        'arg_name': arg_name,
    }


def _generate(mcparser_model: McParser) -> bool:
    """Generate MC parser files from a MC parser model"""
    env: jinja2.Environment = jinja2.Environment(
        loader=jinja2.PackageLoader('mcparser_gen', 'templates')
    )
    parser_header_template: jinja2.Template = env.get_template('mcparser.h')
    parser_source_template: jinja2.Template = env.get_template('mcparser.c')

    if not os.path.exists('out'):
        os.mkdir('out')
    elif not os.path.isdir('out'):
        return False

    with open('out/mcparser.h', 'w') as file:
        file.write(parser_header_template.render(
            op_parsers=mcparser_model.op_parsers))

    with open('out/mcparser.c', 'w') as file:
        file.write(parser_source_template.render(
            op_parsers=mcparser_model.op_parsers))

    return True
