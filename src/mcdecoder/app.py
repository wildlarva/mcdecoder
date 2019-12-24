import argparse
from dataclasses import dataclass
from typing import List, cast

from mcdecoder import generator


@dataclass
class _Arguments:
    command: str
    mc_file: str

    def __init__(self) -> None:
        pass


def run_app(argv: List[str]) -> int:
    # Create an argument parser
    parser = argparse.ArgumentParser(
        prog='python -m mcdecoder', description='Generate a machine code decoder', add_help=True)
    subparsers = parser.add_subparsers(
        dest='command', metavar='command', required=True)

    # Create a subparser for the command 'generate'
    generate_parser = subparsers.add_parser(
        'generate', help='Generate a decoder or other codes to support a decoder')
    generate_parser.add_argument(
        'mc_file', help='A path to a machine code descriptin file')

    # Parse an argument
    try:
        args: _Arguments = cast(_Arguments, parser.parse_args(
            argv[1:], namespace=_Arguments()))
    except SystemExit as se:
        return se.code

    # Run an individual command
    if args.command == 'generate':
        result = generator.generate(args.mc_file)
        if result:
            print('Generated MC decoders.')
        else:
            print('Error occurred on generation.')

    return 0
