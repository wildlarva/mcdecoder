import csv
from dataclasses import dataclass
import os
from typing import List

from mcdecoder import core

# External functions


def export(mcfile: str, output_file: str) -> int:
    result = _export(mcfile, output_file)
    if result:
        print('Exported a machine code description.')
        return 0
    else:
        print('Error occurred on exporting.')
        return 1


# Internal classes

@dataclass
class _InstructionInfo:
    instruction: core.InstructionDescrition
    format: core.InstructionFormat


# Internal functions

def _export(mcfile: str, output_file: str) -> bool:
    # Load MC description
    mc_desc = core.load_mc_description_model(mcfile)

    # Parse instruction formats
    instruction_infos = [_InstructionInfo(instruction=instruction, format=core.parse_instruction_format(
        instruction['format'])) for instruction in mc_desc['instructions']]
    max_instruction_bit_size = max(map(
        lambda info: core.calc_instruction_bit_size(info.format), instruction_infos))

    # Make columns
    bit_columns = [f'b{bit}' for bit in range(max_instruction_bit_size - 1, -1, -1)]
    columns = ['name'] + bit_columns + ['condition']

    # Make rows
    rows: List[List[str]] = []
    for info in instruction_infos:
        instruction_bit_size = core.calc_instruction_bit_size(info.format)

        # Concatenate all bits to one string
        unrelated_bits = '-' * \
            (max_instruction_bit_size - instruction_bit_size)
        related_bits = ''.join(
            map(lambda field_format: field_format.bits_format, info.format.field_formats))
        bits = unrelated_bits + related_bits

        # Make condition string
        condition = '\n'.join(map(lambda pair: f'{pair[0]} {pair[1]}', info.instruction['condition'].items(
        ))) if 'condition' in info.instruction else ''

        # Append row
        row = [info.instruction['name']] + list(bits) + [condition]
        rows.append(row)

    # Make parent directory of output file
    output_dir = os.path.dirname(output_file)
    if output_dir != '':
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        elif not os.path.isdir(output_dir):
            return False

    # Export CSV
    with open(output_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    return True