import os
import shutil

from mcdecoder.app import run_app


def test_run_app_without_arguments() -> None:
    assert run_app(['mcdecoder']) == 2
    assert run_app(['mcdecoder', 'generate']) == 2
    assert run_app(['mcdecoder', 'export']) == 2
    assert run_app(['mcdecoder', 'export', 'tests/common/arm.yaml']) == 2
    assert run_app(['mcdecoder', 'export', '--output', 'out/arm.yaml']) == 2
    assert run_app(['mcdecoder', 'emulate']) == 2
    assert run_app(['mcdecoder', 'emulate', 'tests/common/arm.yaml']) == 2


def test_run_app_help() -> None:
    assert run_app(['mcdecoder', '--help']) == 0
    assert run_app(['mcdecoder', '-h']) == 0
    assert run_app(['mcdecoder', 'generate', '--help']) == 0
    assert run_app(['mcdecoder', 'generate', '-h']) == 0


def test_run_app_version() -> None:
    assert run_app(['mcdecoder', '--version']) == 0


def test_run_app_generate_without_arguments() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert run_app(['mcdecoder', 'generate', '--output',
                    'out', 'tests/common/arm.yaml']) == 0
    assert os.path.isfile('out/arm_mcdecoder.c') is True
    assert os.path.isfile('out/arm_mcdecoder.h') is True


def test_run_app_generate_with_type() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert run_app(['mcdecoder', 'generate', '--type', 'athrill', '--output',
                    'out', 'tests/common/arm.yaml']) == 0
    assert os.path.isfile('out/arm_mcdecoder.c') is True
    assert os.path.isfile('out/arm_mcdecoder.h') is True


def test_run_app_generate_with_template_dir() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert run_app(['mcdecoder', 'generate', '--output', 'out',
                    '--template', 'tests/common/user_templates', 'tests/common/arm.yaml']) == 0
    assert os.path.isfile('out/arm_template.c') is True
    assert os.path.isfile('out/arm_template.h') is True


def test_run_app_generate_conflict_type_and_template_dir() -> None:
    assert run_app(['mcdecoder', 'generate', '--type', 'athrill', '--template',
                    'tests/common/user_templates', '--output', 'out', 'tests/common/arm.yaml']) == 2


def test_run_app_generate_with_output_dir() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert run_app(['mcdecoder', 'generate', '--output',
                    'out/out2', 'tests/common/arm.yaml']) == 0
    assert os.path.isfile('out/out2/arm_mcdecoder.c') is True
    assert os.path.isfile('out/out2/arm_mcdecoder.h') is True


def test_run_app_export() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert run_app(['mcdecoder', 'export', '--output',
                    'out/arm.csv', 'tests/common/arm.yaml']) == 0
    assert os.path.isfile('out/arm.csv') is True


def test_run_app_emulate() -> None:
    assert run_app(['mcdecoder', 'emulate', '--input',
                    'e9 2d 48 00', 'tests/common/arm.yaml']) == 0
    assert run_app(['mcdecoder', 'emulate', '--input',
                    '1110 1001 0010 1101 0100 1000 0000 0000', '--base', '2', 'tests/common/arm.yaml']) == 0
    assert run_app(['mcdecoder', 'emulate', '--input',
                    'e9 2d 48 00', '--base', '16', 'tests/common/arm.yaml']) == 0
    assert run_app(['mcdecoder', 'emulate', '--input',
                    'e9 2d 48 00', '--byteorder', 'big', 'tests/common/arm.yaml']) == 0
    assert run_app(['mcdecoder', 'emulate', '--input',
                    '00 48 2d e9', '--byteorder', 'little', 'tests/common/arm.yaml']) == 0


def test_run_app_check() -> None:
    assert run_app(['mcdecoder', 'check', '--input',
                    'ex xd 48 00', 'tests/common/arm.yaml']) == 0
    assert run_app(['mcdecoder', 'check', '--input',
                    '111x x001 0010 1101 0100 1000 0000 000x', '--base', '2', 'tests/common/arm.yaml']) == 0
    assert run_app(['mcdecoder', 'check', '--input',
                    'ex xd 48 00', '--base', '16', 'tests/common/arm.yaml']) == 0
