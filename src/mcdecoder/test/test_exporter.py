from mcdecoder.exporter import export
import csv


def test_export_without_condition() -> None:
    export('test/riscv.yaml', 'out/riscv.csv')

    with open('out/riscv.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    assert len(rows) == 3

    header_row, add_row, push_row = rows
    assert header_row == ['name'] + [f'b{bit}' for bit in range(15, -1, -1)] + ['condition']
    assert add_row == ['c_addi_1'] + list('000xxxxxxxxxxx01') + ['']
    assert push_row == ['c_sd_1'] + list('111xxxxxxxxxxx10') + ['']


def test_export_with_condition() -> None:
    export('test/arm.yaml', 'out/arm.csv')

    with open('out/arm.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    assert len(rows) == 3

    header_row, add_row, push_row = rows
    assert header_row == ['name'] + [f'b{bit}' for bit in range(31, -1, -1)] + ['condition']
    assert add_row == ['add_1'] + \
        list('xxxx0010100xxxxxxxxxxxxxxxxxxxxx') + ['cond != 15']
    assert push_row == [
        'push_1'] + list('xxxx100100101101xxxxxxxxxxxxxxxx') + ['cond in_range 0-14']
