from dataclasses import dataclass
import importlib.resources
import json
import os
import re
from typing import (
    Any, Dict, Iterable, List, NamedTuple, Optional, Tuple, TypedDict, Union,
    cast)

import jinja2
import jsonschema
import mcdecoder
import yaml

# MC description models loaded from yaml files


class InstructionDescrition(TypedDict):
    name: str
    format: str
    condition: Optional[Dict[str, str]]
    extras: Optional[Any]


class MachineDecoderDescription(TypedDict):
    namespace: Optional[str]


class MachineDescription(TypedDict):
    decoder: Optional[MachineDecoderDescription]
    extras: Optional[Any]


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
class InstructionDecodeCondition:
    """
    A condition of instruction encoding when an instruction applys.
    Each subclass must have a string attribute 'type' to express the type of a subclass.
    """


@dataclass
class EqualityInstructionDecodeCondition(InstructionDecodeCondition):
    """An equality condition subclass for InstructionDecodeCondition to express a field value's equality to a value like !=, >, >=, <, <=, etc."""
    field: str
    operator: str
    value: int
    type: str = 'equality'


@dataclass
class InRangeInstructionDecodeCondition(InstructionDecodeCondition):
    """An in-range condition subclass for InstructionDecodeCondition to express an instruction field is in a value range(inclusive)"""
    field: str
    value_start: int
    value_end: int
    type: str = 'in_range'


@dataclass
class InstructionDecoder:
    name: str
    fixed_bits_mask: int
    fixed_bits: int
    type_bit_size: int
    conditions: List[InstructionDecodeCondition]
    field_decoders: List[InstructionFieldDecoder]
    extras: Optional[Any]


@dataclass
class MachineDecoder:
    namespace: Optional[str]
    extras: Optional[Any]


@dataclass
class McDecoder:
    machine_decoder: MachineDecoder
    instruction_decoders: List[InstructionDecoder]


# Instruction condition
@dataclass
class InstructionCondition:
    field: str
    operator: str
    values: List[int]


@dataclass
class _InstructionConditionToken:
    kind: str
    value: Union[int, str]


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
    # Load MC description
    with open(mcfile_path, 'rb') as file:
        mc_desc_model = cast(
            McDescription, yaml.load(file, Loader=yaml.Loader))

    # Validate
    _validate_mc_desc_model(mc_desc_model)

    # Create decoder model
    machine_decoder = _create_machine_decoder_model(mc_desc_model['machine'])
    instruction_decoders = [_create_instruction_decoder_model(
        instruction_desc_model) for instruction_desc_model in mc_desc_model['instructions']]
    return McDecoder(
        machine_decoder=machine_decoder,
        instruction_decoders=instruction_decoders,
    )


def _validate_mc_desc_model(mc_desc_model: McDescription) -> None:
    with importlib.resources.open_text(mcdecoder, 'mc_schema.json') as file:
        schema = json.load(file)

    jsonschema.validate(mc_desc_model, schema)


def _create_machine_decoder_model(machine_desc_model: MachineDescription) -> MachineDecoder:
    namespace: Optional[str] = None
    if 'decoder' in machine_desc_model:
        decoder_desc_model = machine_desc_model['decoder']
        if 'namespace' in decoder_desc_model:
            namespace = decoder_desc_model['namespace']

    extras: Optional[Any] = None
    if 'extras' in machine_desc_model:
        extras = machine_desc_model['extras']

    return MachineDecoder(namespace=namespace, extras=extras)


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

    # Create instruction decode conditions
    if 'condition' in instruction_desc_model:
        decode_conditions = [_create_instruction_decode_condition(
            field, condition) for field, condition in instruction_desc_model['condition'].items()]
    else:
        decode_conditions = []

    # Create instruction decoder model
    extras: Optional[Any] = None
    if 'extras' in instruction_desc_model:
        extras = instruction_desc_model['extras']

    return InstructionDecoder(
        name=instruction_desc_model['name'],
        fixed_bits_mask=fixed_bits_mask,
        fixed_bits=fixed_bits,
        type_bit_size=_calc_type_bit_size(instruction_bit_size),
        field_decoders=field_decoders,
        conditions=decode_conditions,
        extras=extras,
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


def _create_instruction_decode_condition(field: str, instruction_condition: str) -> InstructionDecodeCondition:
    condition = _parse_instruction_condition(field, instruction_condition)
    if condition.operator == 'in_range':
        return InRangeInstructionDecodeCondition(field=field, value_start=condition.values[0], value_end=condition.values[1])
    else:
        return EqualityInstructionDecodeCondition(field=field, operator=condition.operator, value=condition.values[0])


def _parse_instruction_condition(field: str, instruction_condition: str) -> InstructionCondition:
    """Parse an instruction condition and returns a parsed condition"""
    tokens = _tokenize_instruction_condition(instruction_condition)

    # Must have 2 tokens at least
    if len(tokens) < 2:
        raise RuntimeError(
            f'Unexpected condition expression: {instruction_condition}')

    # The first token must be equality operator
    if tokens[0].kind != 'equality':
        raise RuntimeError(
            f'Unexpected condition expression: {instruction_condition}')

    operator = cast(str, tokens[0].value)

    # Specific parsing for each operator
    if operator == 'in_range':
        # in_range condition must have 4 tokens(operator, value start, range operator and value end)
        if len(tokens) != 4:
            raise RuntimeError(
                f'Unexpected condition expression: {instruction_condition}')

        _, value_start_token, range_token, value_end_token = tokens

        # Validate the token kinds
        if value_start_token.kind != 'number' or range_token.kind != 'range' or value_end_token.kind != 'number':
            raise RuntimeError(
                f'Unexpected condition expression: {instruction_condition}')

        values = [cast(int, value_start_token.value),
                  cast(int, value_end_token.value)]

    else:
        # Other operators must have 2 tokens(operator and value)
        if len(tokens) != 2:
            raise RuntimeError(
                f'Unexpected condition expression: {instruction_condition}')

        _, value_token = tokens

        # Validate the token kind
        if value_token.kind != 'number':
            raise RuntimeError(
                f'Unexpected condition expression: {instruction_condition}')

        values = [cast(int, value_token.value)]

    # Create instruction condition
    return InstructionCondition(field=field, operator=operator, values=values)


def _tokenize_instruction_condition(instruction_condition: str) -> List[_InstructionConditionToken]:
    # Define tokenizer specification
    operator_keywords = ['in_range', ]
    token_specification = [
        ('id', r'[A-Za-z]\w*'),  # Identifiers
        ('number', r'\d+'),  # Integer number
        ('range', r'-'),  # Range operator
        ('equality', r'!=|>|>=|<|<='),  # Equality operator
        ('skip', r'\s+'),  # Skip over spaces and tabs
        ('mismatch', r'.'),  # Any other character
    ]

    # Create tokenizer
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    # Tokenize
    tokens: List[_InstructionConditionToken] = []
    for mo in re.finditer(tok_regex, instruction_condition):
        kind = cast(str, mo.lastgroup)
        value = mo.group()
        if kind == 'id' and value in operator_keywords:
            kind = 'equality'
        elif kind == 'number':
            value = int(value)
        elif kind == 'range':
            pass
        elif kind == 'equality':
            pass
        elif kind == 'skip':
            continue
        elif kind == 'mismatch':
            raise RuntimeError(f'{value!r} unexpected')

        tokens.append(_InstructionConditionToken(kind=kind, value=value))

    return tokens


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
        'mc_decoder': mcdecoder_model,
        'machine_decoder': mcdecoder_model.machine_decoder,
        'instruction_decoders': mcdecoder_model.instruction_decoders,
        'ns': ns_prefix,
    }

    with open(f'out/{ns_prefix}mcdecoder.h', 'w') as file:
        file.write(decoder_header_template.render(template_args))

    with open(f'out/{ns_prefix}mcdecoder.c', 'w') as file:
        file.write(decoder_source_template.render(template_args))

    return True


def _make_namespace_prefix(namespace: Optional[str]) -> str:
    return namespace + '_' if namespace is not None else ''
