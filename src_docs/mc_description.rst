############################
MC description specification
############################

.. highlight:: yaml

***********************
Basic specification
***********************

.. literalinclude:: mc_desc_spec.yaml

*************************
Additional specifications
*************************

=======================================
Split a description into multiple files
=======================================

You can split a description into multiple parts by using :code:`!include` tag.

Expression: :code:`!include <path-included>`

where

<path-included>
  A path to files included.
  You can use wildcard character :code:`*` (asterisk symbol).

--------
Example
--------

* arm.yaml

  .. literalinclude:: ../sample/sample_descs/include/arm.yaml

* instructions/add_instructions.yaml

  .. literalinclude:: ../sample/sample_descs/include/instructions/add_instructions.yaml

* instructions/push_instructions.yaml

  .. literalinclude:: ../sample/sample_descs/include/instructions/push_instructions.yaml

You can see this :download:`example in github <https://github.com/wildlarva/mcdecoder/blob/master/sample/sample_descs/include>`.

*************************
Schema specification
*************************

The schema is defined with JSON Schema and explained with the terms of it.

.. jsonschema:: ../src/mcdecoder/schemas/mc_schema.json
