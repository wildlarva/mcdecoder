import csv
import os
import pathlib
import shutil

from mcdecoder.exporter import export


def test_export_without_condition() -> None:
    _remove_temp_file('out')

    assert export('tests/common/riscv.yaml', 'out/riscv.csv') == 0

    with open('out/riscv.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    assert len(rows) == 3

    header_row, add_row, push_row = rows
    assert header_row == ['name'] + \
        [f'b{bit}' for bit in range(15, -1, -1)] + ['condition']
    assert add_row == ['c_addi_1'] + list('000xxxxxxxxxxx01') + ['']
    assert push_row == ['c_sd_1'] + list('111xxxxxxxxxxx10') + ['']


def test_export_with_condition() -> None:
    _remove_temp_file('out')

    assert export('tests/common/arm.yaml', 'out/arm.csv') == 0

    with open('out/arm.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    assert len(rows) == 3

    header_row, add_row, push_row = rows
    assert header_row == ['name'] + \
        [f'b{bit}' for bit in range(31, -1, -1)] + ['condition']
    assert add_row == ['add_1'] + \
        list('xxxx0010100xxxxxxxxxxxxxxxxxxxxx') + ['not (cond == 15)']
    assert push_row == [
        'push_1'] + list('xxxx100100101101xxxxxxxxxxxxxxxx') + ['cond in_range 0-14']


def test_export_parent_dir_is_file() -> None:
    _remove_temp_file('out')
    pathlib.Path('out').touch()

    assert export('tests/common/arm.yaml', 'out/arm.csv') == 1


def _remove_temp_file(file: str):
    if os.path.isfile(file):
        os.remove(file)
    elif os.path.isdir(file):
        shutil.rmtree(file, ignore_errors=True)
