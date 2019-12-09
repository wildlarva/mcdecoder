import os
import yaml
import jinja2


def generate(mcfile_path):
    """Generate MC parser files from MC description file"""
    mcparser_model = _create_mcparser_model(mcfile_path)
    return _generate(mcparser_model)


def _create_mcparser_model(mcfile_path):
    """Create a model which contains information of MC parser"""
    with open(mcfile_path, 'rb') as file:
        mc_desc_model = yaml.load(file, Loader=yaml.Loader)

    op_parsers = list(map(lambda instruction_desc_model: _create_opparser_model(
        instruction_desc_model), mc_desc_model['instructions']))
    return {
        'parser': {},
        'op_parsers': op_parsers,
    }


def _create_opparser_model(instruction_desc_model):
    """Create a model which contains information of individual OP parser"""
    # Parse instruction format
    instruction_format = _parse_instruction_format(
        instruction_desc_model['format'])

    instruction_bit_size = sum(map(lambda arg_format: len(
        arg_format['bits_format']), instruction_format))

    # Create arg parsers and build fixed bits information
    arg_parsers = []
    start_bit = instruction_bit_size - 1
    fixed_bits_mask = 0
    fixed_bits = 0

    for arg_format in instruction_format:
        # Calculate bit size and position
        bit_size = len(arg_format['bits_format'])
        end_bit = start_bit - bit_size + 1

        # Build arg mask and fixed bits information
        arg_mask = 0
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

            arg_parser = {'name': arg_format['arg_name'],
                          'mask': arg_mask,
                          'start_bit': start_bit,
                          'end_bit': end_bit,
                          'type_bit_size': type_bit_size}
            arg_parsers.append(arg_parser)

        # Change start bit to next arg position
        start_bit -= bit_size

    # Create OP parser model
    opparser_model = {
        'name': instruction_desc_model['name'],
        'fixed_bits_mask': fixed_bits_mask,
        'fixed_bits': fixed_bits,
        'arg_parsers': arg_parsers,
    }
    return opparser_model


def _parse_instruction_format(instruction_format):
    """Parse an instruction format and returns an array of arg formats"""
    arg_formats = instruction_format.split('|')
    return list(map(lambda arg_format: _parse_arg_format(arg_format), arg_formats))


def _parse_arg_format(arg_format):
    """Parse an arg format and returns an arg format dictionary"""
    bits_format, arg_name = (arg_format.split(':') + [None])[:2]
    return {
        'bits_format': bits_format,
        'arg_name': arg_name,
    }


def _generate(mcparser_model):
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

    with open('out/mcparser.h', 'w') as file:
        file.write(parser_header_template.render(mcparser_model))

    with open('out/mcparser.c', 'w') as file:
        file.write(parser_source_template.render(mcparser_model))

    return True
