import pytest

from ..core import (
    EqualityIdCondition,
    FieldIdConditionObject,
    FunctionIdConditionObject,
    ImmediateIdConditionObject,
    InIdCondition,
    InRangeIdCondition,
    LoadError,
    create_mcdecoder_model,
    load_mc_description_model,
)


def test_create_mcdecoder_model_namespace() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/arm.yaml')

    mcdecoder_model.namespace_prefix == 'arm_'


def test_create_mcdecoder_model_with_config() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/process_instruction_hook_with_config/process_instruction_hook.yaml')

    instruction = mcdecoder_model.instructions[0]
    assert instruction.extras['extra_attribute'] == 'extra_content'


def test_create_mcdecoder_model_without_config() -> None:
    with pytest.raises(LoadError):
        create_mcdecoder_model(
            'test/process_instruction_hook_without_config/process_instruction_hook.yaml')


def test_create_mcdecoder_model_extras() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/arm.yaml')
    assert mcdecoder_model.extras is not None
    assert mcdecoder_model.extras['compiler'] == 'gcc'

    machine = mcdecoder_model.machine
    assert machine.extras is not None
    assert machine.extras['arch_type'] == 'arm'

    instruction_add = mcdecoder_model.instructions[0]
    assert instruction_add.extras is not None
    assert instruction_add.extras['clocks'] == 10

    _, _, field_Rn, field_Rd, field_imm12 = instruction_add.fields
    assert field_Rn.extras is not None
    assert field_Rn.extras['type'] == 'register'
    assert field_Rd.extras is not None
    assert field_Rd.extras['type'] == 'register'
    assert field_imm12.extras is not None
    assert field_imm12.extras['type'] == 'immediate'


def test_create_mcdecoder_model_32bit_instructions() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/arm.yaml')

    assert len(mcdecoder_model.instructions) == 2

    instruction_decoder_model_add_1, instruction_decoder_model_push_1 = mcdecoder_model.instructions
    assert instruction_decoder_model_add_1.name == 'add_1'
    assert instruction_decoder_model_add_1.fixed_bit_mask == 0x0fe00000
    assert instruction_decoder_model_add_1.fixed_bits == 0x02800000
    assert instruction_decoder_model_add_1.type_bit_length == 32
    assert len(instruction_decoder_model_add_1.fields) == 5

    field_cond = instruction_decoder_model_add_1.fields[0]
    assert field_cond.name == 'cond'
    assert field_cond.type_bit_length == 8
    assert len(field_cond.subfields) == 1

    subfield_cond = field_cond.subfields[0]
    assert subfield_cond.index == 0
    assert subfield_cond.mask == 0xf0000000
    assert subfield_cond.msb_in_instruction == 31
    assert subfield_cond.lsb_in_instruction == 28
    assert subfield_cond.lsb_in_field == 0

    assert instruction_decoder_model_push_1.name == 'push_1'


def test_create_mcdecoder_model_16bit_x2_instructions() -> None:
    mcdecoder = create_mcdecoder_model('test/arm_thumb.yaml')

    assert len(mcdecoder.instructions) == 2

    instruction_add, instruction_push = mcdecoder.instructions
    assert instruction_add.name == 'add_1'
    assert instruction_add.encoding_element_bit_length == 16
    assert instruction_add.length_of_encoding_elements == 2
    assert instruction_add.fixed_bit_mask == 0xfbe08000
    assert instruction_add.fixed_bits == 0xf1000000
    assert instruction_add.type_bit_length == 32
    assert len(instruction_add.fields) == 6

    field_i = instruction_add.fields[0]
    assert field_i.name == 'i'
    assert field_i.type_bit_length == 8
    assert len(field_i.subfields) == 1

    sf_i = field_i.subfields[0]
    assert sf_i.index == 0
    assert sf_i.mask == 0x04000000
    assert sf_i.msb_in_instruction == 26
    assert sf_i.lsb_in_instruction == 26
    assert sf_i.lsb_in_field == 0

    field_imm3 = instruction_add.fields[3]
    assert field_imm3.name == 'imm3'
    assert field_imm3.type_bit_length == 8
    assert len(field_imm3.subfields) == 1

    sf_imm3 = field_imm3.subfields[0]
    assert sf_imm3.index == 0
    assert sf_imm3.mask == 0x00007000
    assert sf_imm3.msb_in_instruction == 14
    assert sf_imm3.lsb_in_instruction == 12
    assert sf_imm3.lsb_in_field == 0

    assert instruction_push.name == 'push_1'


def test_create_mcdecoder_model_16bit_instructions() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/riscv.yaml')

    assert len(mcdecoder_model.instructions) == 2

    instruction_decoder_model_addi_1, instruction_decoder_model_sd_1 = mcdecoder_model.instructions

    # c_addi_1
    assert instruction_decoder_model_addi_1.name == 'c_addi_1'
    assert instruction_decoder_model_addi_1.fixed_bit_mask == 0xe003
    assert instruction_decoder_model_addi_1.fixed_bits == 0x0001
    assert instruction_decoder_model_addi_1.type_bit_length == 16
    assert len(instruction_decoder_model_addi_1.fields) == 4

    field_cond = instruction_decoder_model_addi_1.fields[0]
    assert field_cond.name == 'funct3'
    assert field_cond.type_bit_length == 8
    assert len(field_cond.subfields) == 1

    subfield_cond = field_cond.subfields[0]
    assert subfield_cond.index == 0
    assert subfield_cond.mask == 0xe000
    assert subfield_cond.msb_in_instruction == 15
    assert subfield_cond.lsb_in_instruction == 13
    assert subfield_cond.lsb_in_field == 0

    field_imm = instruction_decoder_model_addi_1.fields[1]
    assert field_imm.name == 'imm'
    assert field_imm.type_bit_length == 8
    assert len(field_imm.subfields) == 2

    subfield_imm_0, subfield_imm_1 = field_imm.subfields
    assert subfield_imm_0.index == 0
    assert subfield_imm_0.mask == 0x1000
    assert subfield_imm_0.msb_in_instruction == 12
    assert subfield_imm_0.lsb_in_instruction == 12
    assert subfield_imm_0.lsb_in_field == 5

    assert subfield_imm_1.index == 1
    assert subfield_imm_1.mask == 0x007c
    assert subfield_imm_1.msb_in_instruction == 6
    assert subfield_imm_1.lsb_in_instruction == 2
    assert subfield_imm_1.lsb_in_field == 0

    # c_sd_1
    assert instruction_decoder_model_sd_1.name == 'c_sd_1'
    assert len(instruction_decoder_model_sd_1.fields) == 4

    field_offset = instruction_decoder_model_sd_1.fields[1]
    assert len(field_offset.subfields) == 2

    subfield_offset_0, subfield_offset_1 = field_offset.subfields
    assert subfield_offset_0.index == 0
    assert subfield_offset_0.mask == 0x1c00
    assert subfield_offset_0.msb_in_instruction == 12
    assert subfield_offset_0.lsb_in_instruction == 10
    assert subfield_offset_0.lsb_in_field == 3

    assert subfield_offset_1.index == 1
    assert subfield_offset_1.mask == 0x0380
    assert subfield_offset_1.msb_in_instruction == 9
    assert subfield_offset_1.lsb_in_instruction == 7
    assert subfield_offset_1.lsb_in_field == 6


def test_create_mcdecoder_model_condition() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/arm.yaml')

    add_condition = mcdecoder_model.instructions[0].unmatch_condition
    assert isinstance(add_condition, EqualityIdCondition)
    assert add_condition.type == 'equality'
    assert isinstance(add_condition.subject, FieldIdConditionObject)
    assert add_condition.subject.field == 'cond'
    assert add_condition.operator == '=='
    assert isinstance(add_condition.object, ImmediateIdConditionObject)
    assert add_condition.object.value == 15

    push_condition = mcdecoder_model.instructions[1].match_condition
    assert isinstance(push_condition, InRangeIdCondition)
    assert push_condition.type == 'in_range'
    assert isinstance(push_condition.subject, FieldIdConditionObject)
    assert push_condition.subject.field == 'cond'
    assert push_condition.value_start == 0
    assert push_condition.value_end == 14


def test_create_mcdecoder_model_primitive_condition() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/primitive_condition.yaml')

    equality_condition = mcdecoder_model.instructions[0].match_condition
    assert isinstance(equality_condition, EqualityIdCondition)
    assert equality_condition.type == 'equality'
    assert isinstance(equality_condition.subject, FieldIdConditionObject)
    assert equality_condition.subject.type == 'field'
    assert equality_condition.subject.field == 'cond1'
    assert equality_condition.subject.element_index is None
    assert equality_condition.operator == '=='
    assert isinstance(equality_condition.object, ImmediateIdConditionObject)
    assert equality_condition.object.type == 'immediate'
    assert equality_condition.object.value == 1

    in_condition = mcdecoder_model.instructions[1].match_condition
    assert isinstance(in_condition, InIdCondition)
    assert in_condition.type == 'in'
    assert isinstance(in_condition.subject, FieldIdConditionObject)
    assert in_condition.subject.type == 'field'
    assert in_condition.subject.field == 'cond1'
    assert in_condition.subject.element_index is None
    assert in_condition.values == [1, 0b11]

    in_range_condition = mcdecoder_model.instructions[2].unmatch_condition
    assert isinstance(in_range_condition, InRangeIdCondition)
    assert in_range_condition.type == 'in_range'
    assert isinstance(in_range_condition.subject, FieldIdConditionObject)
    assert in_range_condition.subject.type == 'field'
    assert in_range_condition.subject.field == 'cond1'
    assert in_range_condition.subject.element_index is None
    assert in_range_condition.value_start == 1
    assert in_range_condition.value_end == 0xa

    field_element_subject_condition = mcdecoder_model.instructions[3].match_condition
    assert isinstance(field_element_subject_condition, EqualityIdCondition)
    assert field_element_subject_condition.type == 'equality'
    assert isinstance(field_element_subject_condition.subject,
                      FieldIdConditionObject)
    assert field_element_subject_condition.subject.type == 'field'
    assert field_element_subject_condition.subject.field == 'cond1'
    assert field_element_subject_condition.subject.element_index == 0
    assert field_element_subject_condition.operator == '=='
    assert isinstance(field_element_subject_condition.object,
                      ImmediateIdConditionObject)
    assert field_element_subject_condition.object.type == 'immediate'
    assert field_element_subject_condition.object.value == 1

    field_object_condition = mcdecoder_model.instructions[4].match_condition
    assert isinstance(field_object_condition, EqualityIdCondition)
    assert field_object_condition.type == 'equality'
    assert isinstance(field_object_condition.subject, FieldIdConditionObject)
    assert field_object_condition.subject.type == 'field'
    assert field_object_condition.subject.field == 'cond1'
    assert field_object_condition.subject.element_index is None
    assert field_object_condition.operator == '=='
    assert isinstance(field_object_condition.object, FieldIdConditionObject)
    assert field_object_condition.object.type == 'field'
    assert field_object_condition.object.field == 'cond2'
    assert field_object_condition.object.element_index is None

    function_subject_condition = mcdecoder_model.instructions[5].match_condition
    assert isinstance(function_subject_condition, EqualityIdCondition)
    assert function_subject_condition.type == 'equality'
    assert isinstance(function_subject_condition.subject,
                      FunctionIdConditionObject)
    assert function_subject_condition.subject.type == 'function'
    assert function_subject_condition.subject.function == 'setbit_count'
    assert function_subject_condition.subject.argument.field == 'cond1'
    assert function_subject_condition.subject.argument.element_index is None
    assert function_subject_condition.operator == '=='
    assert isinstance(function_subject_condition.object,
                      ImmediateIdConditionObject)
    assert function_subject_condition.object.type == 'immediate'
    assert function_subject_condition.object.value == 2


def test_load_mc_description_model_include() -> None:
    mc_desc = load_mc_description_model('test/include.yaml')

    included_list = mc_desc['extras']['included_list']
    assert len(included_list) == 4
    assert included_list[0] == 1
    assert included_list[1] == 2
    assert included_list[2] == 3
    assert included_list[3] == 4

    included_mapping = mc_desc['extras']['included_mapping']
    assert len(included_mapping) == 4
    assert included_mapping['a'] == 1
    assert included_mapping['b'] == 2
    assert included_mapping['c'] == 3
    assert included_mapping['d'] == 4


def test_create_mcdecoder_model_decision_tree_code32x1() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/decision_tree_code32x1.yaml')

    # Decision tree
    assert len(mcdecoder_model.decision_trees) == 1

    decision_tree = mcdecoder_model.decision_trees[0]
    assert decision_tree.encoding_element_bit_length == 32
    assert decision_tree.length_of_encoding_elements == 1

    # Root node
    root_node = decision_tree.root_node
    assert root_node.mask == 0xf00f0000
    assert len(root_node.fixed_bit_nodes) == 5
    assert root_node.arbitrary_bit_node is None
    assert len(root_node.instructions) == 0

    # Node for instruction0000
    node0000 = root_node.fixed_bit_nodes[0x00000000]
    assert node0000.mask == 0x0ff0ff0f
    assert len(node0000.fixed_bit_nodes) == 3
    assert node0000.arbitrary_bit_node is None
    assert len(node0000.instructions) == 0

    node0000_0001 = node0000.fixed_bit_nodes[0x00000001]
    assert node0000_0001.mask == 0
    assert len(node0000_0001.fixed_bit_nodes) == 0
    assert node0000_0001.arbitrary_bit_node is None
    assert len(node0000_0001.instructions) == 1
    assert node0000_0001.instructions[0].name == 'instruction0000_0001'

    node0000_0010 = node0000.fixed_bit_nodes[0x00000002]
    assert node0000_0010.mask == 0
    assert len(node0000_0010.fixed_bit_nodes) == 0
    assert node0000_0010.arbitrary_bit_node is None
    assert len(node0000_0010.instructions) == 1
    assert node0000_0010.instructions[0].name == 'instruction0000_0010'

    node0000_1000 = node0000.fixed_bit_nodes[0x00000008]
    assert node0000_1000.mask == 0
    assert len(node0000_1000.fixed_bit_nodes) == 0
    assert node0000_1000.arbitrary_bit_node is None
    assert len(node0000_1000.instructions) == 1
    assert node0000_1000.instructions[0].name == 'instruction0000_1000'

    # Node for instruction0001
    node0001 = root_node.fixed_bit_nodes[0x10000000]
    assert node0001.mask == 0x00f0ffff
    assert len(node0001.fixed_bit_nodes) == 3
    assert node0001.arbitrary_bit_node is None
    assert len(node0001.instructions) == 0

    node0001_0001 = node0001.fixed_bit_nodes[0x00000010]
    assert node0001_0001.mask == 0
    assert len(node0001_0001.fixed_bit_nodes) == 0
    assert node0001_0001.arbitrary_bit_node is None
    assert len(node0001_0001.instructions) == 1
    assert node0001_0001.instructions[0].name == 'instruction0001_0001'

    node0001_0010 = node0001.fixed_bit_nodes[0x00000020]
    assert node0001_0010.mask == 0
    assert len(node0001_0010.fixed_bit_nodes) == 0
    assert node0001_0010.arbitrary_bit_node is None
    assert len(node0001_0010.instructions) == 1
    assert node0001_0010.instructions[0].name == 'instruction0001_0010'

    node0001_1000 = node0001.fixed_bit_nodes[0x00000080]
    assert node0001_1000.mask == 0
    assert len(node0001_1000.fixed_bit_nodes) == 0
    assert node0001_1000.arbitrary_bit_node is None
    assert len(node0001_1000.instructions) == 1
    assert node0001_1000.instructions[0].name == 'instruction0001_1000'

    # Node for instruction0101
    node0101 = root_node.fixed_bit_nodes[0x50000000]
    assert node0101.mask == 0x00f00000
    assert len(node0101.fixed_bit_nodes) == 2
    assert node0101.arbitrary_bit_node is not None
    assert len(node0101.instructions) == 0

    node0101_0001 = node0101.fixed_bit_nodes[0x00100000]
    assert node0101_0001.mask == 0
    assert len(node0101_0001.fixed_bit_nodes) == 0
    assert node0101_0001.arbitrary_bit_node is None
    assert len(node0101_0001.instructions) == 1
    assert node0101_0001.instructions[0].name == 'instruction0101_0001'

    node0101_0010 = node0101.fixed_bit_nodes[0x00200000]
    assert node0101_0010.mask == 0
    assert len(node0101_0010.fixed_bit_nodes) == 0
    assert node0101_0010.arbitrary_bit_node is None
    assert len(node0101_0010.instructions) == 1
    assert node0101_0010.instructions[0].name == 'instruction0101_0010'

    node0101_ab = node0101.arbitrary_bit_node
    assert node0101_ab.mask == 0
    assert len(node0101_ab.fixed_bit_nodes) == 0
    assert node0101_ab.arbitrary_bit_node is None
    assert len(node0101_ab.instructions) == 1
    assert node0101_ab.instructions[0].name == 'instruction0101_ab'


def test_create_mcdecoder_model_decision_tree_code16x2() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/decision_tree_code16x2.yaml')

    # Decision tree
    assert len(mcdecoder_model.decision_trees) == 1

    decision_tree = mcdecoder_model.decision_trees[0]
    assert decision_tree.encoding_element_bit_length == 16
    assert decision_tree.length_of_encoding_elements == 2

    # Root node
    root_node = decision_tree.root_node
    assert root_node.mask == 0xf00f0000
    assert len(root_node.fixed_bit_nodes) == 5
    assert root_node.arbitrary_bit_node is None
    assert len(root_node.instructions) == 0

    # Node for instruction0000
    node0000 = root_node.fixed_bit_nodes[0x00000000]
    assert node0000.mask == 0x0ff0ff0f
    assert len(node0000.fixed_bit_nodes) == 3
    assert node0000.arbitrary_bit_node is None
    assert len(node0000.instructions) == 0

    node0000_0001 = node0000.fixed_bit_nodes[0x00000001]
    assert node0000_0001.mask == 0
    assert len(node0000_0001.fixed_bit_nodes) == 0
    assert node0000_0001.arbitrary_bit_node is None
    assert len(node0000_0001.instructions) == 1
    assert node0000_0001.instructions[0].name == 'instruction0000_0001'

    node0000_0010 = node0000.fixed_bit_nodes[0x00000002]
    assert node0000_0010.mask == 0
    assert len(node0000_0010.fixed_bit_nodes) == 0
    assert node0000_0010.arbitrary_bit_node is None
    assert len(node0000_0010.instructions) == 1
    assert node0000_0010.instructions[0].name == 'instruction0000_0010'

    node0000_1000 = node0000.fixed_bit_nodes[0x00000008]
    assert node0000_1000.mask == 0
    assert len(node0000_1000.fixed_bit_nodes) == 0
    assert node0000_1000.arbitrary_bit_node is None
    assert len(node0000_1000.instructions) == 1
    assert node0000_1000.instructions[0].name == 'instruction0000_1000'

    # Node for instruction0001
    node0001 = root_node.fixed_bit_nodes[0x10000000]
    assert node0001.mask == 0x00f0ffff
    assert len(node0001.fixed_bit_nodes) == 3
    assert node0001.arbitrary_bit_node is None
    assert len(node0001.instructions) == 0

    node0001_0001 = node0001.fixed_bit_nodes[0x00000010]
    assert node0001_0001.mask == 0
    assert len(node0001_0001.fixed_bit_nodes) == 0
    assert node0001_0001.arbitrary_bit_node is None
    assert len(node0001_0001.instructions) == 1
    assert node0001_0001.instructions[0].name == 'instruction0001_0001'

    node0001_0010 = node0001.fixed_bit_nodes[0x00000020]
    assert node0001_0010.mask == 0
    assert len(node0001_0010.fixed_bit_nodes) == 0
    assert node0001_0010.arbitrary_bit_node is None
    assert len(node0001_0010.instructions) == 1
    assert node0001_0010.instructions[0].name == 'instruction0001_0010'

    node0001_1000 = node0001.fixed_bit_nodes[0x00000080]
    assert node0001_1000.mask == 0
    assert len(node0001_1000.fixed_bit_nodes) == 0
    assert node0001_1000.arbitrary_bit_node is None
    assert len(node0001_1000.instructions) == 1
    assert node0001_1000.instructions[0].name == 'instruction0001_1000'

    # Node for instruction0101
    node0101 = root_node.fixed_bit_nodes[0x50000000]
    assert node0101.mask == 0x00f00000
    assert len(node0101.fixed_bit_nodes) == 2
    assert node0101.arbitrary_bit_node is not None
    assert len(node0101.instructions) == 0

    node0101_0001 = node0101.fixed_bit_nodes[0x00100000]
    assert node0101_0001.mask == 0
    assert len(node0101_0001.fixed_bit_nodes) == 0
    assert node0101_0001.arbitrary_bit_node is None
    assert len(node0101_0001.instructions) == 1
    assert node0101_0001.instructions[0].name == 'instruction0101_0001'

    node0101_0010 = node0101.fixed_bit_nodes[0x00200000]
    assert node0101_0010.mask == 0
    assert len(node0101_0010.fixed_bit_nodes) == 0
    assert node0101_0010.arbitrary_bit_node is None
    assert len(node0101_0010.instructions) == 1
    assert node0101_0010.instructions[0].name == 'instruction0101_0010'

    node0101_ab = node0101.arbitrary_bit_node
    assert node0101_ab.mask == 0
    assert len(node0101_ab.fixed_bit_nodes) == 0
    assert node0101_ab.arbitrary_bit_node is None
    assert len(node0101_ab.instructions) == 1
    assert node0101_ab.instructions[0].name == 'instruction0101_ab'
