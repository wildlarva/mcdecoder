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
    install_requires=['deprecation>=2.0', 'Jinja2>=2.11.2', 'jsonschema>=3.0.2',
                      'lark-parser>=0.6.6', 'numpy>=1.17.3', 'PyYAML>=5.2'],
)
