import os
import shutil
from typing import List, cast

import jinja2

from ..core import (
    AndIdCondition, EqualityIdCondition, FieldIdConditionObject, ImmediateIdConditionObject,
    InRangeIdCondition, InstructionDecoderCondition,
    InstructionDecoder, InstructionFieldDecoder, InstructionSubfieldDecoder,
    MachineDecoder, McDecoder, McdDecisionNode, McdDecisionTree)
from ..generator import _generate, generate


def test_generate_without_arguments() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert generate('test/arm.yaml', output_directory='out') == 0
    assert os.path.isfile('out/arm_mcdecoder.c') is True
    assert os.path.isfile('out/arm_mcdecoder.h') is True


def test_generate_with_type() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert generate('test/arm.yaml', type='athrill',
                    output_directory='out') == 0
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
        namespace='ns',
        namespace_prefix='ns_',
        machine=MachineDecoder(byteorder='little', extras=None),
        instructions=[
            InstructionDecoder(
                name='add_1',
                _encoding='xxxx0010100xxxxxxxxxxxxxxxxxxxxx',
                encoding_element_bit_length=32,
                length_of_encoding_elements=1,
                fixed_bit_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_length=32,
                fields=[
                    InstructionFieldDecoder(
                        name='cond', _msb=31, type_bit_length=8,
                        subfields=[
                            InstructionSubfieldDecoder(index=0, mask=0xf0000000, msb_in_instruction=31,
                                                       lsb_in_instruction=28, lsb_in_field=0)
                        ], extras=None),
                    InstructionFieldDecoder(
                        name='S', _msb=20, type_bit_length=8, subfields=[
                            InstructionSubfieldDecoder(index=0, mask=0x00100000, msb_in_instruction=20,
                                                       lsb_in_instruction=20, lsb_in_field=0)
                        ], extras=None),
                ],
                match_condition=EqualityIdCondition(
                    subject=FieldIdConditionObject(field='cond', element_index=None), operator='!=',
                    object=ImmediateIdConditionObject(value=0xf)),
                unmatch_condition=None,
                extras=None,
            ),
            InstructionDecoder(
                name='push_1',
                _encoding='xxxx0010100xxxxxxxxxxxxxxxxxxxxx',
                encoding_element_bit_length=32,
                length_of_encoding_elements=1,
                fixed_bit_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_length=32,
                fields=[
                    InstructionFieldDecoder(name='cond', _msb=31, type_bit_length=8, subfields=[
                        InstructionSubfieldDecoder(index=0, mask=0xf0000000, msb_in_instruction=31,
                                                   lsb_in_instruction=28, lsb_in_field=0)
                    ], extras=None),
                    InstructionFieldDecoder(name='register_list', _msb=15, type_bit_length=16, subfields=[
                        InstructionSubfieldDecoder(index=0, mask=0x0000ffff, msb_in_instruction=15,
                                                   lsb_in_instruction=0, lsb_in_field=0)
                    ], extras=None),
                ],
                match_condition=AndIdCondition(conditions=cast(List[InstructionDecoderCondition], [
                    EqualityIdCondition(
                        subject=FieldIdConditionObject(field='register_list', element_index=None), operator='>',
                        object=ImmediateIdConditionObject(value=0x1)),
                    InRangeIdCondition(
                        subject=FieldIdConditionObject(field='cond', element_index=None), value_start=2, value_end=4)
                ])),
                unmatch_condition=None,
                extras=None,
            ),
            InstructionDecoder(
                name='push_2',
                _encoding='xxxx0010100xxxxxxxxxxxxxxxxxxxxx',
                encoding_element_bit_length=32,
                length_of_encoding_elements=1,
                fixed_bit_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_length=32,
                fields=[
                    InstructionFieldDecoder(name='cond', _msb=31, type_bit_length=8, subfields=[
                        InstructionSubfieldDecoder(index=0, mask=0xf0000000, msb_in_instruction=31,
                                                   lsb_in_instruction=28, lsb_in_field=0)
                    ], extras=None),
                    InstructionFieldDecoder(name='register_list', _msb=15, type_bit_length=16, subfields=[
                        InstructionSubfieldDecoder(index=0, mask=0x0000ffff, msb_in_instruction=15,
                                                   lsb_in_instruction=0, lsb_in_field=0)
                    ], extras=None),
                ],
                match_condition=None,
                unmatch_condition=None,
                extras=None,
            ),
        ],
        decision_trees=[
            McdDecisionTree(
                encoding_element_bit_length=32,
                length_of_encoding_elements=1,
                root_node=McdDecisionNode(index=0, mask=0, fixed_bit_nodes={
                }, arbitrary_bit_node=None, instructions=[]),
            ),
        ],
        extras=None,
    )

    shutil.rmtree('out', ignore_errors=True)

    assert _generate(mcdecoder_model, 'out', jinja2.PackageLoader(
        'mcdecoder', 'templates/athrill')) is True
    assert os.path.isfile('out/ns_mcdecoder.c') is True
    assert os.path.isfile('out/ns_mcdecoder.h') is True
