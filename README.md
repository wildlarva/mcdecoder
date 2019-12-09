# Machine Code Parser Generator(mcparser-gen)
## Installation
### For users
```
git clone https://github.com/wildlarva/mcparser-gen.git
cd <path-to-cloned-directory>
python3 -m pip install .
```

### For developers
```
git clone https://github.com/wildlarva/mcparser-gen.git
cd <path-to-cloned-directory>
python3 -m pip install -e .
```
After the installation, changes to the cloned directory are immediately reflected to the tool you installed.

## How to use
```
python3 -m mcparser <path-to-mc-description-file>

ex. python3 -m mcparser test/arm.yaml
```
MC parser files are generated as
* out/mcparser.c
* out/mcparser.h
