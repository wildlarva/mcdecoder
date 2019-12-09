# Machine Code Parser Generator(mcparser-gen)
## Installation
```
git clone https://github.com/wildlarva/mcparser-gen.git
cd <path-to-cloned-dir>
python3 -m pip install -e .
```

## How to use
```
python3 -m mcparser <path-to-mc-description-file>

ex. python3 -m mcparser test/arm.yaml
```
MC parser files are generated as
* out/mcparser.c
* out/mcparser.h
