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
    assert run_app(['mcdecoder', 'generate', 'test/arm.yaml']) == 0
