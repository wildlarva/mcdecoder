import os
import shutil

from mcdecoder.app import run_app


def test_run_app_without_arguments() -> None:
    assert run_app(['mcdecoder']) == 2
    assert run_app(['mcdecoder', 'generate']) == 2
    assert run_app(['mcdecoder', 'export']) == 2
    assert run_app(['mcdecoder', 'export', 'test/arm.yaml']) == 2
    assert run_app(['mcdecoder', 'export', '--output', 'out/arm.yaml']) == 2


def test_run_app_help() -> None:
    assert run_app(['mcdecoder', '--help']) == 0
    assert run_app(['mcdecoder', '-h']) == 0
    assert run_app(['mcdecoder', 'generate', '--help']) == 0
    assert run_app(['mcdecoder', 'generate', '-h']) == 0


def test_run_app_generate_without_template_dir() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert run_app(['mcdecoder', 'generate', '--output',
                    'out', 'test/arm.yaml']) == 0
    assert os.path.isfile('out/arm_mcdecoder.c') is True
    assert os.path.isfile('out/arm_mcdecoder.h') is True


def test_run_app_generate_with_template_dir() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert run_app(['mcdecoder', 'generate', '--output', 'out',
                    '--template', 'test/user_templates', 'test/arm.yaml']) == 0
    assert os.path.isfile('out/arm_template.c') is True
    assert os.path.isfile('out/arm_template.h') is True


def test_run_app_generate_with_output_dir() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert run_app(['mcdecoder', 'generate', '--output',
                    'out/out2', 'test/arm.yaml']) == 0
    assert os.path.isfile('out/out2/arm_mcdecoder.c') is True
    assert os.path.isfile('out/out2/arm_mcdecoder.h') is True


def test_run_app_export() -> None:
    shutil.rmtree('out', ignore_errors=True)

    assert run_app(['mcdecoder', 'export', '--output',
                    'out/arm.csv', 'test/arm.yaml']) == 0
    assert os.path.isfile('out/arm.csv') is True
