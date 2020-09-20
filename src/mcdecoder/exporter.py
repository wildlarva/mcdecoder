import csv
from dataclasses import dataclass
import itertools
from typing import List, cast

from . import common, core

# region External functions


def export(mcfile: str, output_file: str) -> int:
    """
    Implementation of the sub-command 'export'.

    Export an MC description as another format.

    NOTE Currently, mcdecoder supports only CSV format.

    :param mcfile: Path to an MC description file
    :param output_file: Path to an file to be exported
    :return: Exit code of mcdecoder
    """
    result = _export(mcfile, output_file)
    if result:
        print('Exported a machine code description.')
        return 0
    else:
        print('Error occurred on exporting.')
        return 1


# endregion

# region Internal classes

@dataclass
class _InstructionInfo:
    instruction: core.InstructionDescription
    encoding: core.InstructionEncodingDescription


# endregion

# region Internal functions

def _export(mcfile: str, output_file: str) -> bool:
    # Load MC description
    mc_desc = core.load_mc_description(mcfile)

    # Parse instruction formats
    instruction_infos = [_InstructionInfo(instruction=instruction, encoding=core.parse_instruction_encoding(
        instruction['format'])) for instruction in mc_desc['instructions']]
    max_instruction_bit_size = max(core.calc_instruction_bit_size(
        info.encoding) for info in instruction_infos)

    # Make columns
    bit_columns = [f'b{bit}' for bit in range(
        max_instruction_bit_size - 1, -1, -1)]
    columns = ['name'] + bit_columns + ['condition']

    # Make rows
    rows: List[List[str]] = []
    for info in instruction_infos:
        field_encodings = itertools.chain.from_iterable(
            element.fields for element in info.encoding.elements)
        instruction_bit_size = core.calc_instruction_bit_size(info.encoding)

        # Concatenate all bits to one string
        unrelated_bits = '-' * \
            (max_instruction_bit_size - instruction_bit_size)
        related_bits = ''.join(
            field.bits_format for field in field_encodings)
        bits = unrelated_bits + related_bits

        # Make condition string
        condition = ''
        if 'match_condition' in info.instruction:
            condition = cast(str, info.instruction['match_condition'])
        elif 'unmatch_condition' in info.instruction:
            condition = f"not ({info.instruction['unmatch_condition']})"

        # Append row
        row = [info.instruction['name']] + list(bits) + [condition]
        rows.append(row)

    # Make parent directory of output file
    if not common.make_parent_directories(output_file):
        return False

    # Export CSV
    with open(output_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    return True


# endregion
