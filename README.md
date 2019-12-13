# Machine Code Parser Generator(mcparser-gen)

## Installation

### For users

```bash
git clone https://github.com/wildlarva/mcparser-gen.git
cd <path-to-cloned-directory>
python3.8 -m pip install .
```

### For developers

```bash
git clone https://github.com/wildlarva/mcparser-gen.git
cd <path-to-cloned-directory>
python3.8 -m pip install -e .
```

After the installation, changes to the cloned directory are immediately reflected to the tool you installed.

## How to use

```bash
python3.8 -m mcparser_gen <path-to-mc-description-file>

ex. python3.8 -m mcparser_gen test/arm.yaml
```

MC parser files are generated as

* out/mcparser.c
* out/mcparser.h

## How to setup environment for development

```bash
# Clone mcparser-gen
git clone https://github.com/wildlarva/mcparser-gen.git
cd <path-to-cloned-directory>

# Install python tools and libraries
python3.8 -m venv env
source env/bin/activate
pip install pytest conan pyyaml jinja2
```

## How to run tests for mcparser-gen

```bash
# Switch to virtual environment
cd <path-to-cloned-directory>
source env/bin/activate

# Run tests
pytest
```

## How to run tests for generated parsers

```bash
# Switch to virtual environment
cd <path-to-cloned-directory>
source env/bin/activate

# Install mcparser-gen
pip install -e .

# Run tests
make test -C ctest
```
