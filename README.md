# Machine Code Decoder Generator(mcdecoder)

## For users

### Requirements

- Python 3.8 (with pip)

### Installation

```bash
git clone https://github.com/wildlarva/mcdecoder.git
cd mcdecoder
python3.8 -m pip install .
```

### How to use

```bash
mcdecoder generate --output <output-directory> <path-to-mc-description-file>
# or
python3.8 -m mcdecoder generate --output <output-directory> <path-to-mc-description-file>

# ex. mcdecoder generate --output out test/arm.yaml
```

MC decoder files are generated as:

- `<output-directory>/`
  - `mcdecoder.c`
  - `mcdecoder.h`

### More details about usage

See [documentation](https://wildlarva.github.io/mcdecoder/).

## For developers

### Requirements for development

- Python 3.8 (with pip and venv)

### How to setup environment for development

```bash
# Clone mcdecoder
git clone https://github.com/wildlarva/mcdecoder.git

# Create virtual environment and switch to it
cd mcdecoder
python3.8 -m venv env
source env/bin/activate

# Install python tools and libraries
pip install -r requirements.txt

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

### More details about development

See [documentation](https://wildlarva.github.io/mcdecoder/).
