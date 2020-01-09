import os

import jinja2

from . import common, core


# External functions


def generate(mcfile_path: str, output_directory: str = None, template_directory: str = None) -> int:
    """
    Implementation the sub-command 'generate'.

    Generate MC decoder files from MC description file.

    If output_directory is not specified, it is defaulted to the current directory.
    If template_directory is not specified, the default decoder template (athrill decoder) is used.

    :param mcfile_path: Path to an MC description file
    :param output_directory: Path to an output directory of generated codes
    :param template_directory: Path to a directory including template files
    :return: Exit code of mcdecoder
    """
    # Default output directory to the current
    if output_directory is None:
        output_directory = '.'

    # Create decoder model
    mcdecoder_model = core.create_mcdecoder_model(mcfile_path)

    # Create template loader
    if template_directory is None:
        loader = jinja2.PackageLoader('mcdecoder', 'templates/athrill')
    else:
        loader = jinja2.FileSystemLoader(template_directory)

    # Generate
    result = _generate(mcdecoder_model, output_directory, loader)
    if result:
        print('Generated codes.')
        return 0
    else:
        print('Error occurred on generation.')
        return 1


# Internal functions


def _generate(mcdecoder_model: core.McDecoder, output_directory: str, template_loader: jinja2.BaseLoader) -> bool:
    """Generate MC decoder files from a MC decoder model"""
    # Make template arguments
    template_args = {
        'mcdecoder': mcdecoder_model,
        'machine_decoder': mcdecoder_model.machine_decoder,
        'instruction_decoders': mcdecoder_model.instruction_decoders,
        # Shorthand for mcdecoder.namespace_prefix
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
        if not common.make_parent_directories(output_file):
            return False

        # Generate file
        with open(output_file, 'w') as file:
            file.write(template.render(template_args))

    return True
