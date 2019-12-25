import os

import jinja2
from mcdecoder import core


# External functions


def generate(mcfile_path: str) -> bool:
    """Generate MC decoder files from MC description file"""
    mcdecoder_model = core.create_mcdecoder_model(mcfile_path)
    return _generate(mcdecoder_model)


# Internal functions


def _generate(mcdecoder_model: core.McDecoder) -> bool:
    """Generate MC decoder files from a MC decoder model"""
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('mcdecoder', 'templates')
    )
    decoder_header_template = env.get_template('mcdecoder.h')
    decoder_source_template = env.get_template('mcdecoder.c')

    if not os.path.exists('out'):
        os.makedirs('out')
    elif not os.path.isdir('out'):
        return False

    ns_prefix = mcdecoder_model.machine_decoder.namespace_prefix
    template_args = {
        'mc_decoder': mcdecoder_model,
        'machine_decoder': mcdecoder_model.machine_decoder,
        'instruction_decoders': mcdecoder_model.instruction_decoders,
        'ns': ns_prefix,
    }

    with open(f'out/{ns_prefix}mcdecoder.h', 'w') as file:
        file.write(decoder_header_template.render(template_args))

    with open(f'out/{ns_prefix}mcdecoder.c', 'w') as file:
        file.write(decoder_source_template.render(template_args))

    return True
