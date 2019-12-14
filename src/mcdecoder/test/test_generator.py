from mcparser_gen.generator import (
    ArgParser, MachineParser, McParser, OpParser, _create_mcparser_model,
    _generate)


def test_create_mcparser_model_namespace() -> None:
    mcparser_model = _create_mcparser_model(
        'test/arm.yaml')

    mcparser_model.machine_parser.namespace == 'arm'


def test_create_mcparser_model_32bit_instructions() -> None:
    mcparser_model = _create_mcparser_model(
        'test/arm.yaml')

    assert len(mcparser_model.op_parsers) == 2

    op_parser_model_add_1, op_parser_model_push_1 = mcparser_model.op_parsers
    assert op_parser_model_add_1.name == 'add_1'
    assert op_parser_model_add_1.fixed_bits_mask == 0x0fe00000
    assert op_parser_model_add_1.fixed_bits == 0x02800000
    assert op_parser_model_add_1.type_bit_size == 32
    assert len(op_parser_model_add_1.arg_parsers) == 5

    arg_cond = op_parser_model_add_1.arg_parsers[0]
    assert arg_cond.name == 'cond'
    assert arg_cond.mask == 0xf0000000
    assert arg_cond.start_bit == 31
    assert arg_cond.end_bit == 28
    assert arg_cond.type_bit_size == 8

    assert op_parser_model_push_1.name == 'push_1'


def test_create_mcparser_model_16bit_instructions() -> None:
    mcparser_model = _create_mcparser_model(
        'test/riscv.yaml')

    assert len(mcparser_model.op_parsers) == 2

    op_parser_model_addi_1, op_parser_model_sd_1 = mcparser_model.op_parsers
    assert op_parser_model_addi_1.name == 'c_addi_1'
    assert op_parser_model_addi_1.fixed_bits_mask == 0xe003
    assert op_parser_model_addi_1.fixed_bits == 0x0001
    assert op_parser_model_addi_1.type_bit_size == 16
    assert len(op_parser_model_addi_1.arg_parsers) == 5

    arg_cond = op_parser_model_addi_1.arg_parsers[0]
    assert arg_cond.name == 'funct3'
    assert arg_cond.mask == 0xe000
    assert arg_cond.start_bit == 15
    assert arg_cond.end_bit == 13
    assert arg_cond.type_bit_size == 8

    assert op_parser_model_sd_1.name == 'c_sd_1'


def test_generate() -> None:
    mcparser_model = McParser(
        machine_parser=MachineParser(namespace='ns'),
        op_parsers=[
            OpParser(
                name='add_1',
                fixed_bits_mask=0x0fe00000,
                fixed_bits=0x02800000,
                type_bit_size=32,
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
                type_bit_size=32,
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
