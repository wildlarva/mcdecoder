from mcdecoder.emulator import _emulate, emulate


def test_emulate_without_base_and_byteorder() -> None:
    assert emulate('tests/common/arm.yaml',
                   'e9 2d 48 00') == 0


def test_emulate_with_base2() -> None:
    assert emulate('tests/common/arm.yaml',
                   '1110 1001 0010 1101 0100 1000 0000 0000', base=2) == 0


def test_emulate_with_base16() -> None:
    assert emulate('tests/common/arm.yaml', 'e9 2d 48 00', base=16) == 0


def test_emulate_with_big_endian() -> None:
    assert emulate('tests/common/arm.yaml',
                   'e9 2d 48 00', byteorder='big') == 0


def test_emulate_with_little_endian() -> None:
    assert emulate('tests/common/arm.yaml', '00 48 2d e9',
                   byteorder='little') == 0


def test_emulate_unmatch() -> None:
    assert emulate('tests/common/arm.yaml',
                   'ff 00 00 00') == 0


def test__emulate_with_base2_big_endian() -> None:
    instructions = _emulate(
        'tests/common/arm.yaml', '1110 1001 0010 1101 0100 1000 0000 0000', 2, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.fields) == 2

    field_cond, field_register_list = instruction_push.fields
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_with_base16_big_endian_code32x1() -> None:
    instructions = _emulate(
        'tests/common/arm.yaml', 'e9 2d 48 00', 16, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.fields) == 2

    field_cond, field_register_list = instruction_push.fields
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_with_base16_big_endian_code16x2() -> None:
    instructions = _emulate(
        'tests/common/arm_thumb.yaml', 'e9 2d 40 01', 16, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.fields) == 2

    field_m, field_register_list = instruction_push.fields
    assert field_m.decoder.name == 'M'
    assert field_m.value == 0x1

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x1


def test__emulate_with_base2_little_endian() -> None:
    instructions = _emulate(
        'tests/common/arm.yaml', '0000 0000 0100 1000 0010 1101 1110 1001', 2, 'little')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.fields) == 2

    field_cond, field_register_list = instruction_push.fields
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_with_base16_little_endian_code32x1() -> None:
    instructions = _emulate(
        'tests/common/arm.yaml', '00 48 2d e9', 16, 'little')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.fields) == 2

    field_cond, field_register_list = instruction_push.fields
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_with_base16_little_endian_code16x2() -> None:
    instructions = _emulate(
        'tests/common/arm_thumb.yaml', '2d e9 01 40', 16, 'little')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.fields) == 2

    field_m, field_register_list = instruction_push.fields
    assert field_m.decoder.name == 'M'
    assert field_m.value == 0x1

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x1


def test__emulate_insufficient_bits_base2() -> None:
    instructions = _emulate(
        'tests/common/arm.yaml', '1110 1001 0010 1101 0100 1000 0000 000', 2, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.fields) == 2

    field_cond, field_register_list = instruction_push.fields
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_insufficient_bits_base16() -> None:
    instructions = _emulate(
        'tests/common/arm.yaml', 'e9 2d 48 0', 16, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.fields) == 2

    field_cond, field_register_list = instruction_push.fields
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_excessive_bits_base2() -> None:
    instructions = _emulate(
        'tests/common/arm.yaml', '1110 1001 0010 1101 0100 1000 0000 0000 1', 2, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.fields) == 2

    field_cond, field_register_list = instruction_push.fields
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_excessive_bits_base16() -> None:
    instructions = _emulate(
        'tests/common/arm.yaml', 'e9 2d 48 00 1', 16, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.fields) == 2

    field_cond, field_register_list = instruction_push.fields
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_match_equality_condition() -> None:
    instructions = _emulate(
        'tests/common/primitive_condition.yaml', '10 00 00 00', 16, 'big')
    assert len(instructions) == 1

    (instruction,) = instructions
    assert instruction.decoder.name == 'equality_condition'


def test__emulate_unmatch_equality_condition() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '00 00 00 00', 16, 'big')
    assert len(instructions1) == 0

    instructions2 = _emulate(
        'tests/common/primitive_condition.yaml', '20 00 00 00', 16, 'big')
    assert len(instructions2) == 0


def test__emulate_match_in_condition() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '10 00 00 01', 16, 'big')
    assert len(instructions1) == 1

    (instruction1,) = instructions1
    assert instruction1.decoder.name == 'in_condition'

    instructions2 = _emulate(
        'tests/common/primitive_condition.yaml', '30 00 00 01', 16, 'big')
    assert len(instructions2) == 1

    (instruction2,) = instructions1
    assert instruction2.decoder.name == 'in_condition'


def test__emulate_unmatch_in_condition() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '00 00 00 01', 16, 'big')
    assert len(instructions1) == 0

    instructions2 = _emulate(
        'tests/common/primitive_condition.yaml', '20 00 00 01', 16, 'big')
    assert len(instructions2) == 0


def test__emulate_match_in_range_condition() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '00 00 00 02', 16, 'big')
    assert len(instructions1) == 1

    (instruction1,) = instructions1
    assert instruction1.decoder.name == 'in_range_condition'

    instructions2 = _emulate(
        'tests/common/primitive_condition.yaml', 'b0 00 00 02', 16, 'big')
    assert len(instructions2) == 1

    (instruction2,) = instructions1
    assert instruction2.decoder.name == 'in_range_condition'


def test__emulate_unmatch_in_range_condition() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '10 00 00 02', 16, 'big')
    assert len(instructions1) == 0

    instructions2 = _emulate(
        'tests/common/primitive_condition.yaml', 'a0 00 00 02', 16, 'big')
    assert len(instructions2) == 0


def test__emulate_match_field_element_subject() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '10 00 00 03', 16, 'big')
    assert len(instructions1) == 1

    (instruction1,) = instructions1
    assert instruction1.decoder.name == 'field_element_subject'

    instructions2 = _emulate(
        'tests/common/primitive_condition.yaml', '30 00 00 03', 16, 'big')
    assert len(instructions2) == 1

    (instruction2,) = instructions2
    assert instruction2.decoder.name == 'field_element_subject'


def test__emulate_unmatch_field_element_subject() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '20 00 00 03', 16, 'big')
    assert len(instructions1) == 0


def test__emulate_match_field_object() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '00 00 00 04', 16, 'big')
    assert len(instructions1) == 1

    (instruction1,) = instructions1
    assert instruction1.decoder.name == 'field_object'

    instructions2 = _emulate(
        'tests/common/primitive_condition.yaml', '11 00 00 04', 16, 'big')
    assert len(instructions2) == 1

    (instruction2,) = instructions2
    assert instruction2.decoder.name == 'field_object'


def test__emulate_unmatch_field_object() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '01 00 00 04', 16, 'big')
    assert len(instructions1) == 0

    instructions2 = _emulate(
        'tests/common/primitive_condition.yaml', '10 00 00 04', 16, 'big')
    assert len(instructions2) == 0


def test__emulate_match_function_subject() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '30 00 00 05', 16, 'big')
    assert len(instructions1) == 1

    (instruction1,) = instructions1
    assert instruction1.decoder.name == 'function_subject'

    instructions2 = _emulate(
        'tests/common/primitive_condition.yaml', 'a0 00 00 05', 16, 'big')
    assert len(instructions2) == 1

    (instruction2,) = instructions2
    assert instruction2.decoder.name == 'function_subject'


def test__emulate_unmatch_function_subject() -> None:
    instructions1 = _emulate(
        'tests/common/primitive_condition.yaml', '10 00 00 05', 16, 'big')
    assert len(instructions1) == 0

    instructions2 = _emulate(
        'tests/common/primitive_condition.yaml', 'e0 00 00 05', 16, 'big')
    assert len(instructions2) == 0


def test__emulate_match_and_condition() -> None:
    instructions1 = _emulate(
        'tests/common/complex_condition.yaml', '12 00 00 00', 16, 'big')
    assert len(instructions1) == 1

    (instruction1,) = instructions1
    assert instruction1.decoder.name == 'and_condition'


def test__emulate_unmatch_and_condition() -> None:
    instructions1 = _emulate(
        'tests/common/complex_condition.yaml', '11 00 00 00', 16, 'big')
    assert len(instructions1) == 0

    instructions2 = _emulate(
        'tests/common/complex_condition.yaml', '22 00 00 00', 16, 'big')
    assert len(instructions2) == 0


def test__emulate_match_or_condition() -> None:
    instructions1 = _emulate(
        'tests/common/complex_condition.yaml', '21 00 00 01', 16, 'big')
    assert len(instructions1) == 1

    (instruction1,) = instructions1
    assert instruction1.decoder.name == 'or_condition'


def test__emulate_unmatch_or_condition() -> None:
    instructions1 = _emulate(
        'tests/common/complex_condition.yaml', '02 00 00 01', 16, 'big')
    assert len(instructions1) == 0

    instructions2 = _emulate(
        'tests/common/complex_condition.yaml', '10 00 00 01', 16, 'big')
    assert len(instructions2) == 0


def test__emulate_match_andor_condition() -> None:
    instructions1 = _emulate(
        'tests/common/complex_condition.yaml', '12 00 00 02', 16, 'big')
    assert len(instructions1) == 1

    (instruction1,) = instructions1
    assert instruction1.decoder.name == 'and_or_condition1'

    instructions2 = _emulate(
        'tests/common/complex_condition.yaml', '30 00 00 02', 16, 'big')
    assert len(instructions2) == 1

    (instruction2,) = instructions2
    assert instruction2.decoder.name == 'and_or_condition1'

    instructions3 = _emulate(
        'tests/common/complex_condition.yaml', '11 00 00 03', 16, 'big')
    assert len(instructions3) == 1

    (instruction3,) = instructions3
    assert instruction3.decoder.name == 'and_or_condition2'

    instructions4 = _emulate(
        'tests/common/complex_condition.yaml', '22 00 00 03', 16, 'big')
    assert len(instructions4) == 1

    (instruction4,) = instructions4
    assert instruction4.decoder.name == 'and_or_condition2'


def test__emulate_unmatch_andor_condition() -> None:
    instructions1 = _emulate(
        'tests/common/complex_condition.yaml', '11 00 00 02', 16, 'big')
    assert len(instructions1) == 0

    instructions2 = _emulate(
        'tests/common/complex_condition.yaml', '22 00 00 02', 16, 'big')
    assert len(instructions2) == 0

    instructions3 = _emulate(
        'tests/common/complex_condition.yaml', '12 00 00 03', 16, 'big')
    assert len(instructions3) == 0

    instructions4 = _emulate(
        'tests/common/complex_condition.yaml', '30 00 00 03', 16, 'big')
    assert len(instructions4) == 0
