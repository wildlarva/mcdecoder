import argparse
from dataclasses import dataclass
from typing import List, Optional, cast

from mcdecoder import exporter, generator


@dataclass
class _Arguments:
    command: str
    mcfile: Optional[str]
    output_file: Optional[str]

    def __init__(self) -> None:
        pass


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
        'mcfile', help='A path to a machine code descriptin file')

    # Create a subparser for the command 'export'
    export_parser = subparsers.add_parser(
        'export', help='Export a MC description as another format. Currently, mcdecoder only supports CSV format.')
    export_parser.add_argument(
        '--output', dest='output_file', help='A path to a output file')
    export_parser.add_argument(
        'mcfile', help='A path to a machine code descriptin file')

    # Parse an argument
    try:
        args: _Arguments = cast(_Arguments, parser.parse_args(
            argv[1:], namespace=_Arguments()))
    except SystemExit as se:
        return se.code

    # Run an individual command
    if args.command == 'generate':
        result = generator.generate(args.mcfile)
        if result:
            print('Generated MC decoders.')
        else:
            print('Error occurred on generation.')

    elif args.command == 'export':
        result = exporter.export(args.mcfile, args.output_file)
        if result:
            print('Exported a MC description.')
        else:
            print('Error occurred on exporting.')


    return 0
