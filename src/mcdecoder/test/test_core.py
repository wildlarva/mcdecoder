from mcdecoder.core import (
    EqualityInstructionDecodeCondition, InRangeInstructionDecodeCondition, create_mcdecoder_model)


def test_create_mcdecoder_model_namespace() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/arm.yaml')

    mcdecoder_model.machine_decoder.namespace_prefix == 'arm_'


def test_create_mcdecoder_model_extras() -> None:
    mcdecoder_model = create_mcdecoder_model(
        'test/arm.yaml')

    machine_extras = mcdecoder_model.machine_decoder.extras
    assert machine_extras is not None
    assert machine_extras['arch_type'] == 'arm'

    instruction_extras = mcdecoder_model.instruction_decoders[0].extras
    assert instruction_extras is not None
    assert instruction_extras['clocks'] == 10


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

    add_conditions = mcdecoder_model.instruction_decoders[0].conditions
    assert len(add_conditions) == 1

    add_condition = add_conditions[0]
    assert isinstance(add_condition, EqualityInstructionDecodeCondition)
    assert add_condition.type == 'equality'
    assert add_condition.field == 'cond'
    assert add_condition.operator == '!='
    assert add_condition.value == 15

    push_conditions = mcdecoder_model.instruction_decoders[1].conditions
    assert len(push_conditions) == 1

    push_condition = push_conditions[0]
    assert isinstance(push_condition, InRangeInstructionDecodeCondition)
    assert push_condition.type == 'in_range'
    assert push_condition.field == 'cond'
    assert push_condition.value_start == 0
    assert push_condition.value_end == 14