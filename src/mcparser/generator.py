import os
import jinja2


def generate(mc_file):
    mcparser_model = _create_mcparser_model(mc_file)
    return _generate(mcparser_model)


def _create_mcparser_model(mc_file):
    return {}


def _generate(mcparser_model):
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('mcparser', 'templates')
    )
    parser_header_template = env.get_template('mcparser.h')
    parser_source_template = env.get_template('mcparser.c')

    if not os.path.isdir('out'):
        return False

    with open('out/mcparser.h', 'w') as file:
        file.write(parser_header_template.render(mcparser_model))

    with open('out/mcparser.c', 'w') as file:
        file.write(parser_source_template.render(mcparser_model))

    return True


# def test_generate():
#     assert generate('test/arm.yaml') == True

def test__generate():
    mcparser_model = {
        'parser': {},
        'op_parsers': [
            {
                'name': 'add_1',
                'fixed_bits_mask': 0x0fe00000,
                'fixed_bits': 0x02800000,
                'arg_parsers': [
                    {'name': 'cond', 'mask': 0xf0000000, 'start_bit': 31, 'end_bit': 28, 'bit_size': 8, },
                    {'name': 'S', 'mask': 0x00100000, 'start_bit': 20,  'end_bit': 20, 'bit_size': 8, },
                ],
            },
            {
                'name': 'push_1',
                'fixed_bits_mask': 0x0fe00000,
                'fixed_bits': 0x02800000,
                'arg_parsers': [
                    {'name': 'cond', 'mask': 0xf0000000, 'start_bit': 31,  'end_bit': 28, 'bit_size': 8, },
                    {'name': 'register_list', 'mask': 0x0000ffff, 'start_bit': 15,  'end_bit': 0, 'bit_size': 16, },
                ],
            },
        ],
    }
    assert _generate(mcparser_model) == True
