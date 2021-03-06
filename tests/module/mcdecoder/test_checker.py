from mcdecoder.checker import _VEC_SIZE, _check, check


def test_check() -> None:
    assert check('tests/common/arm.yaml', 'e9 2d 48 00') == 0
    assert check('tests/common/arm.yaml', 'ex xd 48 00') == 0


def test_check_duplicate() -> None:
    assert check('tests/common/duplicate_instructions.yaml',
                 'ex xd 48 00') == 0


def test_check_duplicate_same_name() -> None:
    assert check('tests/common/duplicate_instructions_same_name.yaml',
                 'ex xd 48 00') == 0


def test__check_no_mask_code32x1() -> None:
    result1 = _check('tests/common/arm.yaml',
                     'e9 2d 48 00', 16, _VEC_SIZE, lambda _: None)
    assert result1.undefined_error_count == 0
    assert result1.duplicate_error_count == 0
    assert len(result1.duplicate_instruction_pairs) == 0

    result2 = _check(
        'tests/common/arm.yaml', '1110 1001 0010 1101 0100 1000 0000 0000', 2, _VEC_SIZE, lambda _: None)
    assert result2.undefined_error_count == 0
    assert result2.duplicate_error_count == 0
    assert len(result2.duplicate_instruction_pairs) == 0


def test__check_no_mask_code16x2() -> None:
    result1 = _check('tests/common/arm_thumb.yaml',
                     'e9 2d 40 01', 16, _VEC_SIZE, lambda _: None)
    assert result1.undefined_error_count == 0
    assert result1.duplicate_error_count == 0
    assert len(result1.duplicate_instruction_pairs) == 0


def test__check_one_character_mask() -> None:
    # First letter
    errors1 = []
    result1 = _check('tests/common/arm.yaml', 'x9 2d 48 00', 16, _VEC_SIZE,
                     lambda error: errors1.extend(error))
    assert len(errors1) == 1
    assert result1.undefined_error_count == 1
    assert result1.duplicate_error_count == 0
    assert len(result1.duplicate_instruction_pairs) == 0

    assert errors1[0].type == 'undefined'
    assert errors1[0].bits_start == 0xf92d4800
    assert errors1[0].bits_end == 0xf92d4800

    result2 = _check(
        'tests/common/arm.yaml', 'x110 1001 0010 1101 0100 1000 0000 0000', 2, _VEC_SIZE, lambda _: None)
    assert result2.undefined_error_count == 0
    assert result2.duplicate_error_count == 0
    assert len(result2.duplicate_instruction_pairs) == 0

    # Halfway
    errors3 = []
    result3 = _check('tests/common/arm.yaml', 'ex 2d 48 00', 16, _VEC_SIZE,
                     lambda error: errors3.extend(error))
    assert len(errors3) == 2
    assert result3.undefined_error_count == 15
    assert result3.duplicate_error_count == 0
    assert len(result3.duplicate_instruction_pairs) == 0

    assert errors3[0].type == 'undefined'
    assert errors3[0].bits_start == 0xe02d4800
    assert errors3[0].bits_end == 0xe82d4800

    assert errors3[1].type == 'undefined'
    assert errors3[1].bits_start == 0xea2d4800
    assert errors3[1].bits_end == 0xef2d4800

    errors4 = []
    result4 = _check('tests/common/arm.yaml', '111x 1001 0010 1101 0100 1000 0000 0000',
                     2, _VEC_SIZE, lambda error: errors4.extend(error))
    assert len(errors4) == 1
    assert result4.undefined_error_count == 1
    assert result4.duplicate_error_count == 0
    assert len(result4.duplicate_instruction_pairs) == 0

    assert errors4[0].type == 'undefined'
    assert errors4[0].bits_start == 0xf92d4800
    assert errors4[0].bits_end == 0xf92d4800

    # Last letter
    result5 = _check('tests/common/arm.yaml',
                     'e9 2d 48 0x', 16, _VEC_SIZE, lambda _: None)
    assert result5.undefined_error_count == 0
    assert result5.duplicate_error_count == 0
    assert len(result5.duplicate_instruction_pairs) == 0

    result6 = _check(
        'tests/common/arm.yaml', '1110 1001 0010 1101 0100 1000 0000 000x', 2, _VEC_SIZE, lambda _: None)
    assert result6.undefined_error_count == 0
    assert result6.duplicate_error_count == 0
    assert len(result6.duplicate_instruction_pairs) == 0


def test__check_sequential_mask() -> None:
    errors1 = []
    result1 = _check('tests/common/arm.yaml', 'ex xd 48 00', 16, _VEC_SIZE,
                     lambda error: errors1.extend(error))
    assert len(errors1) == 3
    assert result1.undefined_error_count == 40 + 104 + 109
    assert result1.duplicate_error_count == 0
    assert len(result1.duplicate_instruction_pairs) == 0

    assert errors1[0].type == 'undefined'
    assert errors1[0].bits_start == 0xe00d4800
    assert errors1[0].bits_end == 0xe27d4800

    assert errors1[1].type == 'undefined'
    assert errors1[1].bits_start == 0xe2ad4800
    assert errors1[1].bits_end == 0xe91d4800

    assert errors1[2].type == 'undefined'
    assert errors1[2].bits_start == 0xe93d4800
    assert errors1[2].bits_end == 0xeffd4800

    errors2 = []
    result2 = _check('tests/common/arm.yaml', '111x x001 0010 1101 0100 1000 0000 0000',
                     2, _VEC_SIZE, lambda error: errors2.extend(error))
    assert len(errors2) == 2
    assert result2.undefined_error_count == 3
    assert result2.duplicate_error_count == 0
    assert len(result2.duplicate_instruction_pairs) == 0

    assert errors2[0].type == 'undefined'
    assert errors2[0].bits_start == 0xe12d4800
    assert errors2[0].bits_end == 0xe12d4800

    assert errors2[1].type == 'undefined'
    assert errors2[1].bits_start == 0xf12d4800
    assert errors2[1].bits_end == 0xf92d4800


def test__check_split_mask() -> None:
    errors1 = []
    result1 = _check('tests/common/arm.yaml', 'ex 2x 48 00', 16, _VEC_SIZE,
                     lambda error: errors1.extend(error))
    assert len(errors1) == 2
    assert result1.undefined_error_count == 157 + 98
    assert result1.duplicate_error_count == 0
    assert len(result1.duplicate_instruction_pairs) == 0

    assert errors1[0].type == 'undefined'
    assert errors1[0].bits_start == 0xe0204800
    assert errors1[0].bits_end == 0xe92c4800

    assert errors1[1].type == 'undefined'
    assert errors1[1].bits_start == 0xe92e4800
    assert errors1[1].bits_end == 0xef2f4800

    errors2 = []
    result2 = _check('tests/common/arm.yaml', '111x 100x 0010 1101 0100 1000 0000 0000',
                     2, _VEC_SIZE, lambda error: errors2.extend(error))
    assert len(errors2) == 2
    assert result2.undefined_error_count == 3
    assert result2.duplicate_error_count == 0
    assert len(result2.duplicate_instruction_pairs) == 0

    assert errors2[0].type == 'undefined'
    assert errors2[0].bits_start == 0xe82d4800
    assert errors2[0].bits_end == 0xe82d4800

    assert errors2[1].type == 'undefined'
    assert errors2[1].bits_start == 0xf82d4800
    assert errors2[1].bits_end == 0xf92d4800


def test__check_undefined() -> None:
    errors1 = []
    result1 = _check('tests/common/arm.yaml', 'ex xd 48 00', 16, _VEC_SIZE,
                     lambda error: errors1.extend(error))
    assert len(errors1) == 3
    assert result1.undefined_error_count == 40 + 104 + 109
    assert result1.duplicate_error_count == 0
    assert len(result1.duplicate_instruction_pairs) == 0

    assert errors1[0].type == 'undefined'
    assert errors1[0].bits_start == 0xe00d4800
    assert errors1[0].bits_end == 0xe27d4800

    assert errors1[1].type == 'undefined'
    assert errors1[1].bits_start == 0xe2ad4800
    assert errors1[1].bits_end == 0xe91d4800

    assert errors1[2].type == 'undefined'
    assert errors1[2].bits_start == 0xe93d4800
    assert errors1[2].bits_end == 0xeffd4800

    errors2 = []
    result2 = _check('tests/common/arm.yaml', '111x x001 0010 1101 0100 1000 0000 0000',
                     2, _VEC_SIZE, lambda error: errors2.extend(error))
    assert len(errors2) == 2
    assert result2.undefined_error_count == 3
    assert result2.duplicate_error_count == 0
    assert len(result2.duplicate_instruction_pairs) == 0

    assert errors2[0].type == 'undefined'
    assert errors2[0].bits_start == 0xe12d4800
    assert errors2[0].bits_end == 0xe12d4800

    assert errors2[1].type == 'undefined'
    assert errors2[1].bits_start == 0xf12d4800
    assert errors2[1].bits_end == 0xf92d4800


def test__check_duplicate() -> None:
    errors1 = []
    result1 = _check('tests/common/duplicate_instructions.yaml',
                     'ex xd 48 00', 16, _VEC_SIZE, lambda error: errors1.extend(error))
    assert len(errors1) == 3
    assert result1.undefined_error_count == 146 + 109
    assert result1.duplicate_error_count == 1
    assert len(result1.duplicate_instruction_pairs) == 1

    assert errors1[0].type == 'undefined'
    assert errors1[0].bits_start == 0xe00d4800
    assert errors1[0].bits_end == 0xe91d4800

    assert errors1[1].type == 'duplicate'
    assert errors1[1].bits_start == 0xe92d4800
    assert errors1[1].bits_end == 0xe92d4800

    assert errors1[2].type == 'undefined'
    assert errors1[2].bits_start == 0xe93d4800
    assert errors1[2].bits_end == 0xeffd4800

    assert ['duplicate_instruction_1',
            'duplicate_instruction_2'] in result1.duplicate_instruction_pairs

    errors2 = []
    result2 = _check('tests/common/duplicate_instructions.yaml',
                     '111x x001 0010 1101 0100 1000 0000 0000', 2, _VEC_SIZE, lambda error: errors2.extend(error))
    assert len(errors2) == 4
    assert result2.undefined_error_count == 2
    assert result2.duplicate_error_count == 2
    assert len(result2.duplicate_instruction_pairs) == 1

    assert errors2[0].type == 'undefined'
    assert errors2[0].bits_start == 0xe12d4800
    assert errors2[0].bits_end == 0xe12d4800

    assert errors2[1].type == 'duplicate'
    assert errors2[1].bits_start == 0xe92d4800
    assert errors2[1].bits_end == 0xe92d4800

    assert errors2[2].type == 'undefined'
    assert errors2[2].bits_start == 0xf12d4800
    assert errors2[2].bits_end == 0xf12d4800

    assert errors2[3].type == 'duplicate'
    assert errors2[3].bits_start == 0xf92d4800
    assert errors2[3].bits_end == 0xf92d4800

    assert ['duplicate_instruction_1',
            'duplicate_instruction_2'] in result2.duplicate_instruction_pairs


def test__check_with_small_vec_size() -> None:
    # A duplicate error range is not split into two checking batches
    # and the next duplicate error range is in the next checking batch
    errors = []
    result = _check('tests/common/duplicate_instructions_2pair.yaml',
                    '00xx', 16, 16, lambda error: errors.extend(error))
    assert len(errors) == 5
    assert result.undefined_error_count == 256 - 17
    assert result.duplicate_error_count == 17
    assert len(result.duplicate_instruction_pairs) == 2

    assert errors[0].type == 'undefined'
    assert errors[0].bits_start == 0x00000000
    assert errors[0].bits_end == 0x000f0000

    assert errors[1].type == 'duplicate'
    assert errors[1].bits_start == 0x00100000
    assert errors[1].bits_end == 0x001f0000

    assert errors[2].type == 'undefined'
    assert errors[2].bits_start == 0x00200000
    assert errors[2].bits_end == 0x00210000

    assert errors[3].type == 'duplicate'
    assert errors[3].bits_start == 0x00220000
    assert errors[3].bits_end == 0x00220000

    assert errors[4].type == 'undefined'
    assert errors[4].bits_start == 0x00230000
    assert errors[4].bits_end == 0x00ff0000

    assert ['duplicate_instruction_1_1',
            'duplicate_instruction_1_2'] == result.duplicate_instruction_pairs[0]
    assert ['duplicate_instruction_2_1',
            'duplicate_instruction_2_2'] == result.duplicate_instruction_pairs[1]

    # A duplicate error range is not split into two checking batches
    # and the next duplicate error range is not in the next checking batch
    errors = []
    result = _check('tests/common/duplicate_instructions_2pair.yaml',
                    '00xx', 16, 35, lambda error: errors.extend(error))
    assert len(errors) == 5
    assert result.undefined_error_count == 256 - 17
    assert result.duplicate_error_count == 17
    assert len(result.duplicate_instruction_pairs) == 2

    assert errors[0].type == 'undefined'
    assert errors[0].bits_start == 0x00000000
    assert errors[0].bits_end == 0x000f0000

    assert errors[1].type == 'duplicate'
    assert errors[1].bits_start == 0x00100000
    assert errors[1].bits_end == 0x001f0000

    assert errors[2].type == 'undefined'
    assert errors[2].bits_start == 0x00200000
    assert errors[2].bits_end == 0x00210000

    assert errors[3].type == 'duplicate'
    assert errors[3].bits_start == 0x00220000
    assert errors[3].bits_end == 0x00220000

    assert errors[4].type == 'undefined'
    assert errors[4].bits_start == 0x00230000
    assert errors[4].bits_end == 0x00ff0000

    assert ['duplicate_instruction_1_1',
            'duplicate_instruction_1_2'] == result.duplicate_instruction_pairs[0]
    assert ['duplicate_instruction_2_1',
            'duplicate_instruction_2_2'] == result.duplicate_instruction_pairs[1]

    # A duplicate error range is split into two checking batches
    errors = []
    result = _check('tests/common/duplicate_instructions_2pair.yaml',
                    '00xx', 16, 15, lambda error: errors.extend(error))
    assert len(errors) == 5
    assert result.undefined_error_count == 256 - 17
    assert result.duplicate_error_count == 17
    assert len(result.duplicate_instruction_pairs) == 2

    assert errors[0].type == 'undefined'
    assert errors[0].bits_start == 0x00000000
    assert errors[0].bits_end == 0x000f0000

    assert errors[1].type == 'duplicate'
    assert errors[1].bits_start == 0x00100000
    assert errors[1].bits_end == 0x001f0000

    assert errors[2].type == 'undefined'
    assert errors[2].bits_start == 0x00200000
    assert errors[2].bits_end == 0x00210000

    assert errors[3].type == 'duplicate'
    assert errors[3].bits_start == 0x00220000
    assert errors[3].bits_end == 0x00220000

    assert errors[4].type == 'undefined'
    assert errors[4].bits_start == 0x00230000
    assert errors[4].bits_end == 0x00ff0000

    assert ['duplicate_instruction_1_1',
            'duplicate_instruction_1_2'] == result.duplicate_instruction_pairs[0]
    assert ['duplicate_instruction_2_1',
            'duplicate_instruction_2_2'] == result.duplicate_instruction_pairs[1]

    # A undefined error range is not split into two checking batches
    # and the next undefined error range is in the next checking batch
    errors = []
    result = _check('tests/common/duplicate_instructions_2pair.yaml',
                    '00xx', 16, 34, lambda error: errors.extend(error))
    assert len(errors) == 5
    assert result.undefined_error_count == 256 - 17
    assert result.duplicate_error_count == 17
    assert len(result.duplicate_instruction_pairs) == 2

    assert errors[0].type == 'undefined'
    assert errors[0].bits_start == 0x00000000
    assert errors[0].bits_end == 0x000f0000

    assert errors[1].type == 'duplicate'
    assert errors[1].bits_start == 0x00100000
    assert errors[1].bits_end == 0x001f0000

    assert errors[2].type == 'undefined'
    assert errors[2].bits_start == 0x00200000
    assert errors[2].bits_end == 0x00210000

    assert errors[3].type == 'duplicate'
    assert errors[3].bits_start == 0x00220000
    assert errors[3].bits_end == 0x00220000

    assert errors[4].type == 'undefined'
    assert errors[4].bits_start == 0x00230000
    assert errors[4].bits_end == 0x00ff0000

    assert ['duplicate_instruction_1_1',
            'duplicate_instruction_1_2'] == result.duplicate_instruction_pairs[0]
    assert ['duplicate_instruction_2_1',
            'duplicate_instruction_2_2'] == result.duplicate_instruction_pairs[1]

    # A undefined error range is not split into two checking batches
    # and the next undefined error range is not in the next checking batch
    errors = []
    result = _check('tests/common/duplicate_instructions_2pair.yaml',
                    '00xx', 16, 16, lambda error: errors.extend(error))
    assert len(errors) == 5
    assert result.undefined_error_count == 256 - 17
    assert result.duplicate_error_count == 17
    assert len(result.duplicate_instruction_pairs) == 2

    assert errors[0].type == 'undefined'
    assert errors[0].bits_start == 0x00000000
    assert errors[0].bits_end == 0x000f0000

    assert errors[1].type == 'duplicate'
    assert errors[1].bits_start == 0x00100000
    assert errors[1].bits_end == 0x001f0000

    assert errors[2].type == 'undefined'
    assert errors[2].bits_start == 0x00200000
    assert errors[2].bits_end == 0x00210000

    assert errors[3].type == 'duplicate'
    assert errors[3].bits_start == 0x00220000
    assert errors[3].bits_end == 0x00220000

    assert errors[4].type == 'undefined'
    assert errors[4].bits_start == 0x00230000
    assert errors[4].bits_end == 0x00ff0000

    assert ['duplicate_instruction_1_1',
            'duplicate_instruction_1_2'] == result.duplicate_instruction_pairs[0]
    assert ['duplicate_instruction_2_1',
            'duplicate_instruction_2_2'] == result.duplicate_instruction_pairs[1]

    # A undefined error range is split into two checking batches
    errors = []
    result = _check('tests/common/duplicate_instructions_2pair.yaml',
                    '00xx', 16, 15, lambda error: errors.extend(error))
    assert len(errors) == 5
    assert result.undefined_error_count == 256 - 17
    assert result.duplicate_error_count == 17
    assert len(result.duplicate_instruction_pairs) == 2

    assert errors[0].type == 'undefined'
    assert errors[0].bits_start == 0x00000000
    assert errors[0].bits_end == 0x000f0000

    assert errors[1].type == 'duplicate'
    assert errors[1].bits_start == 0x00100000
    assert errors[1].bits_end == 0x001f0000

    assert errors[2].type == 'undefined'
    assert errors[2].bits_start == 0x00200000
    assert errors[2].bits_end == 0x00210000

    assert errors[3].type == 'duplicate'
    assert errors[3].bits_start == 0x00220000
    assert errors[3].bits_end == 0x00220000

    assert errors[4].type == 'undefined'
    assert errors[4].bits_start == 0x00230000
    assert errors[4].bits_end == 0x00ff0000

    assert ['duplicate_instruction_1_1',
            'duplicate_instruction_1_2'] == result.duplicate_instruction_pairs[0]
    assert ['duplicate_instruction_2_1',
            'duplicate_instruction_2_2'] == result.duplicate_instruction_pairs[1]


def test__check_match_equality_condition() -> None:
    result = _check(
        'tests/common/primitive_condition.yaml', '10 00 00 00', 16, _VEC_SIZE, lambda error: None)
    assert result.no_error_count == 1
    assert result.undefined_error_count == 0
    assert result.duplicate_error_count == 0


def test__check_unmatch_equality_condition() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '00 00 00 00', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 0
    assert result1.undefined_error_count == 1
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/primitive_condition.yaml', '20 00 00 00', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 0
    assert result2.undefined_error_count == 1
    assert result2.duplicate_error_count == 0


def test__check_match_in_condition() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '10 00 00 01', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 1
    assert result1.undefined_error_count == 0
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/primitive_condition.yaml', '30 00 00 01', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 1
    assert result2.undefined_error_count == 0
    assert result2.duplicate_error_count == 0


def test__check_unmatch_in_condition() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '00 00 00 01', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 0
    assert result1.undefined_error_count == 1
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/primitive_condition.yaml', '20 00 00 01', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 0
    assert result2.undefined_error_count == 1
    assert result2.duplicate_error_count == 0


def test__check_match_in_range_condition() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '00 00 00 02', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 1
    assert result1.undefined_error_count == 0
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/primitive_condition.yaml', 'b0 00 00 02', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 1
    assert result2.undefined_error_count == 0
    assert result2.duplicate_error_count == 0


def test__check_unmatch_in_range_condition() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '10 00 00 02', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 0
    assert result1.undefined_error_count == 1
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/primitive_condition.yaml', 'a0 00 00 02', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 0
    assert result2.undefined_error_count == 1
    assert result2.duplicate_error_count == 0


def test__check_match_field_element_subject() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '10 00 00 03', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 1
    assert result1.undefined_error_count == 0
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/primitive_condition.yaml', '30 00 00 03', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 1
    assert result2.undefined_error_count == 0
    assert result2.duplicate_error_count == 0


def test__check_unmatch_field_element_subject() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '20 00 00 03', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 0
    assert result1.undefined_error_count == 1
    assert result1.duplicate_error_count == 0


def test__check_match_field_object() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '00 00 00 04', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 1
    assert result1.undefined_error_count == 0
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/primitive_condition.yaml', '11 00 00 04', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 1
    assert result2.undefined_error_count == 0
    assert result2.duplicate_error_count == 0


def test__check_unmatch_field_object() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '01 00 00 04', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 0
    assert result1.undefined_error_count == 1
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/primitive_condition.yaml', '10 00 00 04', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 0
    assert result2.undefined_error_count == 1
    assert result2.duplicate_error_count == 0


def test__check_match_function_subject() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '30 00 00 05', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 1
    assert result1.undefined_error_count == 0
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/primitive_condition.yaml', 'a0 00 00 05', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 1
    assert result2.undefined_error_count == 0
    assert result2.duplicate_error_count == 0


def test__check_unmatch_function_subject() -> None:
    result1 = _check(
        'tests/common/primitive_condition.yaml', '10 00 00 05', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 0
    assert result1.undefined_error_count == 1
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/primitive_condition.yaml', 'e0 00 00 05', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 0
    assert result2.undefined_error_count == 1
    assert result2.duplicate_error_count == 0


def test__check_match_and_condition() -> None:
    result1 = _check(
        'tests/common/complex_condition.yaml', '12 00 00 00', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 1
    assert result1.undefined_error_count == 0
    assert result1.duplicate_error_count == 0


def test__check_unmatch_and_condition() -> None:
    result1 = _check(
        'tests/common/complex_condition.yaml', '11 00 00 00', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 0
    assert result1.undefined_error_count == 1
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/complex_condition.yaml', '22 00 00 00', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 0
    assert result2.undefined_error_count == 1
    assert result2.duplicate_error_count == 0


def test__check_match_or_condition() -> None:
    result1 = _check(
        'tests/common/complex_condition.yaml', '21 00 00 01', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 1
    assert result1.undefined_error_count == 0
    assert result1.duplicate_error_count == 0


def test__check_unmatch_or_condition() -> None:
    result1 = _check(
        'tests/common/complex_condition.yaml', '02 00 00 01', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 0
    assert result1.undefined_error_count == 1
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/complex_condition.yaml', '10 00 00 01', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 0
    assert result2.undefined_error_count == 1
    assert result2.duplicate_error_count == 0


def test__check_match_andor_condition() -> None:
    result1 = _check(
        'tests/common/complex_condition.yaml', '12 00 00 02', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 1
    assert result1.undefined_error_count == 0
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/complex_condition.yaml', '30 00 00 02', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 1
    assert result2.undefined_error_count == 0
    assert result2.duplicate_error_count == 0

    result3 = _check(
        'tests/common/complex_condition.yaml', '11 00 00 03', 16, _VEC_SIZE, lambda error: None)
    assert result3.no_error_count == 1
    assert result3.undefined_error_count == 0
    assert result3.duplicate_error_count == 0

    result4 = _check(
        'tests/common/complex_condition.yaml', '22 00 00 03', 16, _VEC_SIZE, lambda error: None)
    assert result4.no_error_count == 1
    assert result4.undefined_error_count == 0
    assert result4.duplicate_error_count == 0


def test__check_unmatch_andor_condition() -> None:
    result1 = _check(
        'tests/common/complex_condition.yaml', '11 00 00 02', 16, _VEC_SIZE, lambda error: None)
    assert result1.no_error_count == 0
    assert result1.undefined_error_count == 1
    assert result1.duplicate_error_count == 0

    result2 = _check(
        'tests/common/complex_condition.yaml', '22 00 00 02', 16, _VEC_SIZE, lambda error: None)
    assert result2.no_error_count == 0
    assert result2.undefined_error_count == 1
    assert result2.duplicate_error_count == 0

    result3 = _check(
        'tests/common/complex_condition.yaml', '12 00 00 03', 16, _VEC_SIZE, lambda error: None)
    assert result3.no_error_count == 0
    assert result3.undefined_error_count == 1
    assert result3.duplicate_error_count == 0

    result4 = _check(
        'tests/common/complex_condition.yaml', '30 00 00 03', 16, _VEC_SIZE, lambda error: None)
    assert result4.no_error_count == 0
    assert result4.undefined_error_count == 1
    assert result4.duplicate_error_count == 0
