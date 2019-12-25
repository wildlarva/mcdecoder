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
    # Make template arguments
    ns_prefix = mcdecoder_model.machine_decoder.namespace_prefix
    template_args = {
        'mc_decoder': mcdecoder_model,
        'machine_decoder': mcdecoder_model.machine_decoder,
        'instruction_decoders': mcdecoder_model.instruction_decoders,
        'ns': ns_prefix,
    }

    # Find templates
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('mcdecoder', 'templates/athrill')
    )
    template_files = env.list_templates()

    # Generate files
    for template_file in template_files:
        # Load template
        template = env.get_template(template_file)

        # Determine generating file path
        output_file = os.path.join('out', jinja2.Template(
            template_file).render(template_args))

        # Make output directory
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        elif not os.path.isdir(output_dir):
            return False

        # Generate file
        with open(output_file, 'w') as file:
            file.write(template.render(template_args))

    return True
