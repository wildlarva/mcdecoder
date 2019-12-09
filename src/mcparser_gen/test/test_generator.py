from mcparser_gen.generator import _create_mcparser_model, _generate, ArgParser, McParser, OpParser


def test_create_mcparser_model():
    mcparser_model: McParser = _create_mcparser_model(
        'test/arm.yaml')

    assert len(mcparser_model.op_parsers) == 2

    op_parser_model_add_1, op_parser_model_push_1 = mcparser_model.op_parsers
    assert op_parser_model_add_1.name == 'add_1'
    assert op_parser_model_add_1.fixed_bits_mask == 0x0fe00000
    assert op_parser_model_add_1.fixed_bits == 0x02800000
    assert len(op_parser_model_add_1.arg_parsers) == 5

    arg_cond: ArgParser = op_parser_model_add_1.arg_parsers[0]
    assert arg_cond.name == 'cond'
    assert arg_cond.mask == 0xf0000000
    assert arg_cond.start_bit == 31
    assert arg_cond.end_bit == 28
    assert arg_cond.type_bit_size == 8


def test_generate():
    mcparser_model: McParser = McParser(
        op_parsers=[
            OpParser(
                name='add_1',
                fixed_bits_mask=0x0fe00000,
                fixed_bits=0x02800000,
                arg_parsers=[
                    ArgParser(name='cond', mask=0xf0000000,
                              start_bit=31, end_bit=28, type_bit_size=8, ),
                    ArgParser(name='S', mask=0x00100000, start_bit=20,
                              end_bit=20, type_bit_size=8, ),
                ],
            ),
            OpParser(
                name='push_1',
                fixed_bits_mask=0x0fe00000,
                fixed_bits=0x02800000,
                arg_parsers=[
                    ArgParser(name='cond', mask=0xf0000000, start_bit=31,
                              end_bit=28, type_bit_size=8, ),
                    ArgParser(name='register_list', mask=0x0000ffff,
                              start_bit=15,  end_bit=0, type_bit_size=16, ),
                ],
            ),
        ],
    )
    assert _generate(mcparser_model) == True
