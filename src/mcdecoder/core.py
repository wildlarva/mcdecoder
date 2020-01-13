from dataclasses import dataclass
import glob
import importlib.resources
import itertools
import json
import os.path
from os.path import isfile
from typing import (
    Any, Callable, Dict, List, Literal, Optional, Tuple, TypedDict, cast)

import jsonschema
import lark
import numpy as np
import yaml

# region External classes

# region MC description models loaded from yaml files


class InstructionDescription(TypedDict):
    """Describes an instruction"""
    name: str
    """Name of an instruction"""
    format: str
    """Encoding format of an instruction"""
    match_condition: Optional[str]
    """Condition an instruction must satisfy"""
    unmatch_condition: Optional[str]
    """Condition an instruction must not satisfy"""
    extras: Optional[Any]
    """Container of user-defined data for an instruction"""
    field_extras: Optional[Dict[str, Any]]
    """Container of user-defined data for each field"""


class MachineDescription(TypedDict):
    """Describes a machine"""
    extras: Optional[Any]
    """Container of user-defined data for a machine"""


class McDecoderDescription(TypedDict):
    """Decoder information that isn't related to a machine, an instruction and a field"""
    namespace: Optional[str]
    """Namespace for the symbols of a generated decoder"""


class McDescription(TypedDict):
    """Describes a machine code specification. The root element of MC description model"""
    machine: MachineDescription
    """Child MachineDescription"""
    instructions: List[InstructionDescription]
    """Child InstructionDescriptions"""
    decoder: Optional[McDecoderDescription]
    """Child McDecoderDescription"""
    extras: Optional[Any]
    """User-defined data not related to a machine, an instruction and a field"""

# endregion

# region MC description models parsed from string


@dataclass
class InstructionConditionObjectDescription:
    """Parsed object/subject in an instruction condition"""
    pass


@dataclass
class FieldInstructionConditionObjectDescription(InstructionConditionObjectDescription):
    """Field object/subject in an instruction condition"""
    field: str
    """Name of a field to be tested"""
    element_index: Optional[int]
    """Bit element index of a field to be tested"""


@dataclass
class ImmediateInstructionConditionObjectDescription(InstructionConditionObjectDescription):
    """Immediate value object/subject in an instruction condition"""
    value: int
    """Value to be tested"""


@dataclass
class FunctionInstructionConditionObjectDescription(InstructionConditionObjectDescription):
    """Uses the result of a function call as an object/subject in an instruction condition"""
    function: str
    """Name of a function to be called"""
    argument: FieldInstructionConditionObjectDescription
    """Argument FieldInstructionConditionObjectDescription"""


@dataclass
class InstructionConditionDescription:
    """Parsed condition of an instruction"""
    pass


@dataclass
class LogicalInstructionConditionDescription(InstructionConditionDescription):
    """Parsed logical condition of an instruction, 'and' or 'or'"""
    operator: Literal['and', 'or']
    """Operator of a logical condition"""
    conditions: List[InstructionConditionDescription]
    """Conditions combined with an logical operator"""


@dataclass
class EqualityInstructionConditionDescription(InstructionConditionDescription):
    """Parsed equality condition of an instruction such as '==', 'in', etc."""
    subject: InstructionConditionObjectDescription
    """Subjective InstructionConditionObjectDescription to be tested"""
    operator: str
    """Operator to test"""
    object: InstructionConditionObjectDescription
    """Objective InstructionConditionObjectDescription to test with"""


@dataclass
class InInstructionConditionDescription(InstructionConditionDescription):
    """Parsed 'in' condition of an instruction"""
    subject: InstructionConditionObjectDescription
    """Subjective InstructionConditionObjectDescription to be tested"""
    values: List[int]
    """Values to test with"""


@dataclass
class InRangeInstructionConditionDescription(InstructionConditionDescription):
    """Parsed 'in_range' condition of an instruction"""
    subject: InstructionConditionObjectDescription
    """Subjective InstructionConditionObjectDescription to be tested"""
    value_start: int
    """Start of a value range a field must be in"""
    value_end: int
    """End of a value range a field must be in"""


@dataclass
class BitRangeDescription:
    """Parsed bit range"""
    start: int
    """MSB of a bit range"""
    end: int
    """LSB of a bit range"""


@dataclass
class InstructionFieldFormatDescription:
    """Parsed encoding format of an instruction field"""
    name: Optional[str]
    """Name of a field"""
    bits_format: str
    """Encoding format of a field"""
    bit_ranges: List[BitRangeDescription]
    """Bit ranges of a field that the encoding format corresponds to"""


@dataclass
class InstructionFormatDescription:
    """Parsed encoding format of an instruction"""
    field_formats: List[InstructionFieldFormatDescription]
    """Child InstructionFieldFormatDescriptions"""

# endregion

# region Decoder models
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
    """MSB of a field in an instruction"""
    type_bit_size: int
    """Bit size of a data type used for a field"""
    subfield_decoders: List[InstructionSubfieldDecoder]
    """Child InstructionSubfieldDecoders"""
    extras: Optional[Any]
    """User-defined data for a field"""


@dataclass
class InstructionDecoderConditionObject:
    """
    Object or subject of InstructionDecoderCondition.

    Each subclass must have a string attribute 'type' to express the type of a subclass.
    """
    pass


@dataclass
class FieldIdConditionObject(InstructionDecoderConditionObject):
    """Field object/subject subclass for InstructionDecoderConditionObject"""
    field: str
    """Name of a field to be tested"""
    element_index: Optional[int]
    """Bit element index of a field to be tested"""
    type: str = 'field'
    """Type of InstructionDecoderConditionObject. It's always 'field' for FieldIdConditionObject"""


@dataclass
class ImmediateIdConditionObject(InstructionDecoderConditionObject):
    """Immediate value object/subject subclass for InstructionDecoderConditionObject"""
    value: int
    """Value to be tested"""
    type: str = 'immediate'
    """Type of InstructionDecoderConditionObject. It's always 'immediate' for ImmediateIdConditionObject"""


@dataclass
class FunctionIdConditionObject(InstructionDecoderConditionObject):
    """Uses the result of a function call as an object/subject. It is a subclass for InstructionDecoderConditionObject"""
    function: str
    """Name of a function to be called"""
    argument: FieldIdConditionObject
    """Argument FieldIdConditionObject"""
    type: str = 'function'
    """Type of InstructionDecoderConditionObject. It's always 'function' for FunctionIdConditionObject"""


@dataclass
class InstructionDecoderCondition:
    """
    Condition of instruction encoding when an instruction applys.

    Each subclass must have a string attribute 'type' to express the type of a subclass.
    """
    pass


@dataclass
class AndIdCondition(InstructionDecoderCondition):
    """'and' condition subclass for InstructionDecoderCondition to combine conditions with AND operator"""
    conditions: List[InstructionDecoderCondition]
    """Child InstructionDecoderConditions combined with logical AND operation"""
    type: str = 'and'
    """Type of InstructionDecoderCondition. It's always 'and' for AndIdCondition"""


@dataclass
class OrIdCondition(InstructionDecoderCondition):
    """'or' condition subclass for InstructionDecoderCondition to combine conditions with OR operator"""
    conditions: List[InstructionDecoderCondition]
    """Child InstructionDecoderConditions combined with logical OR operation"""
    type: str = 'or'
    """Type of InstructionDecoderCondition. It's always 'or' for OrIdCondition"""


@dataclass
class EqualityIdCondition(InstructionDecoderCondition):
    """
    Equality condition subclass for InstructionDecoderCondition to test a field value's equality with a value.

    Supported operators are ==, !=, >, >=, < and <=.
    """
    subject: InstructionDecoderConditionObject
    """Subjective InstructionDecoderConditionObject to be tested"""
    operator: str
    """Operator to test"""
    object: InstructionDecoderConditionObject
    """Objective InstructionDecoderConditionObject to test with"""
    type: str = 'equality'
    """Type of InstructionDecoderCondition. It's always 'equality' for EqualityIdCondition"""


@dataclass
class InIdCondition(InstructionDecoderCondition):
    """'in' condition subclass for InstructionDecoderCondition to test an instruction field is in a value set"""
    subject: InstructionDecoderConditionObject
    """Subjective InstructionDecoderConditionObject to be tested"""
    values: List[int]
    """Value set a field must be in"""
    type: str = 'in'
    """Type of InstructionDecoderCondition. It's always 'in' for InIdCondition"""


@dataclass
class InRangeIdCondition(InstructionDecoderCondition):
    """
    'in_range' condition subclass for InstructionDecoderCondition
    to test an instruction field is in a value range(inclusive)
    """
    subject: InstructionDecoderConditionObject
    """Subjective InstructionDecoderConditionObject to be tested"""
    value_start: int
    """Start of a value range a field must be in"""
    value_end: int
    """End of a value range a field must be in"""
    type: str = 'in_range'
    """Type of InstructionDecoderCondition. It's always 'in_range' for InRangeIdCondition"""


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
    match_condition: Optional[InstructionDecoderCondition]
    """Condition an instruction must satisfy"""
    unmatch_condition: Optional[InstructionDecoderCondition]
    """Condition an instruction must not satisfy"""
    field_decoders: List[InstructionFieldDecoder]
    """Child InstructionFieldDecoders"""
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
    """Child MachineDecoder"""
    instruction_decoders: List[InstructionDecoder]
    """Child InstructionDecoders"""
    extras: Optional[Any]
    """User-defined data not related to a machine, an instruction and a field"""

# endregion

# region Decode emulation


@dataclass
class DecodeContext:
    """Context information while decoding. It is used for non-vectorized calculations."""
    mcdecoder: McDecoder
    """McDecoder used for decoding"""
    code16: int
    """16-bit code"""
    code32: int
    """32-bit code"""


@dataclass
class DecodeContextVectorized:
    """Context information while decoding. It is used for vectorized calculations"""
    mcdecoder: McDecoder
    """McDecoder used for decoding"""
    code16_vec: np.ndarray
    """N-vector of 16-bit codes. The length of code16_vec and code32_vec must be the same"""
    code32_vec: np.ndarray
    """N-vector of 32-bit codes. The length of code16_vec and code32_vec must be the same"""


@dataclass
class InstructionFieldDecodeResult:
    """Decoding result of an instruction field"""
    decoder: InstructionFieldDecoder
    """Corresponding InstructionFieldDecoder"""
    value: int
    """Decoded value for a field"""


@dataclass
class InstructionDecodeResult:
    """Decoding result of an instruction"""
    decoder: InstructionDecoder
    """Corresponding InstructionDecoder"""
    field_results: List[InstructionFieldDecodeResult]
    """Child InstructionFieldDecodeResults"""

# endregion

# endregion

# region External functions


def create_mcdecoder_model(mcfile_path: str) -> McDecoder:
    """
    Create a model which contains information of MC decoder

    :param mcfile_path: Path to an MC description file
    :return: Created McDecoder
    """
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
    """
    Load an MC description file and validate against the schema

    :param mcfile_path: Path to an MC description file
    :return: Loaded McDescription
    """
    # Load MC description
    _yaml_include_context.base_dir = os.path.dirname(mcfile_path)
    with open(mcfile_path, 'rb') as file:
        mc_desc_model = yaml.load(file, Loader=yaml.Loader)

    # Validate
    _validate_mc_desc_model(mc_desc_model)

    return cast(McDescription, mc_desc_model)


def parse_instruction_format(instruction_format: str) -> InstructionFormatDescription:
    """
    Parse a string of the encoding format of an instruction

    :param instruction_format: String of the encoding format of an instruction
    :return: Parsed InstructionFormatDescription
    """
    parsed_tree = _instruction_format_parser.parse(instruction_format)
    return cast(InstructionFormatDescription, _InstructionFormatDescriptionTransformer(None).transform(parsed_tree))


def calc_instruction_bit_size(instruction_format: InstructionFormatDescription) -> int:
    """
    Calculate the bit length of an instruction

    :param instruction_format: Calculation target
    :return: Bit length of an instruction
    """
    return sum(len(
        field_format.bits_format) for field_format in instruction_format.field_formats)


def find_matched_instructions(context: DecodeContext) -> List[InstructionDecoder]:
    """
    Find instructions matched with a given code

    :param context: Context information while decoding
    :return: Matched InstructionDecoders
    """
    context_vectorized = DecodeContextVectorized(mcdecoder=context.mcdecoder, code16_vec=np.array([
                                                 context.code16]), code32_vec=np.array([context.code32]))
    test_mat = find_matched_instructions_vectorized(context_vectorized)

    instruction_vec = np.array(
        context.mcdecoder.instruction_decoders, dtype=np.object)
    return list(instruction_vec[test_mat[0]])


def find_matched_instructions_vectorized(context: DecodeContextVectorized) -> np.ndarray:
    """
    Find all the matched instructions to vectorized codes and return matched instructin matrix.

    :param context: Context information while decoding
    :return: N x M matrix of codes(N) and instructions(M).
            Each element holds the boolean result whether a code is matched for an instruction.
    """
    # Vectorize the attributes of instruction decoders
    instruction_fields_mat = np.array([(instruction.type_bit_size, instruction.fixed_bits_mask,
                                        instruction.fixed_bits) for instruction in context.mcdecoder.instruction_decoders])

    type_bit_size_vec = instruction_fields_mat[:, 0]
    fixed_bits_mask_vec = instruction_fields_mat[:, 1]
    fixed_bits_vec = instruction_fields_mat[:, 2]

    # N x M matrix of codes and instructions holding code values
    code_mat: np.ndarray = np.where(type_bit_size_vec == 16, context.code16_vec.reshape(
        context.code16_vec.shape[0], 1), context.code32_vec.reshape(context.code32_vec.shape[0], 1))

    # N x M matrix of codes and instructions holding fixed bits test boolean values
    fb_test_mat = (code_mat & fixed_bits_mask_vec) == fixed_bits_vec

    test_mat = fb_test_mat
    for i, instruction_decoder in enumerate(context.mcdecoder.instruction_decoders):
        if instruction_decoder.match_condition is not None:
            test_vec = _test_instruction_condition_vectorized(
                code_mat[:, i], instruction_decoder.match_condition, instruction_decoder)
            test_mat[:, i] = np.logical_and(  # type: ignore # TODO pyright can't recognize numpy.logical_and
                test_mat[:, i], test_vec)

        elif instruction_decoder.unmatch_condition is not None:
            test_vec = np.logical_not(  # type: ignore # TODO pyright can't recognize numpy.logical_not
                _test_instruction_condition_vectorized(code_mat[:, i], instruction_decoder.unmatch_condition,
                                                       instruction_decoder))
            test_mat[:, i] = np.logical_and(  # type: ignore # TODO pyright can't recognize numpy.logical_and
                test_mat[:, i], test_vec)

    return test_mat


def decode_instruction(context: DecodeContext, instruction_decoder: InstructionDecoder) -> InstructionDecodeResult:
    """
    Decode an instruction

    :param context: Context information while decoding
    :param instruction_decoder: InstructionDecoder to decode with
    :return: InstructionDecodeResult
    """
    code = _get_appropriate_code(context, instruction_decoder)

    field_results: List[InstructionFieldDecodeResult] = []
    for field_decoder in instruction_decoder.field_decoders:
        value = _decode_field(code, field_decoder)
        field_results.append(InstructionFieldDecodeResult(
            decoder=field_decoder, value=value))

    return InstructionDecodeResult(decoder=instruction_decoder, field_results=field_results)

# endregion

# region Internal classes


@dataclass
class _YamlIncludeContext:
    """Context information for YAML !include tag"""
    base_dir: str
    """Base directory for !include tag"""


@lark.v_args(inline=True)
class _InstructionFormatDescriptionTransformer(lark.Transformer):
    @lark.v_args(inline=False)
    def instruction_format(self, field_formats: List[InstructionFieldFormatDescription]) -> InstructionFormatDescription:
        return InstructionFormatDescription(field_formats=field_formats)

    def field_format(self, field_bits: str, field_name: str = None,
                     field_bit_ranges: List[BitRangeDescription] = None) -> InstructionFieldFormatDescription:
        if field_bit_ranges is None:
            field_bit_ranges = [BitRangeDescription(
                start=len(field_bits) - 1, end=0)]

        return InstructionFieldFormatDescription(name=field_name, bits_format=field_bits, bit_ranges=field_bit_ranges)

    @lark.v_args(inline=False)
    def field_bits(self, field_bits_tokens: List[lark.Token]) -> str:
        return ''.join(field_bits_tokens)

    @lark.v_args(inline=False)
    def field_bit_ranges(self, field_bit_ranges: List[BitRangeDescription]) -> List[BitRangeDescription]:
        return field_bit_ranges

    def field_bit_range(self, subfield_start: int, subfield_end: int = None) -> BitRangeDescription:
        if subfield_end is None:
            subfield_end = subfield_start
        return BitRangeDescription(start=subfield_start, end=subfield_end)

    def id(self, id_token: lark.Token) -> str:
        return str(id_token)

    def number(self, number_token: lark.Token) -> int:
        return int(number_token)

    # NOTE: Pyright detects error without arguments for __init__
    def __init__(self, dummy: Any) -> None:
        pass


@lark.v_args(inline=True)
class _InstructionConditionDescriptionTransformer(lark.Transformer):
    @lark.v_args(inline=False)
    def or_condition(self, and_conditions: List[InstructionConditionDescription]) -> InstructionConditionDescription:
        if len(and_conditions) == 1:
            return and_conditions[0]
        else:
            return LogicalInstructionConditionDescription(operator='or', conditions=and_conditions)

    @lark.v_args(inline=False)
    def and_condition(self, atom_conditions: List[InstructionConditionDescription]) -> InstructionConditionDescription:
        if len(atom_conditions) == 1:
            return atom_conditions[0]
        else:
            return LogicalInstructionConditionDescription(operator='and', conditions=atom_conditions)

    def equality_condition(self, subject: InstructionConditionObjectDescription, equality_op: str,
                           object: InstructionConditionObjectDescription) -> EqualityInstructionConditionDescription:
        return EqualityInstructionConditionDescription(subject=subject, operator=equality_op, object=object)

    def in_condition(self, subject: InstructionConditionObjectDescription, values: List[int]) \
            -> InInstructionConditionDescription:
        return InInstructionConditionDescription(subject=subject, values=values)

    def in_range_condition(self, subject: InstructionConditionObjectDescription, value_start: int, value_end: int) \
            -> InRangeInstructionConditionDescription:
        return InRangeInstructionConditionDescription(subject=subject, value_start=value_start, value_end=value_end)

    def field_object(self, field: str, element_index: Optional[int] = None) -> FieldInstructionConditionObjectDescription:
        return FieldInstructionConditionObjectDescription(field=field, element_index=element_index)

    def immediate_object(self, value: int) -> ImmediateInstructionConditionObjectDescription:
        return ImmediateInstructionConditionObjectDescription(value=value)

    def function_object(self, function: str, argument: FieldInstructionConditionObjectDescription) \
            -> FunctionInstructionConditionObjectDescription:
        return FunctionInstructionConditionObjectDescription(function=function, argument=argument)

    @lark.v_args(inline=False)
    def number_array(self, numbers: List[int]) -> List[int]:
        return numbers

    def id(self, id_token: lark.Token) -> str:
        return str(id_token)

    def decimal_number(self, number_token: lark.Token) -> int:
        return int(number_token)

    def hex_number(self, number_token: lark.Token) -> int:
        return int(number_token, base=16)

    def binary_number(self, number_token: lark.Token) -> int:
        return int(number_token, base=2)

    def equality_op(self, equality_op_token: lark.Token) -> str:
        return str(equality_op_token)

    def __init__(self, dummy: Any) -> None:
        pass

# endregion

# region Internal functions


def _yaml_include_constructor(loader: yaml.Loader, node: yaml.Node) -> Any:
    """Constructor for YAML !include tag"""
    if not isinstance(node, yaml.ScalarNode):
        raise TypeError(f'Unsupported type for !include: {node}')

    # Make path pattern
    path_pattern = loader.construct_scalar(node)
    if _yaml_include_context.base_dir is not None:
        path_pattern = os.path.join(
            _yaml_include_context.base_dir, path_pattern)

    # Load included yamls
    results = []
    paths = (path for path in glob.iglob(path_pattern) if isfile(path))
    for path in paths:
        with open(path, 'r') as file:
            results.append(yaml.load(file, Loader=yaml.Loader))

    result_types = list(set(type(result) for result in results))
    if len(result_types) == 0:
        return None

    if len(result_types) > 1:
        raise RuntimeError(
            f'The result of !include cannot be combinations of multiple types: {result_types}')

    # Combine included data
    result_type = result_types[0]
    if issubclass(result_type, list):
        return list(itertools.chain.from_iterable(results))
    elif issubclass(result_type, dict):
        result_dict = {}
        for result in results:
            result_dict.update(cast(dict, result))
        return result_dict
    else:
        return results


def _add_yaml_include_constructor() -> None:
    """Add !include constructor to PyYAML"""
    yaml.add_constructor('!include', _yaml_include_constructor)


def _validate_mc_desc_model(mc_desc_model: Any) -> None:
    with importlib.resources.open_text('mcdecoder.schemas', 'mc_desc_schema.json') as file:
        schema = json.load(file)

    jsonschema.validate(mc_desc_model, schema)


def _create_instruction_format_parser() -> lark.Lark:
    with importlib.resources.open_text('mcdecoder.grammars', 'instruction_format.lark') as file:
        return lark.Lark(file, start='instruction_format', parser='lalr')


def _create_machine_decoder_model(machine_desc_model: MachineDescription) -> MachineDecoder:
    extras: Optional[Any] = None
    if 'extras' in machine_desc_model:
        extras = machine_desc_model['extras']

    return MachineDecoder(extras=extras)


def _make_namespace_prefix(namespace: Optional[str]) -> str:
    return namespace + '_' if namespace is not None else ''


def _create_instruction_decoder_model(instruction_desc_model: InstructionDescription) -> InstructionDecoder:
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
    field_names = set(cast(str, field.name)
                      for field in instruction_format.field_formats if field.name is not None)
    field_extras_dict: Dict[str, Any] = cast(Dict[str, Any], instruction_desc_model['field_extras']) \
        if 'field_extras' in instruction_desc_model else {}
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
    if 'match_condition' in instruction_desc_model:
        match_condition = _parse_and_create_instruction_decoder_condition(
            cast(str, instruction_desc_model['match_condition']))
    else:
        match_condition = None

    if 'unmatch_condition' in instruction_desc_model:
        unmatch_condition = _parse_and_create_instruction_decoder_condition(
            cast(str, instruction_desc_model['unmatch_condition']))
    else:
        unmatch_condition = None

    # Create instruction decoder model
    instruction_extras = instruction_desc_model['extras'] if 'extras' in instruction_desc_model else None

    return InstructionDecoder(
        name=instruction_desc_model['name'],
        fixed_bits_mask=fixed_bits_mask,
        fixed_bits=fixed_bits,
        type_bit_size=_calc_type_bit_size(instruction_bit_size),
        field_decoders=field_decoders,
        match_condition=match_condition,
        unmatch_condition=unmatch_condition,
        extras=instruction_extras,
    )


def _build_fixed_bits_info(instruction_format: InstructionFormatDescription) -> Tuple[int, int]:
    """Build fixed bits information and returns fixed bit mask and fixed bits"""
    instruction_bit_format = ''.join(
        field_format.bits_format for field_format in instruction_format.field_formats)
    fixed_bit_mask = int(instruction_bit_format.replace(
        '0', '1').replace('x', '0'), base=2)
    fixed_bits = int(instruction_bit_format.replace('x', '0'), base=2)
    return fixed_bit_mask, fixed_bits


def _create_field_decoder(field_name: str, field_extras: Optional[Any], instruction_format: InstructionFormatDescription,
                          ff_index_to_start_bit: Dict[int, int]) -> InstructionFieldDecoder:
    """Create a model which contains information of a instruction field decoder"""
    # Find related field formats
    field_formats = [
        field for field in instruction_format.field_formats if field.name == field_name]

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
                index=sf_index, mask=sf_mask, start_bit_in_instruction=sf_start_bit_in_instruction,
                end_bit_in_instruction=sf_end_bit_in_instruction, end_bit_in_field=bit_range.end)
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


def _parse_and_create_instruction_decoder_condition(instruction_condition: str) -> InstructionDecoderCondition:
    parsed_condition = _parse_instruction_condition(instruction_condition)
    return _create_instruction_decoder_condition(parsed_condition)


def _create_instruction_decoder_condition(condition: InstructionConditionDescription) -> InstructionDecoderCondition:
    if isinstance(condition, LogicalInstructionConditionDescription):
        child_decode_conditions = [_create_instruction_decoder_condition(
            child_condition) for child_condition in condition.conditions]
        if condition.operator == 'and':
            return AndIdCondition(conditions=child_decode_conditions)
        else:  # condition.operator == 'or'
            return OrIdCondition(conditions=child_decode_conditions)

    elif isinstance(condition, EqualityInstructionConditionDescription):
        decoder_condition_subject = _create_instruction_decoder_condition_object(
            condition.subject)
        decoder_condition_object = _create_instruction_decoder_condition_object(
            condition.object)
        return EqualityIdCondition(subject=decoder_condition_subject, operator=condition.operator,
                                   object=decoder_condition_object)

    elif isinstance(condition, InInstructionConditionDescription):
        decoder_condition_subject = _create_instruction_decoder_condition_object(
            condition.subject)
        return InIdCondition(subject=decoder_condition_subject, values=condition.values)

    elif isinstance(condition, InRangeInstructionConditionDescription):
        decoder_condition_subject = _create_instruction_decoder_condition_object(
            condition.subject)
        return InRangeIdCondition(subject=decoder_condition_subject, value_start=condition.value_start,
                                  value_end=condition.value_end)

    else:
        raise RuntimeError(f'Unknown condition type: {condition}')


def _create_instruction_decoder_condition_object(object: InstructionConditionObjectDescription) \
        -> InstructionDecoderConditionObject:
    if isinstance(object, FieldInstructionConditionObjectDescription):
        return FieldIdConditionObject(field=object.field, element_index=object.element_index)
    elif isinstance(object, ImmediateInstructionConditionObjectDescription):
        return ImmediateIdConditionObject(value=object.value)
    elif isinstance(object, FunctionInstructionConditionObjectDescription):
        decoder_condition_argument = cast(FieldIdConditionObject,
                                          _create_instruction_decoder_condition_object(object.argument))
        return FunctionIdConditionObject(function=object.function, argument=decoder_condition_argument)
    else:
        raise RuntimeError(f'Unknown condition object type: {object}')


def _parse_instruction_condition(instruction_condition: str) -> InstructionConditionDescription:
    """Parse an instruction condition and returns a parsed condition"""
    parsed_tree = _instruction_condition_parser.parse(instruction_condition)
    return cast(InstructionConditionDescription, _InstructionConditionDescriptionTransformer(None).transform(parsed_tree))


def _create_instruction_condition_parser() -> lark.Lark:
    with importlib.resources.open_text('mcdecoder.grammars', 'instruction_condition.lark') as file:
        return lark.Lark(file, start='condition', parser='lalr')


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


def _test_instruction_condition_vectorized(code_vec: np.ndarray, condition: InstructionDecoderCondition,  # noqa: C901
                                           instruction_decoder: InstructionDecoder) -> np.ndarray:
    # NOTE Do not refactor and split into multiple functions for performance
    if isinstance(condition, AndIdCondition):
        total_test_vec = np.full((code_vec.shape[0]), True)
        for child_condition in condition.conditions:
            test_vec: np.ndarray = _test_instruction_condition_vectorized(
                code_vec, child_condition, instruction_decoder)
            total_test_vec = np.logical_and(  # type: ignore # TODO pyright can't recognize numpy.logical_and
                total_test_vec, test_vec)

        return total_test_vec

    elif isinstance(condition, OrIdCondition):
        total_test_vec = np.full((code_vec.shape[0]), False)
        for child_condition in condition.conditions:
            test_vec: np.ndarray = _test_instruction_condition_vectorized(
                code_vec, child_condition, instruction_decoder)
            total_test_vec = np.logical_or(  # type: ignore # TODO pyright can't recognize numpy.logical_and
                total_test_vec, test_vec)

        return total_test_vec

    elif isinstance(condition, EqualityIdCondition):
        subject_vec = _instruction_condition_object_vectorized(
            code_vec, condition.subject, instruction_decoder)
        object_vec = _instruction_condition_object_vectorized(
            code_vec, condition.object, instruction_decoder)
        if condition.operator == '==':
            return subject_vec == object_vec
        elif condition.operator == '!=':
            return subject_vec != object_vec
        elif condition.operator == '<':
            return subject_vec < object_vec
        elif condition.operator == '<=':
            return subject_vec <= object_vec
        elif condition.operator == '>':
            return subject_vec > object_vec
        elif condition.operator == '>=':
            return subject_vec >= object_vec
        else:
            return np.full((code_vec.shape[0]), False)

    elif isinstance(condition, InIdCondition):
        subject_vec = _instruction_condition_object_vectorized(
            code_vec, condition.subject, instruction_decoder)
        return np.isin(subject_vec, condition.values)

    elif isinstance(condition, InRangeIdCondition):
        subject_vec = _instruction_condition_object_vectorized(
            code_vec, condition.subject, instruction_decoder)
        return np.logical_and(  # type: ignore # TODO pyright can't recognize numpy.logical_and
            subject_vec >= condition.value_start, subject_vec <= condition.value_end)

    else:
        return np.full((code_vec.shape[0]), False)


def _instruction_condition_object_vectorized(code_vec: np.ndarray, object: InstructionDecoderConditionObject,
                                             instruction_decoder: InstructionDecoder) -> np.ndarray:
    if isinstance(object, FieldIdConditionObject):
        field_decoder = next((field for field in instruction_decoder.field_decoders if field.name ==
                              object.field), None)
        if field_decoder is None:
            return np.zeros((code_vec.shape[0]))

        value_vec = _decode_field_vectorized(code_vec, field_decoder)
        if object.element_index is not None:
            value_vec = (value_vec & (1 << object.element_index)
                         ) >> object.element_index

        return value_vec

    elif isinstance(object, ImmediateIdConditionObject):
        # Returns scalar
        return np.array(object.value)

    elif isinstance(object, FunctionIdConditionObject):
        if not (object.function in _FUNCTION_NAME_TO_FUNCTION):
            return np.zeros((code_vec.shape[0]))

        function = _FUNCTION_NAME_TO_FUNCTION[object.function]
        value_vec = _instruction_condition_object_vectorized(
            code_vec, object.argument, instruction_decoder)
        return function(value_vec)

    else:
        return np.zeros((code_vec.shape[0]))


def _decode_field_vectorized(code_vec: np.ndarray, field_decoder: InstructionFieldDecoder) -> np.ndarray:
    value_vec = np.zeros(code_vec.shape[0], dtype=int)
    for sf_decoder in field_decoder.subfield_decoders:
        value_vec |= ((code_vec & sf_decoder.mask) >>
                      sf_decoder.end_bit_in_instruction) << sf_decoder.end_bit_in_field
    return value_vec


def _setbit_count(value_vec: np.ndarray) -> np.ndarray:
    """
    Calculate the set bit count of a value. It is built-in function for an instruction condition.

    :param value_vec: N-vector of values
    :return: N-vector of set bit counts of values
    """
    value_vvec = value_vec.reshape(value_vec.shape[0], 1)
    bit_mat = np.unpackbits(value_vvec.view(dtype=np.uint8),  # type: ignore # TODO pyright can't recognize numpy.uint8
                            axis=1)
    count_vec = np.sum(bit_mat, axis=1)
    return count_vec


# endregion

# region Internal variables

_FUNCTION_NAME_TO_FUNCTION: Dict[str, Callable[[np.ndarray], np.ndarray]] = {
    'setbit_count': _setbit_count,
}
"""
Dictionary to define built-in functions for an instruction condition.
Its entry is a pair of a function name and a function.
"""

_yaml_include_context: _YamlIncludeContext = _YamlIncludeContext(base_dir='')
_instruction_format_parser: lark.Lark = _create_instruction_format_parser()
_instruction_condition_parser: lark.Lark = _create_instruction_condition_parser()

# endregion

# region Global executions
_add_yaml_include_constructor()

# endregion
