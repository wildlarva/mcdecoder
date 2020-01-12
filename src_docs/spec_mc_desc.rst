############################
MC description specification
############################

.. highlight:: yaml

***********************
Basic specification
***********************

.. literalinclude:: spec_mc_desc.yaml

*************************
Additional specifications
*************************

=======================================
Split a description into multiple files
=======================================

You can split a description into multiple files by using :code:`!include` tag.
You can use it anywhere in a description and
the contents of specified files will be inserted into the place
where the tag is.
If multiple files are specified, the contents will be combined.
The behavior depends on the types of the contents of files included:

* Sequence: Produce one sequence consisting of the elements of all sequences.
* Mapping: Produce one mapping consisting of the elements of all mappings.
* Scalar: Produce one sequence consisting of scalars.
* Mixture: Prompt an error.

Expression: :code:`!include <path-included>`

where

<path-included>
  A path to files included.
  You can use the wildcard character :code:`*` (asterisk symbol)
  to specify multiple files.

--------
Example
--------

.. literalinclude:: ../examples/include/arm.yaml
    :caption: arm.yaml

.. literalinclude:: ../examples/include/instructions/add_instructions.yaml
    :caption: instructions/add_instructions.yaml

.. literalinclude:: ../examples/include/instructions/push_instructions.yaml
    :caption: instructions/push_instructions.yaml

You can see this :download:`example in github <https://github.com/wildlarva/mcdecoder/blob/master/examples/include>`.

*************************
Schema specification
*************************

The schema is defined with JSON Schema and explained with the terms of it.

.. jsonschema:: ../src/mcdecoder/schemas/mc_desc_schema.json
