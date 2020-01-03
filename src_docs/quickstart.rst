############################
Quickstart tutorial
############################

You can generate a machine code decoder with mcdecoder
by defining specifications of machine code.
In this tutorial, you'll see how to define machine code specifications
and generate a decoder from the specification.

The guide steps of the tutorial are:

1. Introduce an example instruction encoding to be decoded
2. Write an MC description to express the encoding
3. Check if the MC description is working
4. Generate a decoder from the MC description
5. Run the decoder from C client code

*********************************************************************
1. Introduce an example instruction encoding to be decoded
*********************************************************************

In this tutorial, We use the ARM instructions below as an example.

- ADD (immediate, ARM) Encoding A1
- PUSH Encoding A1

We ignore instruction matching conditions using field values
(e.g. Rn == 0b1111 and S == 0) here for simplicity.

.. rst-class:: instruction-encoding


.. table:: The instruction encoding of ADD (immediate, ARM) Encoding A1
   :widths: 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1

   == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
   MSB                                                                                       LSB
   ----- ----------------------------------------------------------------------------------- -----
   31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
   -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   cond        0  0  1  0  1  0  0  S  Rn          Rn          imm12
   =========== ===== == =========== == =========== =========== ===================================

.. rst-class:: instruction-encoding


.. table:: The instruction encoding of PUSH Encoding A1
   :widths: 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1

   == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
   MSB                                                                                       LSB
   ----- ----------------------------------------------------------------------------------- -----
   31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
   -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   cond        1  0  0  1  0  0  1  0  1  1  0  1  register_list
   =========== ================= == == =========== ===============================================

*********************************************************************
2. Write an MC description to express the encoding
*********************************************************************

Write machine code specifications as a file.
In mcdecoder, we call it a machine code description file or
an MC description file.
It's defined as a YAML format.

You must add a sequence element of :code:`instructions`
for each instruction.
Name each instruction and define an instruction encoding in :code:`format`
according to the encoding introduced before.
See :doc:`spec_mc_desc` to understand the grammar of MC description.

Make :code:`arm.yaml` with the following content.

.. literalinclude:: ../examples/quickstart/arm.yaml
   :language: yaml
   :caption: arm.yaml

*********************************************************************
3. Check if the MC description is working
*********************************************************************

Now you have a minimum MC description.
Let's check if it is working.
For this, you can use :code:`mcdecoder emulate` command
to emulate a decoder behavior.

Input the machine code :code:`e28db004` for example.
It means :code:`add FP, SP, #4` in ARM assembly language
and the fields in its encoding format should be:

* Rn = 13 (which is R13 or SP)
* Rd = 11 (which is R11 or FP)
* imm12 = 4

Run the command:

.. code-block:: bash

    mcdecoder emulate arm.yaml --pattern e28db004

Its output will be...

.. code-block:: bash

    instruction: add_immediate_a1

    cond: 14, 0xe, 0b1110
    S: 0, 0x0, 0b0
    Rn: 13, 0xd, 0b1101
    Rd: 11, 0xb, 0b1011
    imm12: 4, 0x4, 0b100

Fine. It looks working.

See :doc:`spec_commandline_options` for more information
about :code:`emulate` sub-command if you'd like.

*********************************************************************
4. Generate a decoder from the MC description
*********************************************************************

Run :code:`mcdecoder generate` command to generate a decoder
from the MC description.

.. code-block:: bash

    mcdecoder generate --output out arm.yaml

You'll get generated files below:

.. code-block:: bash

    out
    ├── mcdecoder.c
    └── mcdecoder.h

See :doc:`spec_commandline_options` for more details
about :code:`generate` sub-command if you'd like.

*********************************************************************
5. Run the decoder from C client code
*********************************************************************

Create a C client code to test the function of the generated decoder.
Use a decoder API :code:`op_parse` in the client and define the stubs of
instruction execution callback :code:`op_exec_<instruction>`.

.. code-block:: c

    /* Decoder API */
    int op_parse(uint16 code[OP_DECODE_MAX], OpDecodedCodeType *decoded_code, OperationCodeType *optype);

    /* Instruction execution callback */
    int op_exec_add_immediate_a1(struct TargetCore *core);

In the client code, input the machine code :code:`e28db004`
as you did with :code:`mcdecoder emulate` and check if the result is the same.

Make the following C client code.

.. literalinclude:: ../examples/quickstart/client.c
   :language: c
   :caption: client.c

Now compile and execute the client code to get the decoding result.

.. code-block:: bash

    gcc client.c out/mcdecoder.c
    ./a.out

The result will be:

.. code-block:: bash

    Decode succeeded.
    Instruction: add_immediate_a1
    Rn = 13, Rd = 11, imm12 = 4

Good! It coincides with the result of :code:`mcdecoder emulate` and
the tutorial is over.

You can see :download:`example files in the tutorial in github <https://github.com/wildlarva/mcdecoder/blob/master/examples/quickstart>`.

*********************************************************************
What's next?
*********************************************************************

* :doc:`More details about MC description <spec_mc_desc>`
* :doc:`More details about mcdecoder emulate and generate
  <spec_commandline_options>`
* :doc:`Other useful mcdecoder commands <spec_commandline_options>`

  * :code:`mcdecoder check`: Check the integrity of your MC description

    * You can check your MC description if

      * there are no instructions for a certain bit pattern or
      * there are multiple instructions for a certain bit pattern.

  * :code:`mcdecoder export`: Export the MC description as CSV format

    * You can see all instructions at a glance in CSV view and
      filter instructions with spreadsheet apps
      like Google Spreadsheet or Excel.

* :doc:`User templates: Create your own template <user_templates>`

  * if you need your custom decoder or you need additional codes
    to support your decoder, you can create your own templates.
