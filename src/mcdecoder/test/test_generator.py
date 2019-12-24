from mcdecoder.core import (
    EqualityInstructionDecodeCondition, InRangeInstructionDecodeCondition,
    InstructionDecoder, InstructionFieldDecoder, InstructionSubfieldDecoder,
    MachineDecoder, McDecoder)
from mcdecoder.generator import _generate, generate


def test_generate() -> None:
    assert generate('test/arm.yaml') == True


def test__generate() -> None:
    mcdecoder_model = McDecoder(
        machine_decoder=MachineDecoder(namespace_prefix='ns', extras=None),
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
                conditions=[EqualityInstructionDecodeCondition(
                    field='cond', operator='!=', value=0xf)],
                extras=None,
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
                conditions=[EqualityInstructionDecodeCondition(
                    field='register_list', operator='>', value=0x1), InRangeInstructionDecodeCondition(field='cond', value_start=2, value_end=4)],
                extras=None,
            ),
            InstructionDecoder(
                name='push_2',
                fixed_bits_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_size=32,
                field_decoders=[
                    InstructionFieldDecoder(name='cond', start_bit=31, type_bit_size=8, subfield_decoders=[InstructionSubfieldDecoder(
                        index=0, mask=0xf0000000, start_bit_in_instruction=31, end_bit_in_instruction=28, end_bit_in_field=0)]),
                    InstructionFieldDecoder(name='register_list', start_bit=15, type_bit_size=16, subfield_decoders=[InstructionSubfieldDecoder(
                        index=0, mask=0x0000ffff, start_bit_in_instruction=15, end_bit_in_instruction=0, end_bit_in_field=0)]),
                ],
                conditions=[],
                extras=None,
            ),
        ],
    )
    assert _generate(mcdecoder_model) == True
