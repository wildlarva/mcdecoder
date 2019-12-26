import os

import jinja2
from mcdecoder import core


# External functions


def generate(mcfile_path: str, output_directory: str = None, template_directory: str = None) -> bool:
    """Generate MC decoder files from MC description file"""
    # Create decoder model
    mcdecoder_model = core.create_mcdecoder_model(mcfile_path)

    # Create template loader
    if template_directory is None:
        loader = jinja2.PackageLoader('mcdecoder', 'templates/athrill')
    else:
        loader = jinja2.FileSystemLoader(template_directory)

    # Default output directory to the current
    if output_directory is None:
        output_directory = '.'

    # Generate
    return _generate(mcdecoder_model, output_directory, loader)


# Internal functions


def _generate(mcdecoder_model: core.McDecoder, output_directory: str, template_loader: jinja2.BaseLoader) -> bool:
    """Generate MC decoder files from a MC decoder model"""
    # Make template arguments
    template_args = {
        'mcdecoder': mcdecoder_model,
        'machine_decoder': mcdecoder_model.machine_decoder,
        'instruction_decoders': mcdecoder_model.instruction_decoders,
        # Shorthand for machine_decoder.namespace_prefix
        'ns': mcdecoder_model.namespace_prefix,
        'extras': mcdecoder_model.extras,  # Shorthand for mcdecoder.extras
    }

    # Find templates
    env = jinja2.Environment(loader=template_loader)
    template_files = env.list_templates()

    # Generate files
    for template_file in template_files:
        # Load template
        template = env.get_template(template_file)

        # Determine generating file path
        output_file = os.path.join(output_directory, jinja2.Template(
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
