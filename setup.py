import sys

from setuptools import find_packages, setup

if sys.version_info < (3,8):
    sys.exit('Sorry, Python < 3.8 is not supported.')

setup(
    name='mcdecoder',
    version='0.1a1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'mcdecoder': ['py.typed'],
    },
    python_requires='>=3.8',
    install_requires=['pyyaml', 'jinja2'],
)
