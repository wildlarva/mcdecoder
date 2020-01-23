import sys

from setuptools import find_packages, setup

from src.mcdecoder import __version__

if sys.version_info < (3, 8):
    sys.exit('Sorry, Python < 3.8 is not supported.')

setup(
    name='mcdecoder',
    version=__version__.__version__,
    packages=find_packages(
        'src', exclude=['test', 'test.*', '*.test', '*.test.*']),
    package_dir={'': 'src'},
    package_data={'': ['*.json', '*.lark'], 'mcdecoder': ['templates/*/*']},
    entry_points={
        'console_scripts': ['mcdecoder = mcdecoder.__main__:main']
    },
    python_requires='>=3.8',
    install_requires=['Jinja2', 'jsonschema',
                      'lark-parser', 'numpy', 'PyYAML'],
)
