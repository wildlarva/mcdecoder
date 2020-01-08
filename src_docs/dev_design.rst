################################
Internal design
################################

*********************************
Runtime environment
*********************************

.. digraph:: runtime

    node [shape=box]
    edge [style=dotted]

    subgraph cluster_mcdecoder {
        label = "mcdecoder"
        mcdecoder -> __main__ -> app -> {generator, exporter, emulator, checker} -> core
        common
        mcdecoder [label = "mcdecoder (command)"]
    }

    generator -> Jinja2
    checker -> numpy
    core -> {PyYAML, jsonschema, lark, numpy}
    lark [label="Lark"]
    numpy [label="NumPy"]


================================================
Modules and other important files in mcdecoder
================================================

.. table::

    +--------------+--------------------------------------------------+
    |Module/File   |Description                                       |
    +==============+==================================================+
    |mcdecoder     |Shell script to run mcdecoder                     |
    +--------------+--------------------------------------------------+
    |__main__      |Python entrypoint of mcdecoder                    |
    +--------------+--------------------------------------------------+
    |app           |Implement app workflow of mcdecoder               |
    |              |                                                  |
    |              |Parses command line options and dispatch          |
    |              |to each implementation of sub-commands.           |
    +--------------+--------------------------------------------------+
    |generator     |Implementation of the sub-command 'generate'      |
    |              |                                                  |
    |              |Generates codes according to templates.           |
    +--------------+--------------------------------------------------+
    |exporter      |Implementation of the sub-command 'export'        |
    |              |                                                  |
    |              |Exports MC description to other formats.          |
    +--------------+--------------------------------------------------+
    |emulator      |Implementation of the sub-command 'emulate'       |
    |              |                                                  |
    |              |Emulates a decoder and return decoded result.     |
    +--------------+--------------------------------------------------+
    |checker       |Implementation of the sub-command 'check'         |
    |              |                                                  |
    |              |Checks the integrity of a MC description.         |
    |              |Uses vectorized calculations for performance.     |
    +--------------+--------------------------------------------------+
    |core          |Provides core features of mcdecoder               |
    |              |                                                  |
    |              |Core features include:                            |
    |              |                                                  |
    |              |- Parse an MC description                         |
    |              |- Validate an MC description against the schema   |
    |              |- Create an instance of MC decoder model          |
    |              |- Emulate a decoder                               |
    +--------------+--------------------------------------------------+
    |common        |Provides common implementations of mcdecoder      |
    |              |                                                  |
    |              |Provides utilities and more to other modules.     |
    +--------------+--------------------------------------------------+

- Modules for sub-commands, such as generator, exporter, emulator
  and checker, provide the features of each sub-command.
  Each module provides implementations only for its sub-command.
- If multiple sub-commands require a certain feature,
  it should be defined in core module.
- If a certain implementation are not strongly related to mcdecoder,
  it should be defined in common module like making directories,
  converting the base of integer values, etc.
- Performance should be severely considered in checker module and
  the related features of core module.
  This module does billions of calculations for checking,
  so its performance is so important.
- All modules have dependencies to common module.

==================================
Dependencies to external package
==================================

.. table::

    +-------------+--------------------------------------------------+
    |Package      |Description                                       |
    +=============+==================================================+
    |PyYAML       |Used to load an MC description                    |
    +-------------+--------------------------------------------------+
    |jsonschema   |Used to validate an MC description                |
    +-------------+--------------------------------------------------+
    |Lark         |Used to parse an MC description                   |
    +-------------+--------------------------------------------------+
    |NumPy        |Used to improve the performance of the sub-command|
    |             |'check'                                           |
    +-------------+--------------------------------------------------+
    |Jinja2       |Used to generate codes                            |
    +-------------+--------------------------------------------------+

*********************************
Develop environment
*********************************

.. digraph:: develop

    compound = true
    node [shape=box]
    edge [style=dotted]

    subgraph cluster_sphinx {
        label = "Sphinx"
        sphinx_argparse [label="sphinx-\nargparse"]
        sphinx_jsonschema [label="Sphinx\nJSON Schema"]
        sphinx_rtd_theme [label="Read the Docs\nSphinx Theme"]
        m2r [label="M2R"]
        graphviz [label="Graphviz"]
    }

    subgraph cluster_conan {
        label = "Conan"
        google_test [label="Google Test"]
    }

    mcdecoder -> pytest
    mcdecoder -> sphinx_rtd_theme [lhead=cluster_sphinx]
    mcdecoder -> google_test [lhead=cluster_conan]

.. table::

    ============================= ==========================================================
    Package                       Description
    ============================= ==========================================================
    mcdecoder                     This project
    pytest                        Used to test mcdecoder
    Conan                         Used to manage packages of C/C++
    Google Test                   Used to test generated decoders in C/C++
    Sphinx                        Used to build documents
    sphinx-argparse               Used to build documents about command line options
    Sphinx JSON Schema            Used to build documents about the schema of MC description
    Read the Docs Sphinx Theme    Used to improve usability of generated documents
    M2R                           Used to import README.md to Sphinx
    Graphviz                      Used to show diagrams in documents
    ============================= ==========================================================
