import argparse
from dataclasses import dataclass
from typing import List, Literal, Optional, cast

from mcdecoder import emulator, exporter, generator


# External functions


def run_app(argv: List[str]) -> int:
    # Create an argument parser
    parser = _create_parser()

    # Parse an argument
    try:
        args = cast(_Arguments, parser.parse_args(
            argv[1:], namespace=_Arguments()))
    except SystemExit as se:
        return se.code

    # Run an individual command
    if args.command == 'generate':
        return generator.generate(
            args.mcfile, output_directory=args.output_directory, template_directory=args.template_directory)

    elif args.command == 'export':
        return exporter.export(args.mcfile, args.output_file)

    elif args.command == 'emulate':
        return emulator.emulate(args.mcfile, args.bit_pattern,
                                base=args.base, byteorder=args.byteorder)

    return 0


# Internal classes


@dataclass
class _Arguments:
    command: Literal['generate', 'export', 'emulate']
    mcfile: Optional[str]
    output_directory: Optional[str]
    output_file: Optional[str]
    template_directory: Optional[str]
    bit_pattern: Optional[str]
    base: Optional[Literal[2, 16]]
    byteorder: Optional[Literal['big', 'little']]

    def __init__(self) -> None:
        pass


# Internal functions
def _create_parser() -> argparse.ArgumentParser:
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

    # Create a subparser for the command 'emulate'
    emulate_parser = subparsers.add_parser(
        'emulate', help='Emulate a decoder.')
    emulate_parser.add_argument(
        '--pattern', metavar='bits', dest='bit_pattern', required=True, help='A bit pattern as a input for a decoder')
    emulate_parser.add_argument(
        '--base', choices=[2, 16], type=int, help='The base of a bit pattern')
    emulate_parser.add_argument(
        '--byteorder', choices=['big', 'little'], help='The byte order of a bit pattern')
    emulate_parser.add_argument(
        'mcfile', help='A path to a machine code description file')

    return parser
