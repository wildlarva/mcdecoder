README: mcdecoder
=================

The mcdecoder (Machine Code Decoder) is a set of tools to implement a machine code decoder. It includes tools to:

* Generate a decoder for a user-defined machine code specification
* Emulate a decoder for a binary data and show decoded result
* Check the integrity of a machine code specification
* etc.

Currently, the mcdecoder only generates decoders in C language.

Quickstart
----------

#. Define your machine code specification

   .. code-block:: yaml
      :caption: arm.yaml

       machine:
         byteorder: little
       instructions:
         - name: add_immediate_a1
           format: xxxx:cond|00|1|0100|x:S|xxxx:Rn|xxxx:Rd|xxxx xxxx xxxx:imm12

#. Generate a decoder

   .. code-block:: bash

       mcdecoder generate arm.yaml

#. Use the decoder from a C client

   .. code-block:: c

       const uint8_t kMachineCodes[] = { 0x04, 0xB0, 0x8D, 0xE2, };
       DecodeRequest request;
       DecodeResult result;
       bool succeeded;

       request.codes = &kMachineCodes[0];
       succeeded = DecodeInstruction(&request, &result);

For more details, follow Installation steps below and go on to :doc:`quickstart`.

Who is mcdecoder for
--------------------

* Developers of a CPU emulator

  * To implement the decoder part of an emulator

* Developers of a static analyzer for machine codes

  * To implement the decoder part of an analyzer

* Learners of the basics about machine codes

  * Hands-on approach to learn: write and test actual machine codes

Implementing and maintaining a decoder are tough and cumbersome. The mcdecoder soothes these pains by generating a decoder.
The mcdecoder was originally developed for `athrill <https://github.com/toppers/athrill>`__, a CPU emulator. It is now independent from athrill.

Requirements
------------

* Python 3.10 (with pip)

Installation
------------

.. code-block:: bash

    python3.10 -m pip install mcdecoder

License
-------

The mcdecoder uses MIT License. See `LICENSE <https://github.com/wildlarva/mcdecoder/blob/master/LICENSE>`__ for more details.

More details about usage
------------------------

See :doc:`documents for mcdecoder users <guides>`.

For developers of mcdecoder
---------------------------

See :doc:`documents for mcdecoder developers <dev_docs>`.
