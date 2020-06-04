import argparse
from dataclasses import dataclass
import textwrap
from typing import List, Literal, Optional, cast

from . import __version__, checker, emulator, exporter, generator

# region External functions


def run_app(argv: List[str]) -> int:
    """
    Run the application workflow of mcdecoder.

    Parse argv and execute a corresponding sub-command.

    :param argv: Command line parameters
    :return: Exit code of mcdecoder
    """
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
        return generator.generate(cast(str, args.mcfile), type=args.generator_type, template_directory=args.template_directory,
                                  output_directory=cast(str, args.output_directory))

    elif args.command == 'export':
        return exporter.export(cast(str, args.mcfile), cast(str, args.output_file))

    elif args.command == 'emulate':
        assert args.base is not None
        assert args.byteorder is not None
        return emulator.emulate(cast(str, args.mcfile), cast(str, args.bit_pattern), base=args.base, byteorder=args.byteorder)

    elif args.command == 'check':
        assert args.base is not None
        return checker.check(cast(str, args.mcfile), cast(str, args.bit_pattern), base=args.base)

    return 0


# endregion

# region Internal classes


@dataclass
class _Arguments:
    command: Literal['generate', 'export', 'emulate', 'check']
    mcfile: Optional[str]
    output_directory: Optional[str]
    output_file: Optional[str]
    generator_type: Optional[str]
    template_directory: Optional[str]
    bit_pattern: Optional[str]
    base: Optional[Literal[2, 16]]
    byteorder: Optional[Literal['big', 'little']]

    def __init__(self) -> None:
        pass


# endregion

# region Internal functions
def _create_parser() -> argparse.ArgumentParser:
    # Create an argument parser
    parser = argparse.ArgumentParser(
        prog='mcdecoder', add_help=True, formatter_class=argparse.RawTextHelpFormatter,
        description='A toolset for a machine code decoder')
    subparsers = parser.add_subparsers(
        dest='command', metavar='command', required=True)
    parser.add_argument('--version', action='version',
                        version=f'mcdecoder {__version__.__version__}')

    # Create a subparser for the command 'generate'
    generate_parser = subparsers.add_parser(
        'generate', formatter_class=argparse.RawTextHelpFormatter, help='Generate a decoder or other codes to support a decoder', description='Generate a decoder or other codes to support a decoder', epilog=textwrap.dedent('''\
            Usage::
              
              # Generate a decoder to 'out' directory
              mcdecoder generate --output out mc.yaml

              # Generate codes with the generator 'athrill'
              mcdecoder generate --type athrill --output out mc.yaml
              
              # Generate codes according to user-defined template files in 'user_templates' directory
              mcdecoder generate --template user_templates --output out mc.yaml
            '''))  # noqa: W293
    generator_group = generate_parser.add_mutually_exclusive_group()
    generator_group.add_argument('--type', metavar='type', dest='generator_type', help=textwrap.dedent('''\
        The type of a generator used for generating codes. Possible generators are:

        * c_decoder: Generating standard decoder API in C
        * athrill: Generating decoder API for athrill
        '''))
    generator_group.add_argument(
        '--template', metavar='templatedir', dest='template_directory',
        help='A path to a directoy including user-defined template files')
    generate_parser.add_argument(
        '--output', metavar='outdir', dest='output_directory', default='.', help='A path to an output directory (default: .)')
    generate_parser.add_argument(
        'mcfile', help='A path to a machine code description file')

    # Create a subparser for the command 'export'
    export_parser = subparsers.add_parser(
        'export', formatter_class=argparse.RawTextHelpFormatter, help='Export an MC description as another format. Currently, mcdecoder only supports CSV format', description='Export an MC description as another format. Currently, mcdecoder only supports CSV format', epilog=textwrap.dedent('''
            Usage::

              # Export a MC description as CSV format
              mcdecoder export --output mc.csv mc.yaml
            '''))  # noqa: W293
    export_parser.add_argument(
        '--output', metavar='outfile', dest='output_file', required=True, help='A path to an output file')
    export_parser.add_argument(
        'mcfile', help='A path to a machine code description file')

    # Create a subparser for the command 'emulate'
    emulate_parser = subparsers.add_parser(
        'emulate', formatter_class=argparse.RawTextHelpFormatter, help='Emulate a decoder by inputting binary data', description='Emulate a decoder by inputting binary data', epilog=textwrap.dedent('''\
            Usage::

              # Emulate a decoder when inputting e92d4800
              mcdecoder emulate --input e92d4800 mc.yaml

              # Emulate a decoder when inputting '1110 1001 0010 1101 0100 1000 0000 0000'
              mcdecoder emulate --base 2 --input '1110 1001 0010 1101 0100 1000 0000 0000' mc.yaml

              # Emulate a decoder when inputting e92d4800 as little endian
              mcdecoder emulate --byteorder little --input 00482de9 mc.yaml
            '''))  # noqa: W293
    emulate_parser.add_argument(
        '--input', '--pattern', metavar='indata', dest='bit_pattern', required=True,
        help=textwrap.dedent('''\
            A binary/hex string as input binary data for a decoder.
            --pattern will be deprecated since 0.1b1'''))
    emulate_parser.add_argument(
        '--base', choices=[2, 16], default=16, type=int, help='The base of a binary/hex string (default: 16)')
    emulate_parser.add_argument(
        '--byteorder', choices=['big', 'little'], default='big', help='The byte order of a binary/hex string (default: big)')
    emulate_parser.add_argument(
        'mcfile', help='A path to a machine code description file')

    # Create a subparser for the command 'check'
    emulate_parser = subparsers.add_parser(
        'check', formatter_class=argparse.RawTextHelpFormatter, help='Check the instruction validity of an MC description by inputting binary data', description='Check the instruction validity of MC description by inputting binary data to a decoder', epilog=textwrap.dedent('''\
            Notes:

              This command detects following problems:

              * No instructions are defined for a certain binary data
              * Duplicate instructions are defined for a certain binary data

            Usage::

              # Check by inputting the range from 092d4800 to f92d4800 to a decoder
              mcdecoder check --input x92d4800 mc.yaml

              # Check by inputting the range from '1010 1001 0010 1101 0100 1000 0000 0000' to '1110 1001 0010 1101 0100 1000 0000 0000' to a decoder
              mcdecoder check --base 2 --input '1x10 1001 0010 1101 0100 1000 0000 0000' mc.yaml

              # Check by inputting the range from 002d4800 to ff2d4800 to a decoder
              mcdecoder check --input xx2d4800 mc.yaml
            '''))  # noqa: E501, W293
    emulate_parser.add_argument(
        '--input', '--pattern', metavar='indata', dest='bit_pattern', required=True, help=textwrap.dedent('''\
            A binary/hex string as input binary data for a decoder.
            'x' character acts as a wildcard which corresponds to a range 0-1 for binary or 0-f for hex.
            --pattern will be deprecated since 0.1b1'''))
    emulate_parser.add_argument(
        '--base', choices=[2, 16], default=16, type=int, help='The base of a binary/hex string (default: 16)')
    emulate_parser.add_argument(
        'mcfile', help='A path to a machine code description file')

    return parser


# endregion
