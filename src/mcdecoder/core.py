from dataclasses import dataclass
import importlib.resources
import json
from typing import Any, Dict, List, Optional, Tuple, TypedDict, cast

import jsonschema
import lark
import numpy as np
import yaml

# External classes

# MC description models loaded from yaml files


class InstructionDescrition(TypedDict):
    name: str
    format: str
    condition: Optional[Dict[str, str]]
    extras: Optional[Any]
    field_extras: Dict[str, Any]


class MachineDescription(TypedDict):
    extras: Optional[Any]


class McDecoderDescription(TypedDict):
    namespace: Optional[str]


class McDescription(TypedDict):
    machine: MachineDescription
    instructions: List[InstructionDescrition]
    decoder: Optional[McDecoderDescription]
    extras: Optional[Any]


# Decoder models
@dataclass
class InstructionSubfieldDecoder:
    """Decoder for a instruction subfield"""
    index: int
    """Index number of a subfield in a field: 0th to (n-1)th"""
    mask: int
    """Mask of a subfield in an instruction"""
    start_bit_in_instruction: int
    """MSB of a subfield in an instruction"""
    end_bit_in_instruction: int
    """LSB of a subfield in an instruction"""
    end_bit_in_field: int
    """LSB of a subfield in a field"""


@dataclass
class InstructionFieldDecoder:
    """Decoder for an instruction field"""
    name: str
    """Name of a field"""
    start_bit: int
    """MSB of a field"""
    type_bit_size: int
    """Bit size of data type used for a field"""
    subfield_decoders: List[InstructionSubfieldDecoder]
    """Subfield decoders"""
    extras: Optional[Any]
    """User-defined data for a field"""


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
    """Name of a field to be tested"""
    operator: str
    """Operator to test"""
    value: int
    """Value to be tested with"""
    type: str = 'equality'
    """Type of InstructionDecodeCondition"""


@dataclass
class InRangeInstructionDecodeCondition(InstructionDecodeCondition):
    """An in-range condition subclass for InstructionDecodeCondition to express an instruction field is in a value range(inclusive)"""
    field: str
    """Name of a field to be tested"""
    value_start: int
    """Start of a value range a field must be in"""
    value_end: int
    """End of a value range a field must be in"""
    type: str = 'in_range'
    """Type of InstructionDecodeCondition"""


@dataclass
class InstructionDecoder:
    """Decoder for an instruction"""
    name: str
    """Name of an instruction"""
    fixed_bits_mask: int
    """Mask of fixed bit positions of an instruction"""
    fixed_bits: int
    """Fixed bits of an instruction"""
    type_bit_size: int
    """Bit size of a data type used for an instruction"""
    conditions: List[InstructionDecodeCondition]
    """Conditions an instruction must be satisfy"""
    field_decoders: List[InstructionFieldDecoder]
    """Field decoders"""
    extras: Optional[Any]
    """User-defined data for an instruction"""


@dataclass
class MachineDecoder:
    """Decoder for a machine"""
    extras: Optional[Any]
    """User-defined data for a machine"""


@dataclass
class McDecoder:
    """Decoder itself. The root model element of MC decoder model"""
    namespace_prefix: str
    """Namespace prefix of generated codes"""
    machine_decoder: MachineDecoder
    """Machine decoder"""
    instruction_decoders: List[InstructionDecoder]
    """Instruction decoders"""
    extras: Optional[Any]
    """User-defined data not related to a machine, an instruction and a field"""


# Instruction condition
@dataclass
class InstructionCondition:
    field: str
    operator: str
    values: List[int]


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


# Decode emulation


@dataclass
class DecodeContext:
    mcdecoder: McDecoder
    code16: int
    code32: int


@dataclass
class DecodeContextVectorized:
    mcdecoder: McDecoder
    """McDecoder used for decoding"""
    code16_vec: np.ndarray
    """N-vector of 16-bit codes. The length of this code16 and code32 must be the same"""
    code32_vec: np.ndarray
    """N-vector of 32-bit codes. The length of this code16 and code32 must be the same"""


@dataclass
class InstructionFieldDecodeResult:
    decoder: InstructionFieldDecoder
    value: int


@dataclass
class InstructionDecodeResult:
    decoder: InstructionDecoder
    field_results: List[InstructionFieldDecodeResult]


# External functions


def create_mcdecoder_model(mcfile_path: str) -> McDecoder:
    """Create a model which contains information of MC decoder"""
    # Load MC description
    mc_desc_model = load_mc_description_model(mcfile_path)

    # Create machine and instruction decoders
    machine_decoder = _create_machine_decoder_model(mc_desc_model['machine'])
    instruction_decoders = [_create_instruction_decoder_model(
        instruction_desc_model) for instruction_desc_model in mc_desc_model['instructions']]

    # Create MC decoder
    namespace: Optional[str] = None
    if 'decoder' in mc_desc_model:
        decoder_desc_model = mc_desc_model['decoder']
        if 'namespace' in decoder_desc_model:
            namespace = decoder_desc_model['namespace']

    extras = mc_desc_model['extras'] if 'extras' in mc_desc_model else None
    return McDecoder(
        namespace_prefix=_make_namespace_prefix(namespace),
        machine_decoder=machine_decoder,
        instruction_decoders=instruction_decoders,
        extras=extras,
    )


def load_mc_description_model(mcfile_path: str) -> McDescription:
    # Load MC description
    with open(mcfile_path, 'rb') as file:
        mc_desc_model = yaml.load(file, Loader=yaml.Loader)

    # Validate
    _validate_mc_desc_model(mc_desc_model)

    return cast(McDescription, mc_desc_model)


def parse_instruction_format(instruction_format: str) -> InstructionFormat:
    """Parse an instruction format and returns an array of field formats"""
    with importlib.resources.open_text('mcdecoder.grammars', 'instruction_format.lark') as file:
        parser = lark.Lark(file, start='instruction_format')

    parsed_tree = parser.parse(instruction_format)
    return cast(InstructionFormat, _InstructionFormatTransformer(None).transform(parsed_tree))


def calc_instruction_bit_size(instruction_format: InstructionFormat) -> int:
    return sum(map(lambda field_format: len(
        field_format.bits_format), instruction_format.field_formats))


def find_matched_instructions(context: DecodeContext) -> List[InstructionDecoder]:
    matched_decoders: List[InstructionDecoder] = []

    for instruction_decoder in context.mcdecoder.instruction_decoders:
        # Get appripriate code
        # Do not use _get_appropriate_code() for performance
        if instruction_decoder.type_bit_size == 16:
            code = context.code16
        else:
            code = context.code32

        # Test if instruction is matched to code
        if (code & instruction_decoder.fixed_bits_mask) != instruction_decoder.fixed_bits:
            continue
        if not _test_instruction_conditions(code, instruction_decoder):
            continue

        # Add matched instruction
        matched_decoders.append(instruction_decoder)

    return matched_decoders


def find_matched_instructions_vectorized(context: DecodeContextVectorized) -> np.ndarray:
    """
    Find all the matched instructions to vectorized codes and return matched instructin matrix.

    :param context: context information of matching instructions
    :return: N x M matrix of codes(N) and instructions(M). Each element holds the boolean result whether a code is matched for an instruction.
    """
    # Vectorize the attributes of instruction decoders
    instruction_fields_matrix = np.array([(instruction.type_bit_size, instruction.fixed_bits_mask, instruction.fixed_bits) for instruction in context.mcdecoder.instruction_decoders])

    type_bit_size_vec = instruction_fields_matrix[:, 0]
    fixed_bits_mask_vec = instruction_fields_matrix[:, 1]
    fixed_bits_vec = instruction_fields_matrix[:, 2]

    # N x M matrix of codes and instructions holding code values
    code_mat: np.ndarray = np.where(type_bit_size_vec == 16, context.code16_vec.reshape(context.code16_vec.shape[0], 1), context.code32_vec.reshape(context.code16_vec.shape[0], 1))

    # N x M matrix of codes and instructions holding fixed bits test boolean values
    fb_test_mat = (code_mat & fixed_bits_mask_vec) == fixed_bits_vec

    test_mat = fb_test_mat
    for i, instruction_decoder in enumerate(context.mcdecoder.instruction_decoders):
        test_vec = _test_instruction_conditions_vectorized(code_mat[:, i], instruction_decoder)
        test_mat[:, i] = np.logical_and(test_mat[:, i], test_vec)

    return test_mat


def decode_instruction(context: DecodeContext, instruction_decoder: InstructionDecoder) -> InstructionDecodeResult:
    code = _get_appropriate_code(context, instruction_decoder)

    field_results: List[InstructionFieldDecodeResult] = []
    for field_decoder in instruction_decoder.field_decoders:
        value = _decode_field(code, field_decoder)
        field_results.append(InstructionFieldDecodeResult(
            decoder=field_decoder, value=value))

    return InstructionDecodeResult(decoder=instruction_decoder, field_results=field_results)


# Internal classes


@lark.v_args(inline=True)
class _InstructionFormatTransformer(lark.Transformer):
    @lark.v_args(inline=False)
    def instruction_format(self, field_formats: List[InstructionFieldFormat]) -> InstructionFormat:
        return InstructionFormat(field_formats=field_formats)

    def field_format(self, field_bits: str, field_name: str = None, field_bit_ranges: List[BitRange] = None) -> InstructionFieldFormat:
        if field_bit_ranges is None:
            field_bit_ranges = [BitRange(start=len(field_bits) - 1, end=0)]

        return InstructionFieldFormat(name=field_name, bits_format=field_bits, bit_ranges=field_bit_ranges)

    @lark.v_args(inline=False)
    def field_bits(self, field_bits_tokens: List[lark.Token]) -> str:
        return ''.join(field_bits_tokens)

    @lark.v_args(inline=False)
    def field_bit_ranges(self, field_bit_ranges: List[BitRange]) -> List[BitRange]:
        return field_bit_ranges

    def field_bit_range(self, subfield_start: int, subfield_end: int = None) -> BitRange:
        if subfield_end is None:
            subfield_end = subfield_start
        return BitRange(start=subfield_start, end=subfield_end)

    def id(self, id_token: lark.Token) -> str:
        return str(id_token)

    def number(self, number_token: lark.Token) -> int:
        return int(number_token)

    # NOTE: Pyright detects error without arguments for __init__
    def __init__(self, dummy: Any) -> None:
        pass


@lark.v_args(inline=True)
class _InstructionConditionTransformer(lark.Transformer):
    _field: str

    def equality_condition(self, equality_op: str, value: int) -> InstructionCondition:
        return InstructionCondition(field=self._field, operator=equality_op, values=[value])

    def in_range_condition(self, value_start: int, value_end: int) -> InstructionCondition:
        return InstructionCondition(field=self._field, operator='in_range', values=[value_start, value_end])

    def equality_op(self, equality_op_token: lark.Token) -> str:
        return str(equality_op_token)

    def number(self, number_token: lark.Token) -> int:
        return int(number_token)

    def __init__(self, field: str) -> None:
        self._field = field


# Internal functions


def _validate_mc_desc_model(mc_desc_model: Any) -> None:
    with importlib.resources.open_text('mcdecoder.schemas', 'mc_schema.json') as file:
        schema = json.load(file)

    jsonschema.validate(mc_desc_model, schema)


def _create_machine_decoder_model(machine_desc_model: MachineDescription) -> MachineDecoder:
    extras: Optional[Any] = None
    if 'extras' in machine_desc_model:
        extras = machine_desc_model['extras']

    return MachineDecoder(extras=extras)


def _make_namespace_prefix(namespace: Optional[str]) -> str:
    return namespace + '_' if namespace is not None else ''


def _create_instruction_decoder_model(instruction_desc_model: InstructionDescrition) -> InstructionDecoder:
    """Create a model which contains information of individual instruction decoder"""
    # Parse instruction format
    instruction_format = parse_instruction_format(
        instruction_desc_model['format'])
    instruction_bit_size = calc_instruction_bit_size(instruction_format)

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
    field_extras_dict: Dict[str,
                            Any] = instruction_desc_model['field_extras'] if 'field_extras' in instruction_desc_model else {}
    field_decoders = []

    for field_name in field_names:
        field_extras = field_extras_dict[field_name] if field_name in field_extras_dict else None
        field_decoder = _create_field_decoder(
            field_name, field_extras, instruction_format, ff_index_to_start_bit)
        field_decoders.append(field_decoder)

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
    instruction_extras = instruction_desc_model['extras'] if 'extras' in instruction_desc_model else None

    return InstructionDecoder(
        name=instruction_desc_model['name'],
        fixed_bits_mask=fixed_bits_mask,
        fixed_bits=fixed_bits,
        type_bit_size=_calc_type_bit_size(instruction_bit_size),
        field_decoders=field_decoders,
        conditions=decode_conditions,
        extras=instruction_extras,
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


def _create_field_decoder(field_name: str, field_extras: Optional[Any], instruction_format: InstructionFormat, ff_index_to_start_bit: Dict[int, int]) -> InstructionFieldDecoder:
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
        subfield_decoders=sf_decoders,
        extras=field_extras)


def _calc_type_bit_size(bit_size: int) -> int:
    """Calculate the bit size of a data type which can express the given bit size"""
    if bit_size <= 8:
        return 8
    elif bit_size <= 16:
        return 16
    else:
        return 32


def _create_instruction_decode_condition(field: str, instruction_condition: str) -> InstructionDecodeCondition:
    condition = _parse_instruction_condition(field, instruction_condition)
    if condition.operator == 'in_range':
        return InRangeInstructionDecodeCondition(field=field, value_start=condition.values[0], value_end=condition.values[1])
    else:
        return EqualityInstructionDecodeCondition(field=field, operator=condition.operator, value=condition.values[0])


def _parse_instruction_condition(field: str, instruction_condition: str) -> InstructionCondition:
    """Parse an instruction condition and returns a parsed condition"""
    with importlib.resources.open_text('mcdecoder.grammars', 'instruction_condition.lark') as file:
        parser = lark.Lark(file, start='condition')

    parsed_tree = parser.parse(instruction_condition)
    return cast(InstructionCondition, _InstructionConditionTransformer(
        field).transform(parsed_tree))


def _test_instruction_conditions(code: int, instruction_decoder: InstructionDecoder) -> bool:
    for condition in instruction_decoder.conditions:
        if not _test_instruction_condition(code, condition, instruction_decoder):
            return False

    return True


def _test_instruction_condition(code: int, condition: InstructionDecodeCondition, instruction_decoder: InstructionDecoder) -> bool:
    if isinstance(condition, EqualityInstructionDecodeCondition):
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

    elif isinstance(condition, InRangeInstructionDecodeCondition):
        field_decoder = next((field for field in instruction_decoder.field_decoders if field.name ==
                              condition.field), None)
        if field_decoder is None:
            return False

        value = _decode_field(code, field_decoder)
        return value >= condition.value_start and value <= condition.value_end

    else:
        return False


def _decode_field(code: int, field_decoder: InstructionFieldDecoder) -> int:
    value = 0
    for sf_decoder in field_decoder.subfield_decoders:
        value |= ((code & sf_decoder.mask) >>
                  sf_decoder.end_bit_in_instruction) << sf_decoder.end_bit_in_field
    return value


def _get_appropriate_code(context: DecodeContext, instruction_decoder: InstructionDecoder) -> int:
    if instruction_decoder.type_bit_size == 16:
        return context.code16
    else:
        return context.code32


def _test_instruction_conditions_vectorized(code_vec: np.ndarray, instruction_decoder: InstructionDecoder) -> np.ndarray:
    total_test_vec = np.full((code_vec.shape[0]), True)
    for condition in instruction_decoder.conditions:
        test_vec: np.ndarray = _test_instruction_condition_vectorized(code_vec, condition, instruction_decoder)
        total_test_vec = np.logical_and(total_test_vec, test_vec)

    return total_test_vec


def _test_instruction_condition_vectorized(code_vec: np.ndarray, condition: InstructionDecodeCondition, instruction_decoder: InstructionDecoder) -> np.ndarray:
    if isinstance(condition, EqualityInstructionDecodeCondition):
        field_decoder = next((field for field in instruction_decoder.field_decoders if field.name ==
                              condition.field), None)
        if field_decoder is None:
            return np.full((code_vec.shape[0]), False)

        value = _decode_field_vectorized(code_vec, field_decoder)
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
            return np.full((code_vec.shape[0]), False)

    elif isinstance(condition, InRangeInstructionDecodeCondition):
        field_decoder = next((field for field in instruction_decoder.field_decoders if field.name ==
                              condition.field), None)
        if field_decoder is None:
            return np.full((code_vec.shape[0]), False)

        value = _decode_field_vectorized(code_vec, field_decoder)
        return np.logical_and(value >= condition.value_start, value <= condition.value_end)

    else:
        return np.full((code_vec.shape[0]), False)


def _decode_field_vectorized(code_vec: np.ndarray, field_decoder: InstructionFieldDecoder) -> np.ndarray:
    value = np.zeros(code_vec.shape[0], dtype=int)
    for sf_decoder in field_decoder.subfield_decoders:
        value |= ((code_vec & sf_decoder.mask) >>
                  sf_decoder.end_bit_in_instruction) << sf_decoder.end_bit_in_field
    return value
