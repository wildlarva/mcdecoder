# Machine Code Decoder Generator(mcdecoder)

## For users

### Requirements

- Python 3.8 (with pip)

### Installation

```bash
git clone https://github.com/wildlarva/mcdecoder.git
cd <path-to-cloned-directory>
python3.8 -m pip install .
```

### How to use

```bash
python3.8 -m mcdecoder <path-to-mc-description-file>

ex. python3.8 -m mcdecoder test/arm.yaml
```

MC decoder files are generated as

* out/mcdecoder.c
* out/mcdecoder.h

See [the specification of machine code description file](doc/mc_desc_spec.yaml).

## For developers

### Requirements

- Python 3.8 (with pip and venv)

### How to setup environment for development

```bash
# Clone mcdecoder
git clone https://github.com/wildlarva/mcdecoder.git

# Create virtual environment and switch to it
cd <path-to-cloned-directory>
python3.8 -m venv env
source env/bin/activate

# Install python tools and libraries
pip install pytest conan pyyaml jinja2

# Install mcdecoder
pip install -e .
```

After the installation, changes to the cloned directory are immediately reflected to mcdecoder you installed.

### How to run tests for mcdecoder

```bash
# Switch to virtual environment
cd <path-to-cloned-directory>
source env/bin/activate

# Run tests
pytest
```

### How to run tests for generated decoders

```bash
# Switch to virtual environment
cd <path-to-cloned-directory>
source env/bin/activate

# Run tests
make -C ctest clean test
```
