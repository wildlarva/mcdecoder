import argparse
from dataclasses import dataclass
from typing import List, Optional, cast

from mcdecoder import exporter, generator


# External functions


def run_app(argv: List[str]) -> int:
    # Create an argument parser
    parser = argparse.ArgumentParser(
        prog='mcdecoder', description='Generate a machine code decoder', add_help=True)
    subparsers = parser.add_subparsers(
        dest='command', metavar='command', required=True)

    # Create a subparser for the command 'generate'
    generate_parser = subparsers.add_parser(
        'generate', help='Generate a decoder or other codes to support a decoder')
    generate_parser.add_argument(
        '--output', metavar='outdir', dest='output_directory', help='A path to an output directory')
    generate_parser.add_argument(
        '--template', metavar='templatedir', dest='template_directory', help='A path to a directoy including user-defined template files')
    generate_parser.add_argument(
        'mcfile', help='A path to a machine code description file')

    # Create a subparser for the command 'export'
    export_parser = subparsers.add_parser(
        'export', help='Export an MC description as another format. Currently, mcdecoder only supports CSV format.')
    export_parser.add_argument(
        '--output', metavar='outfile', dest='output_file', required=True, help='A path to an output file')
    export_parser.add_argument(
        'mcfile', help='A path to a machine code description file')

    # Parse an argument
    try:
        args: _Arguments = cast(_Arguments, parser.parse_args(
            argv[1:], namespace=_Arguments()))
    except SystemExit as se:
        return se.code

    # Run an individual command
    if args.command == 'generate':
        result = generator.generate(
            args.mcfile, output_directory=args.output_directory, template_directory=args.template_directory)
        if result:
            print('Generated machine code decoders.')
        else:
            print('Error occurred on generation.')

    elif args.command == 'export':
        result = exporter.export(args.mcfile, args.output_file)
        if result:
            print('Exported a machine code description.')
        else:
            print('Error occurred on exporting.')

    return 0


# Internal classes


@dataclass
class _Arguments:
    command: str
    mcfile: Optional[str]
    output_directory: Optional[str]
    output_file: Optional[str]
    template_directory: Optional[str]

    def __init__(self) -> None:
        pass
