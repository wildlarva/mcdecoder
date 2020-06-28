import sys

from ..__main__ import main


def test_main(monkeypatch) -> None:
    monkeypatch.setattr(sys, 'argv', [sys.argv[0], '--version'])
    assert main() == 0
