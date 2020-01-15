# README: mcdecoder

mcdecoder (Machine Code Decoder) is a set of tools to implement a machine code decoder. It includes tools to:

- Generate a decoder for a user-defined machine code specification
- Emulate a decoder for a binary data and show decoded result
- Check the integrity of a machine code specification
- etc.

## Quickstart

1. Define your machine code specification

    ```yaml
    # arm.yaml
    machine:
      byteorder: little
    instructions:
      - name: add_immediate_a1
        format: xxxx:cond|00|1|0100|x:S|xxxx:Rn|xxxx:Rd|xxxx xxxx xxxx:imm12
    ```

2. Generate a decoder

    ```bash
    mcdecoder generate arm.yaml
    ```

3. Use the decoder from a client

    ```c
    OpDecodedCodeType decoded_code;
    OperationCodeType optype;
    int result;

    uint8 machine_codes[] = { 0x04, 0xB0, 0x8D, 0xE2, };
    result = op_parse((uint16 *) &machine_codes[0], &decoded_code, &optype);
    ```

For more details, follow Installation steps below and go on to [Quickstart tutorial](https://wildlarva.github.io/mcdecoder/quickstart.html).

## Who is mcdecoder for

- Developers of a CPU emulator
  - To implement the decoder part of an emulator
- Developers of a static analyzer for machine codes
  - To implement the decoder part of an analyzer
- Learners of the basics about machine codes
  - Hands-on approach to learn: write and test actual machine codes

Implementing and maintaining a decoder are tough and cumbersome. mcdecoder soothes these pains by generating a decoder.
mcdecoder was originally developed for [athrill](https://github.com/tmori/athrill/), a CPU emulator.
It will be independent from athrill and be a more general tool in the near future.

## Requirements

- Python 3.8 (with pip)

## Installation

```bash
git clone https://github.com/wildlarva/mcdecoder.git
cd mcdecoder
python3.8 -m pip install .
```

## More details about usage

See [documents for mcdecoder users](https://wildlarva.github.io/mcdecoder/).

## For developers of mcdecoder

See [documents for mcdecoder developers](https://wildlarva.github.io/mcdecoder/dev_docs.html).
