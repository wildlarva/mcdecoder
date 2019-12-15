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
    assert field_cond.mask == 0xf0000000
    assert field_cond.start_bit == 31
    assert field_cond.end_bit == 28
    assert field_cond.type_bit_size == 8

    assert instruction_decoder_model_push_1.name == 'push_1'


def test_create_mcdecoder_model_16bit_instructions() -> None:
    mcdecoder_model = _create_mcdecoder_model(
        'test/riscv.yaml')

    assert len(mcdecoder_model.instruction_decoders) == 2

    instruction_decoder_model_addi_1, instruction_decoder_model_sd_1 = mcdecoder_model.instruction_decoders
    assert instruction_decoder_model_addi_1.name == 'c_addi_1'
    assert instruction_decoder_model_addi_1.fixed_bits_mask == 0xe003
    assert instruction_decoder_model_addi_1.fixed_bits == 0x0001
    assert instruction_decoder_model_addi_1.type_bit_size == 16
    assert len(instruction_decoder_model_addi_1.field_decoders) == 5

    field_cond = instruction_decoder_model_addi_1.field_decoders[0]
    assert field_cond.name == 'funct3'
    assert field_cond.mask == 0xe000
    assert field_cond.start_bit == 15
    assert field_cond.end_bit == 13
    assert field_cond.type_bit_size == 8

    assert instruction_decoder_model_sd_1.name == 'c_sd_1'


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
                    InstructionFieldDecoder(name='cond', mask=0xf0000000,
                              start_bit=31, end_bit=28, type_bit_size=8, subfield_decoders=[InstructionSubfieldDecoder(mask=0xf0000000, start_bit_in_instruction=31, end_bit_in_instruction=28, end_bit_in_field=0)]),
                    InstructionFieldDecoder(name='S', mask=0x00100000, start_bit=20,
                              end_bit=20, type_bit_size=8, subfield_decoders=[InstructionSubfieldDecoder(mask=0x00100000, start_bit_in_instruction=20, end_bit_in_instruction=20, end_bit_in_field=0)]),
                ],
            ),
            InstructionDecoder(
                name='push_1',
                fixed_bits_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_size=32,
                field_decoders=[
                    InstructionFieldDecoder(name='cond', mask=0xf0000000, start_bit=31,
                              end_bit=28, type_bit_size=8, subfield_decoders=[InstructionSubfieldDecoder(mask=0xf0000000, start_bit_in_instruction=31, end_bit_in_instruction=28, end_bit_in_field=0)]),
                    InstructionFieldDecoder(name='register_list', mask=0x0000ffff,
                              start_bit=15,  end_bit=0, type_bit_size=16, subfield_decoders=[InstructionSubfieldDecoder(mask=0x0000ffff, start_bit_in_instruction=15, end_bit_in_instruction=0, end_bit_in_field=0)]),
                ],
            ),
        ],
    )
    assert _generate(mcdecoder_model) == True
