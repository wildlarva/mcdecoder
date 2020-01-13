from ..core import (
    EqualityIdCondition, FieldIdConditionObject, ImmediateIdConditionObject, InRangeIdCondition,
    create_mcdecoder_model, load_mc_description_model)


def test_create_mcdecoder_model_namespace() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/arm.yaml')

    mcdecoder_model.namespace_prefix == 'arm_'


def test_create_mcdecoder_model_extras() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/arm.yaml')
    assert mcdecoder_model.extras is not None
    assert mcdecoder_model.extras['compiler'] == 'gcc'

    machine = mcdecoder_model.machine_decoder
    assert machine.extras is not None
    assert machine.extras['arch_type'] == 'arm'

    instruction_add = mcdecoder_model.instruction_decoders[0]
    assert instruction_add.extras is not None
    assert instruction_add.extras['clocks'] == 10

    _, _, field_Rn, field_Rd, field_imm12 = instruction_add.field_decoders
    assert field_Rn.extras is not None
    assert field_Rn.extras['type'] == 'register'
    assert field_Rd.extras is not None
    assert field_Rd.extras['type'] == 'register'
    assert field_imm12.extras is not None
    assert field_imm12.extras['type'] == 'immediate'


def test_create_mcdecoder_model_32bit_instructions() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/arm.yaml')

    assert len(mcdecoder_model.instruction_decoders) == 2

    instruction_decoder_model_add_1, instruction_decoder_model_push_1 = mcdecoder_model.instruction_decoders
    assert instruction_decoder_model_add_1.name == 'add_1'
    assert instruction_decoder_model_add_1.fixed_bits_mask == 0x0fe00000
    assert instruction_decoder_model_add_1.fixed_bits == 0x02800000
    assert instruction_decoder_model_add_1.type_bit_size == 32
    assert len(instruction_decoder_model_add_1.field_decoders) == 5

    field_cond = instruction_decoder_model_add_1.field_decoders[0]
    assert field_cond.name == 'cond'
    assert field_cond.type_bit_size == 8
    assert len(field_cond.subfield_decoders) == 1

    subfield_cond = field_cond.subfield_decoders[0]
    assert subfield_cond.index == 0
    assert subfield_cond.mask == 0xf0000000
    assert subfield_cond.start_bit_in_instruction == 31
    assert subfield_cond.end_bit_in_instruction == 28
    assert subfield_cond.end_bit_in_field == 0

    assert instruction_decoder_model_push_1.name == 'push_1'


def test_create_mcdecoder_model_16bit_x2_instructions() -> None:
    mcdecoder = create_mcdecoder_model('test/arm_thumb.yaml')

    assert len(mcdecoder.instruction_decoders) == 2

    instruction_add, instruction_push = mcdecoder.instruction_decoders
    assert instruction_add.name == 'add_1'
    assert instruction_add.encoding_element_bit_length == 16
    assert instruction_add.length_of_encoding_elements == 2
    assert instruction_add.fixed_bits_mask == 0xfbe08000
    assert instruction_add.fixed_bits == 0xf1000000
    assert instruction_add.type_bit_size == 32
    assert len(instruction_add.field_decoders) == 6

    field_i = instruction_add.field_decoders[0]
    assert field_i.name == 'i'
    assert field_i.type_bit_size == 8
    assert len(field_i.subfield_decoders) == 1

    sf_i = field_i.subfield_decoders[0]
    assert sf_i.index == 0
    assert sf_i.mask == 0x04000000
    assert sf_i.start_bit_in_instruction == 26
    assert sf_i.end_bit_in_instruction == 26
    assert sf_i.end_bit_in_field == 0

    field_imm3 = instruction_add.field_decoders[3]
    assert field_imm3.name == 'imm3'
    assert field_imm3.type_bit_size == 8
    assert len(field_imm3.subfield_decoders) == 1

    sf_imm3 = field_imm3.subfield_decoders[0]
    assert sf_imm3.index == 0
    assert sf_imm3.mask == 0x00007000
    assert sf_imm3.start_bit_in_instruction == 14
    assert sf_imm3.end_bit_in_instruction == 12
    assert sf_imm3.end_bit_in_field == 0

    assert instruction_push.name == 'push_1'


def test_create_mcdecoder_model_16bit_instructions() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/riscv.yaml')

    assert len(mcdecoder_model.instruction_decoders) == 2

    instruction_decoder_model_addi_1, instruction_decoder_model_sd_1 = mcdecoder_model.instruction_decoders

    # c_addi_1
    assert instruction_decoder_model_addi_1.name == 'c_addi_1'
    assert instruction_decoder_model_addi_1.fixed_bits_mask == 0xe003
    assert instruction_decoder_model_addi_1.fixed_bits == 0x0001
    assert instruction_decoder_model_addi_1.type_bit_size == 16
    assert len(instruction_decoder_model_addi_1.field_decoders) == 4

    field_cond = instruction_decoder_model_addi_1.field_decoders[0]
    assert field_cond.name == 'funct3'
    assert field_cond.type_bit_size == 8
    assert len(field_cond.subfield_decoders) == 1

    subfield_cond = field_cond.subfield_decoders[0]
    assert subfield_cond.index == 0
    assert subfield_cond.mask == 0xe000
    assert subfield_cond.start_bit_in_instruction == 15
    assert subfield_cond.end_bit_in_instruction == 13
    assert subfield_cond.end_bit_in_field == 0

    field_imm = instruction_decoder_model_addi_1.field_decoders[1]
    assert field_imm.name == 'imm'
    assert field_imm.type_bit_size == 8
    assert len(field_imm.subfield_decoders) == 2

    subfield_imm_0, subfield_imm_1 = field_imm.subfield_decoders
    assert subfield_imm_0.index == 0
    assert subfield_imm_0.mask == 0x1000
    assert subfield_imm_0.start_bit_in_instruction == 12
    assert subfield_imm_0.end_bit_in_instruction == 12
    assert subfield_imm_0.end_bit_in_field == 5

    assert subfield_imm_1.index == 1
    assert subfield_imm_1.mask == 0x007c
    assert subfield_imm_1.start_bit_in_instruction == 6
    assert subfield_imm_1.end_bit_in_instruction == 2
    assert subfield_imm_1.end_bit_in_field == 0

    # c_sd_1
    assert instruction_decoder_model_sd_1.name == 'c_sd_1'
    assert len(instruction_decoder_model_sd_1.field_decoders) == 4

    field_offset = instruction_decoder_model_sd_1.field_decoders[1]
    assert len(field_offset.subfield_decoders) == 2

    subfield_offset_0, subfield_offset_1 = field_offset.subfield_decoders
    assert subfield_offset_0.index == 0
    assert subfield_offset_0.mask == 0x1c00
    assert subfield_offset_0.start_bit_in_instruction == 12
    assert subfield_offset_0.end_bit_in_instruction == 10
    assert subfield_offset_0.end_bit_in_field == 3

    assert subfield_offset_1.index == 1
    assert subfield_offset_1.mask == 0x0380
    assert subfield_offset_1.start_bit_in_instruction == 9
    assert subfield_offset_1.end_bit_in_instruction == 7
    assert subfield_offset_1.end_bit_in_field == 6


def test_create_mcdecoder_model_condition() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/arm.yaml')

    add_condition = mcdecoder_model.instruction_decoders[0].unmatch_condition
    assert isinstance(add_condition, EqualityIdCondition)
    assert add_condition.type == 'equality'
    assert isinstance(add_condition.subject, FieldIdConditionObject)
    assert add_condition.subject.field == 'cond'
    assert add_condition.operator == '=='
    assert isinstance(add_condition.object, ImmediateIdConditionObject)
    assert add_condition.object.value == 15

    push_condition = mcdecoder_model.instruction_decoders[1].match_condition
    assert isinstance(push_condition, InRangeIdCondition)
    assert push_condition.type == 'in_range'
    assert isinstance(push_condition.subject, FieldIdConditionObject)
    assert push_condition.subject.field == 'cond'
    assert push_condition.value_start == 0
    assert push_condition.value_end == 14


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
