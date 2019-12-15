from mcdecoder.generator import (
    InstructionFieldDecoder, InstructionSubfieldDecoder, MachineDecoder, McDecoder, InstructionDecoder, _create_mcdecoder_model,
    _generate)


def test_create_mcdecoder_model_namespace() -> None:
    mcdecoder_model = _create_mcdecoder_model(
        'test/arm.yaml')

    mcdecoder_model.machine_decoder.namespace == 'arm'


def test_create_mcdecoder_model_32bit_instructions() -> None:
    mcdecoder_model = _create_mcdecoder_model(
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
    mcdecoder_model = _create_mcdecoder_model(
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


def test_generate() -> None:
    mcdecoder_model = McDecoder(
        machine_decoder=MachineDecoder(namespace='ns'),
        instruction_decoders=[
            InstructionDecoder(
                name='add_1',
                fixed_bits_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_size=32,
                field_decoders=[
                    InstructionFieldDecoder(name='cond', start_bit=31, type_bit_size=8, subfield_decoders=[InstructionSubfieldDecoder(
                        index=0, mask=0xf0000000, start_bit_in_instruction=31, end_bit_in_instruction=28, end_bit_in_field=0)]),
                    InstructionFieldDecoder(name='S', start_bit=20, type_bit_size=8, subfield_decoders=[InstructionSubfieldDecoder(
                        index=0, mask=0x00100000, start_bit_in_instruction=20, end_bit_in_instruction=20, end_bit_in_field=0)]),
                ],
            ),
            InstructionDecoder(
                name='push_1',
                fixed_bits_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_size=32,
                field_decoders=[
                    InstructionFieldDecoder(name='cond', start_bit=31, type_bit_size=8, subfield_decoders=[InstructionSubfieldDecoder(
                        index=0, mask=0xf0000000, start_bit_in_instruction=31, end_bit_in_instruction=28, end_bit_in_field=0)]),
                    InstructionFieldDecoder(name='register_list', start_bit=15, type_bit_size=16, subfield_decoders=[InstructionSubfieldDecoder(
                        index=0, mask=0x0000ffff, start_bit_in_instruction=15, end_bit_in_instruction=0, end_bit_in_field=0)]),
                ],
            ),
        ],
    )
    assert _generate(mcdecoder_model) == True
