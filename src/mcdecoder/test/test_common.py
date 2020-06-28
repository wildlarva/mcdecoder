import os
import pathlib

from ..common import make_parent_directories


def test_make_parent_directories_not_exist() -> None:
    _remove_temp_file('somedir')
    assert make_parent_directories('somedir/some.txt') is True
    assert os.path.isdir('somedir') is True


def test_make_parent_directories_exist() -> None:
    _remove_temp_file('somedir')
    os.makedirs('somedir', exist_ok=True)
    assert make_parent_directories('somedir/some.txt') is True


def test_make_parent_directories_not_dir() -> None:
    _remove_temp_file('somedir')
    pathlib.Path('somedir').touch()
    assert make_parent_directories('somedir/some.txt') is False


def test_make_parent_directories_without_parent_dir() -> None:
    assert make_parent_directories('some.txt') is True


def _remove_temp_file(file: str):
    if os.path.isfile(file):
        os.remove(file)
    elif os.path.isdir(file):
        os.removedirs(file)
