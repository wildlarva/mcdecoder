import os
import shutil
from typing import List, cast

import jinja2

from ..core import (
    AndIdCondition, EqualityIdCondition, FieldIdConditionObject,
    InRangeIdCondition, InstructionDecoderCondition,
    InstructionDecoder, InstructionFieldDecoder, InstructionSubfieldDecoder,
    MachineDecoder, McDecoder)
from ..generator import _generate, generate


def test_generate_without_template_dir() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert generate('test/arm.yaml', output_directory='out') == 0
    assert os.path.isfile('out/arm_mcdecoder.c') is True
    assert os.path.isfile('out/arm_mcdecoder.h') is True


def test_generate_with_template_dir() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert generate('test/arm.yaml', output_directory='out',
                    template_directory='test/user_templates') == 0
    assert os.path.isfile('out/arm_template.c') is True
    assert os.path.isfile('out/arm_template.h') is True


def test_generate_with_output_dir() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert generate('test/arm.yaml', output_directory='out/out2') == 0
    assert os.path.isfile('out/out2/arm_mcdecoder.c') is True
    assert os.path.isfile('out/out2/arm_mcdecoder.h') is True


def test__generate() -> None:
    mcdecoder_model = McDecoder(
        namespace_prefix='ns_',
        machine_decoder=MachineDecoder(extras=None),
        instruction_decoders=[
            InstructionDecoder(
                name='add_1',
                fixed_bits_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_size=32,
                field_decoders=[
                    InstructionFieldDecoder(
                        name='cond', start_bit=31, type_bit_size=8,
                        subfield_decoders=[
                            InstructionSubfieldDecoder(index=0, mask=0xf0000000, start_bit_in_instruction=31,
                                                       end_bit_in_instruction=28, end_bit_in_field=0)
                        ], extras=None),
                    InstructionFieldDecoder(
                        name='S', start_bit=20, type_bit_size=8, subfield_decoders=[
                            InstructionSubfieldDecoder(index=0, mask=0x00100000, start_bit_in_instruction=20,
                                                       end_bit_in_instruction=20, end_bit_in_field=0)
                        ], extras=None),
                ],
                match_condition=EqualityIdCondition(
                    subject=FieldIdConditionObject(field='cond', element_index=None), operator='!=', value=0xf),
                unmatch_condition=None,
                extras=None,
            ),
            InstructionDecoder(
                name='push_1',
                fixed_bits_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_size=32,
                field_decoders=[
                    InstructionFieldDecoder(name='cond', start_bit=31, type_bit_size=8, subfield_decoders=[
                        InstructionSubfieldDecoder(index=0, mask=0xf0000000, start_bit_in_instruction=31,
                                                   end_bit_in_instruction=28, end_bit_in_field=0)
                    ], extras=None),
                    InstructionFieldDecoder(name='register_list', start_bit=15, type_bit_size=16, subfield_decoders=[
                        InstructionSubfieldDecoder(index=0, mask=0x0000ffff, start_bit_in_instruction=15,
                                                   end_bit_in_instruction=0, end_bit_in_field=0)
                    ], extras=None),
                ],
                match_condition=AndIdCondition(conditions=cast(List[InstructionDecoderCondition], [
                    EqualityIdCondition(
                        subject=FieldIdConditionObject(field='register_list', element_index=None), operator='>', value=0x1),
                    InRangeIdCondition(
                        subject=FieldIdConditionObject(field='cond', element_index=None), value_start=2, value_end=4)
                ])),
                unmatch_condition=None,
                extras=None,
            ),
            InstructionDecoder(
                name='push_2',
                fixed_bits_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_size=32,
                field_decoders=[
                    InstructionFieldDecoder(name='cond', start_bit=31, type_bit_size=8, subfield_decoders=[
                        InstructionSubfieldDecoder(index=0, mask=0xf0000000, start_bit_in_instruction=31,
                                                   end_bit_in_instruction=28, end_bit_in_field=0)
                    ], extras=None),
                    InstructionFieldDecoder(name='register_list', start_bit=15, type_bit_size=16, subfield_decoders=[
                        InstructionSubfieldDecoder(index=0, mask=0x0000ffff, start_bit_in_instruction=15,
                                                   end_bit_in_instruction=0, end_bit_in_field=0)
                    ], extras=None),
                ],
                match_condition=None,
                unmatch_condition=None,
                extras=None,
            ),
        ],
        extras=None,
    )

    shutil.rmtree('out', ignore_errors=True)

    assert _generate(mcdecoder_model, 'out', jinja2.PackageLoader(
        'mcdecoder', 'templates/athrill')) is True
    assert os.path.isfile('out/ns_mcdecoder.c') is True
    assert os.path.isfile('out/ns_mcdecoder.h') is True
