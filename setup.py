import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 8):
    sys.exit('Sorry, Python < 3.8 is not supported.')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mcdecoder',
    version='0.1.1',
    packages=find_packages(
        'src', exclude=['test', 'test.*', '*.test', '*.test.*']),
    package_dir={'': 'src'},
    package_data={'': ['*.json', '*.lark'], 'mcdecoder': ['templates/*/*']},
    entry_points={
        'console_scripts': ['mcdecoder = mcdecoder.__main__:main']
    },
    python_requires='>=3.8',
    install_requires=['deprecation>=2.0.7', 'Jinja2>=3.1.3', 'jsonschema>=3.2.0',
                      'lark-parser>=0.9.0', 'numpy>=1.24.0', 'PyYAML>=6.0'],

    # Metadata to display on PyPI
    author='wildlarva',
    description='The generator of a machine code decoder, ' + \
    'transforming a user-defined machine code specification into decoder codes.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wildlarva/mcdecoder',
    project_urls={
        "Documentation": "https://wildlarva.github.io/mcdecoder/",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",  # Runtime language
        "Operating System :: OS Independent",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Programming Language :: C",  # Supported language for generator
        "Development Status :: 4 - Beta",
    ],
)
