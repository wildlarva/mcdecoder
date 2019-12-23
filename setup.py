import sys

from setuptools import find_packages, setup

if sys.version_info < (3,8):
    sys.exit('Sorry, Python < 3.8 is not supported.')

setup(
    name='mcdecoder',
    version='0.1a2.dev1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=['pyyaml', 'jinja2'],
)
