import os
import shutil

from mcdecoder.app import run_app


def test_run_app_without_arguments() -> None:
    assert run_app(['mcdecoder']) == 2
    assert run_app(['mcdecoder', 'generate']) == 2


def test_run_app_help() -> None:
    assert run_app(['mcdecoder', '--help']) == 0
    assert run_app(['mcdecoder', '-h']) == 0
    assert run_app(['mcdecoder', 'generate', '--help']) == 0
    assert run_app(['mcdecoder', 'generate', '-h']) == 0


def test_run_app_generate() -> None:
    shutil.rmtree('out')

    assert run_app(['mcdecoder', 'generate', 'test/arm.yaml']) == 0
    assert os.path.isfile('out/arm_mcdecoder.c') == True
    assert os.path.isfile('out/arm_mcdecoder.h') == True


def test_run_app_export() -> None:
    shutil.rmtree('out')

    assert run_app(['mcdecoder', 'export', '--output',
                    'out/arm.csv', 'test/arm.yaml']) == 0
    assert os.path.isfile('out/arm.csv') == True
