############################
MC description specification
############################

.. highlight:: yaml

**********************************************
Overview
**********************************************

Machine code description file or MC description file is defined
as a YAML format.
Here is an overview of MC description.

.. literalinclude:: spec_mc_desc.yaml

**********************************************
machine: Describes a machine
**********************************************

:code:`machine` describes the specification of a machine.

========================================================================================================
machine.byteorder: Byte order of a machine
========================================================================================================

:code:`byteorder` is the byte order of a machine.
It can be :code:`big` (big endian) or :code:`little` (little endian).

========================================================================================================
machine.extras: User-defined data for a machine
========================================================================================================

:code:`extras` defines user-defined data for a machine.
Any structure can be defined as user-defined data.

Here is an example of defining a mapping as user-defined data.

.. code-block:: yaml

    extras:
      arch_type: arm

Here is an example of defining a sequence as user-defined data.

.. code-block:: yaml

    extras:
      - 10
      - 20

**********************************************
instructions: Describes instructions
**********************************************

:code:`instructions` describes the specification of instructions.
Each list element in :code:`instructions` represents an instruction.

========================================================================================================
instructions.name: Name of an instruction
========================================================================================================

:code:`name` defines the name of an instruction.

========================================================================================================
instructions.format: Encoding format of an instruction
========================================================================================================

:code:`format` defines the encoding format of an instruction.
Instruction can be split into multiple parts
which are named instruction fields.
One field can be split into several bit ranges.
Each bit range is called a subfield in a field.

Here is an example of instruction fields
(the fields 'cond', 'S', 'Rn', 'Rd' and 'imm12').

.. code-block:: yaml

    format: xxxx:cond|00|1|0100|x:S|xxxx:Rn|xxxx:Rd|xxxx xxxx xxxx:imm12

Here is an example of instruction subfields
(the field 'imm' is split into several bit positions).

.. code-block:: yaml

    format: 000:funct3|x:imm[5]|xxxx x:dest|xxx xx:imm[4:0]|01:op

Expression: :code:`<field_bits>:<field_name>[<field_bit_ranges>]|... // ...`

Fields are separated by bar symbol(:code:`|`).
If an instruction is constructed by multiple N-byte words,
they're split by double-slash symbol(:code:`//`).

where

<field_bits>
    Encoding format of an instruction field

    It takes an array of :code:`0`, :code:`1` or :code:`x`.
    :code:`0` or :code:`1` represents a fixed bit of an instruction field.
    :code:`x` represents any bit.

<field_name>
    [optional] Name of an instruction field

    One field name can be used multiple times in one instruction.

<field_bit_ranges>
    [optional] Field bit ranges of an instruction field

    Expression: :code:`<subfield_start>:<subfield_end>,...`

    Bit ranges are separated by comma symbol(:code:`,`).

<subfield_start>
    MSB of a subfield in an instruction field

    NOTE: This is a MSB in a field, not in an instruction.

<subfield_end>
    [optional] LSB of a subfield in an instruction field

    NOTE: This is an LSB in a field, not in an instruction.

========================================================================================================
instructions.match_condition: Condition an instruction applys
========================================================================================================

:code:`match_condition` defines the bit condition when an instruction applys.
The following condition types are supported.

* Equality: The equality between a field value and a given value.
* In a set: A field value is in a given value set.
* In a range: A field value is in a given value range(inclusive).

These conditions can be combined with a logical operator :code:`and` or
:code:`or`.
You can also use :code:`(` and :code:`)` for readability.

Equality condition
-----------------------

It defines a condition to test the equality between a field value and
a given value.

When the field 'cond' equals 15,

.. code-block:: yaml

    match_condition: cond == 15

When the field 'Rn' equals the field 'Rd',

.. code-block:: yaml

    match_condition: Rn == Rd

When the 15th bit of the field 'register_list' equals 1,

.. code-block:: yaml

    match_condition: register_list[15] == 1

When the set bit count of the field 'register_list' is less than 2,

.. code-block:: yaml

    match_condition: setbit_count(register_list) < 2

Expression: :code:`<subject> <operator> <object>`

where

<operator>
    Equality operator to test

    It can be :code:`==`, :code:`!=`, :code:`<`, :code:`<=`, :code:`>` or
    :code:`>=`.

See also the common expressions below.

In-a-set condition
----------------------

It defines a condition to test that a field value is in a given value set.

When the field 'cond' is in a set [13, 15],

.. code-block:: yaml

    match_condition: cond in [13, 15]

Expression: :code:`<subject> in <values>`

where

<values>
    Value set to test with

    Expression: :code:`[<value>,...]`

    It takes multiple values with the separator :code:`,`
    (comma symbol).

See also the common expressions below.

In-a-range condition
-------------------------

It defines a condition to test that a field value is
in a given value range(inclusive).

When the field 'cond' is in a range 10 to 15,

.. code-block:: yaml

    match_condition: cond in_range 10-15

Expression: :code:`<subject> in_range <value_start>-<value_end>`

where

<value_start>
    Start of a value range(inclusive)

    Base 2, 10 or 16 integer values like :code:`15`, :code:`0b1111`,
    :code:`0xf`, etc.

<value_end>
    End of a value range(inclusive)

    Base 2, 10 or 16 integer values like :code:`15`, :code:`0b1111`,
    :code:`0xf`, etc.

See also the common expressions below.

Common expressions
--------------------------------------

<subject>
    Subject to be tested

    Expression: :code:`<field_object>` or :code:`<function_object>`

<object>
    Object to test with

    Expression: :code:`<value>` or :code:`<field_object>` or
    :code:`<function_object>`

<function_object>
    The result of a function call to be tested

    Expression: :code:`<function>(<field_object>)`

<function>
    Function name that its result is to be tested

    Supported functions are:

    * :code:`setbit_count`: Count the set bit count of a given argument.

<field_object>
    Field object to be tested

    Expression: :code:`<field>[<field_element_index>]`

<field>
    Field name to be tested

<field_element_index>
    [optional] Bit element index of a field

    Base 10 integer value like :code:`1`, :code:`2`, etc.

<value>
    Value to test the equality with

    Base 2, 10 or 16 integer values like :code:`15`, :code:`0b1111`,
    :code:`0xf`, etc.

===================================================================================
instructions.unmatch_condition: Condition an instruction doesn't apply
===================================================================================

:code:`unmatch_condition` defines the condition
when an instruction does not apply.
The expression is the same as that of :code:`match_condition`.
:code:`unmatch_condition` is mutually exclusive with :code:`match_condition`.

========================================================================================================
instructions.extras: User-defined data for an instruction
========================================================================================================

:code:`extras` defines user-defined data for an instruction.
Any structure can be defined as user-defined data.

Here is an example of defining a mapping as user-defined data.

.. code-block:: yaml

    extras:
      clocks: 10

Here is an example of defining a sequence as user-defined data.

.. code-block:: yaml

    extras:
      - 10
      - 20

================================================================================
instructions.field_extras: User-defined data for each field
================================================================================

:code:`field_extras` defines user-defined data for each field.
Each mapping key in :code:`field_extras` represents a field
defining user-defined data and its value holds user-defined data for the field.
Any structure can be defined as user-defined data.

Here is an example of defining a mapping as user-defined data.

.. code-block:: yaml

    field_extras:
      Rn: {type: register} # User-defined data for the field 'Rn'
      imm12: {type: immediate} # User-defined data for the field 'imm12'

Here is an example of defining a sequence as user-defined data.

.. code-block:: yaml

    field_extras:
      Rn: [10, 20] # User-defined data for the field 'Rn'
      imm12: [30, 40] # User-defined data for the field 'imm12'

********************************************************************************************
decoder: Decoder information of the global scope
********************************************************************************************

:code:`decoder` is a decoder information that isn't related to a machine,
an instruction and a field.

========================================================================================================
decoder.namespace: Namespace for the symbols of a generated decoder
========================================================================================================

:code:`namespace` defines the namespace for the symbols of a generated decoder.

******************************************************************************************************
extras: User-defined data of the global scope
******************************************************************************************************

:code:`extras` defines user-defined data that isn't related to a machine,
an instruction and a field.
Any structure can be defined as user-defined data.

Here is an example of defining a mapping as user-defined data.

.. code-block:: yaml

    extras:
      compiler: gcc
      version: 1.0

Here is an example of defining a sequence as user-defined data.

.. code-block:: yaml

    extras:
      - 10
      - 20

*************************
Additional specifications
*************************

=========================================================
!include: Split a description into multiple files
=========================================================

You can split a description into multiple files by using :code:`!include` tag.
You can use it anywhere in a description and
the contents of specified files will be inserted into the place
where the tag is.
If multiple files are specified, the contents will be combined.
The behavior depends on the types of the contents of included files:

* Sequence: Produce one sequence consisting of the elements of all sequences.
* Mapping: Produce one mapping consisting of the elements of all mappings.
* Scalar: Produce one sequence consisting of scalars.
* Mixture: Prompt an error.

Here's an example of including instructions from other files.

.. literalinclude:: ../examples/include/arm.yaml
    :caption: arm.yaml

.. literalinclude:: ../examples/include/instructions/add_instructions.yaml
    :caption: instructions/add_instructions.yaml

.. literalinclude:: ../examples/include/instructions/push_instructions.yaml
    :caption: instructions/push_instructions.yaml

You can see this :download:`example in github <https://github.com/wildlarva/mcdecoder/blob/master/examples/include>`.

Expression: :code:`!include <path-included>`

where

<path-included>
  A path to files included.
  You can use the wildcard character :code:`*` (asterisk symbol)
  to specify multiple files.

*************************
Schema specification
*************************

The schema is defined with JSON Schema and explained with the terms of it.

.. jsonschema:: ../src/mcdecoder/schemas/mc_desc_schema.json
