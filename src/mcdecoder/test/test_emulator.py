from ..emulator import _emulate, emulate


def test_emulate_without_base_and_byteorder() -> None:
    assert emulate('test/arm.yaml',
                   'e9 2d 48 00') == 0


def test_emulate_with_base2() -> None:
    assert emulate('test/arm.yaml',
                   '1110 1001 0010 1101 0100 1000 0000 0000', base=2) == 0


def test_emulate_with_base16() -> None:
    assert emulate('test/arm.yaml', 'e9 2d 48 00', base=16) == 0


def test_emulate_with_big_endian() -> None:
    assert emulate('test/arm.yaml',
                   'e9 2d 48 00', byteorder='big') == 0


def test_emulate_with_little_endian() -> None:
    assert emulate('test/arm.yaml', '00 48 2d e9',
                   byteorder='little') == 0


def test__emulate_with_base2_big_endian() -> None:
    instructions = _emulate(
        'test/arm.yaml', '1110 1001 0010 1101 0100 1000 0000 0000', 2, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.field_results) == 2

    field_cond, field_register_list = instruction_push.field_results
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_with_base16_big_endian() -> None:
    instructions = _emulate(
        'test/arm.yaml', 'e9 2d 48 00', 16, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.field_results) == 2

    field_cond, field_register_list = instruction_push.field_results
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_with_base2_little_endian() -> None:
    instructions = _emulate(
        'test/arm.yaml', '0000 0000 0100 1000 0010 1101 1110 1001', 2, 'little')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.field_results) == 2

    field_cond, field_register_list = instruction_push.field_results
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_with_base16_little_endian() -> None:
    instructions = _emulate(
        'test/arm.yaml', '00 48 2d e9', 16, 'little')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.field_results) == 2

    field_cond, field_register_list = instruction_push.field_results
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_insufficient_bits_base2() -> None:
    instructions = _emulate(
        'test/arm.yaml', '1110 1001 0010 1101 0100 1000 0000 000', 2, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.field_results) == 2

    field_cond, field_register_list = instruction_push.field_results
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_insufficient_bits_base16() -> None:
    instructions = _emulate(
        'test/arm.yaml', 'e9 2d 48 0', 16, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.field_results) == 2

    field_cond, field_register_list = instruction_push.field_results
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_excessive_bits_base2() -> None:
    instructions = _emulate(
        'test/arm.yaml', '1110 1001 0010 1101 0100 1000 0000 0000 1', 2, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.field_results) == 2

    field_cond, field_register_list = instruction_push.field_results
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_excessive_bits_base16() -> None:
    instructions = _emulate(
        'test/arm.yaml', 'e9 2d 48 00 1', 16, 'big')
    assert len(instructions) == 1

    (instruction_push,) = instructions
    assert instruction_push.decoder.name == 'push_1'
    assert len(instruction_push.field_results) == 2

    field_cond, field_register_list = instruction_push.field_results
    assert field_cond.decoder.name == 'cond'
    assert field_cond.value == 0x0e

    assert field_register_list.decoder.name == 'register_list'
    assert field_register_list.value == 0x4800


def test__emulate_mismatch_equality_condition() -> None:
    instructions = _emulate(
        'test/arm.yaml', 'f2 8d b0 04', 16, 'big')
    assert len(instructions) == 0


def test__emulate_mismatch_in_range_condition() -> None:
    instructions = _emulate(
        'test/arm.yaml', 'f9 2d 48 00', 16, 'big')
    assert len(instructions) == 0
