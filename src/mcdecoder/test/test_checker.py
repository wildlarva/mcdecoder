from mcdecoder.checker import _check, check


def test_check() -> None:
    assert check('test/arm.yaml', 'e9 2d 48 00') == 0
    assert check('test/arm.yaml', 'ex xd 48 00') == 0


def test__check_no_mask() -> None:
    assert len(list(_check('test/arm.yaml', 'e9 2d 48 00', 16))) == 0
    
    assert len(list(_check('test/arm.yaml', '1110 1001 0010 1101 0100 1000 0000 0000', 2))) == 0


def test__check_one_character_mask() -> None:
    # First letter
    errors1 = list(_check('test/arm.yaml', 'x9 2d 48 00', 16))
    assert len(errors1) == 1

    assert errors1[0].type == 'undefined'
    assert errors1[0].bits_start == 0xf92d4800
    assert errors1[0].bits_end == 0xf92d4800
    
    assert len(list(_check('test/arm.yaml', 'x110 1001 0010 1101 0100 1000 0000 0000', 2))) == 0

    # Halfway
    errors2 = list(_check('test/arm.yaml', 'ex 2d 48 00', 16))
    assert len(errors2) == 2

    assert errors2[0].type == 'undefined'
    assert errors2[0].bits_start == 0xe02d4800
    assert errors2[0].bits_end == 0xe82d4800

    assert errors2[1].type == 'undefined'
    assert errors2[1].bits_start == 0xea2d4800
    assert errors2[1].bits_end == 0xef2d4800
    
    assert len(list(_check('test/arm.yaml', '111x 1001 0010 1101 0100 1000 0000 000x', 2))) == 1

    # Last letter
    assert len(list(_check('test/arm.yaml', 'e9 2d 48 0x', 16))) == 0
    
    assert len(list(_check('test/arm.yaml', '1110 1001 0010 1101 0100 1000 0000 000x', 2))) == 0


def test__check_sequential_mask() -> None:
    errors = list(_check('test/arm.yaml', 'ex xd 48 00', 16))
    assert len(errors) == 3

    assert errors[0].type == 'undefined'
    assert errors[0].bits_start == 0xe00d4800
    assert errors[0].bits_end == 0xe27d4800

    assert errors[1].type == 'undefined'
    assert errors[1].bits_start == 0xe2ad4800
    assert errors[1].bits_end == 0xe91d4800

    assert errors[2].type == 'undefined'
    assert errors[2].bits_start == 0xe93d4800
    assert errors[2].bits_end == 0xeffd4800
    
    assert len(list(_check('test/arm.yaml', '111x x001 0010 1101 0100 1000 0000 000x', 2))) == 2


def test__check_split_mask() -> None:
    errors = list(_check('test/arm.yaml', 'ex 2x 48 00', 16))
    assert len(errors) == 2

    assert errors[0].type == 'undefined'
    assert errors[0].bits_start == 0xe0204800
    assert errors[0].bits_end == 0xe92c4800

    assert errors[1].type == 'undefined'
    assert errors[1].bits_start == 0xe92e4800
    assert errors[1].bits_end == 0xef2f4800
    
    assert len(list(_check('test/arm.yaml', '111x 100x 0010 1101 0100 1000 0000 000x', 2))) == 2
