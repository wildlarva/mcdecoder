################################
Internal design
################################

*********************************
Runtime environment
*********************************

Runtime structure and dependencies
================================================

.. digraph:: runtime

    node [shape=box]
    edge [style=dotted]

    subgraph cluster_mcdecoder {
        label = "mcdecoder"

        mcdecoder -> __main__ -> app -> {generator, exporter, emulator, checker} -> core
        generator -> templates
        core -> {schemas, grammars}

        mcdecoder [label = "mcdecoder (command)"]
        common
        __version__
        templates [label = "templates/*/*"]
        schemas [label = "schemas/*.json"]
        grammars [label = "grammars/*.lark"]
    }

    generator -> Jinja2
    checker -> numpy
    core -> {PyYAML, jsonschema, lark, numpy}

    lark [label = "Lark"]
    numpy [label = "NumPy"]
    deprecation

Modules in mcdecoder
================================================

.. table::

    +---------------+--------------------------------------------------+
    |Module         |Description                                       |
    +===============+==================================================+
    |__main__       |Python entrypoint of mcdecoder                    |
    +---------------+--------------------------------------------------+
    |app            |Implementation of the app workflow of mcdecoder   |
    |               |                                                  |
    |               |Parses command line options and dispatch          |
    |               |to each implementation of sub-commands.           |
    +---------------+--------------------------------------------------+
    |generator      |Implementation of the sub-command 'generate'      |
    |               |                                                  |
    |               |Generates codes according to templates.           |
    +---------------+--------------------------------------------------+
    |exporter       |Implementation of the sub-command 'export'        |
    |               |                                                  |
    |               |Exports MC description to other formats.          |
    +---------------+--------------------------------------------------+
    |emulator       |Implementation of the sub-command 'emulate'       |
    |               |                                                  |
    |               |Emulates a decoder and return decoded result.     |
    +---------------+--------------------------------------------------+
    |checker        |Implementation of the sub-command 'check'         |
    |               |                                                  |
    |               |Checks the integrity of a MC description.         |
    |               |Uses vectorized calculations for performance.     |
    +---------------+--------------------------------------------------+
    |core           |Provides core features of mcdecoder               |
    |               |                                                  |
    |               |Core features include:                            |
    |               |                                                  |
    |               |- Parse an MC description                         |
    |               |- Validate an MC description against the schema   |
    |               |- Create an instance of MC decoder model          |
    |               |- Emulate a decoder                               |
    +---------------+--------------------------------------------------+
    |common         |Provides common implementations of mcdecoder      |
    |               |                                                  |
    |               |Provides utilities and more to other modules.     |
    +---------------+--------------------------------------------------+
    |__version__    |Provides the version number of mcdecoder          |
    +---------------+--------------------------------------------------+

* Modules for sub-commands, such as generator, exporter, emulator
  and checker, provide the features of each sub-command.
  Each module provides implementations only for its sub-command.
* If multiple sub-commands require a certain feature,
  it should be defined in core module.
* If a certain implementation are not strongly related to mcdecoder,
  it should be defined in common module like making directories,
  converting the base of integer values, etc.
* Performance should be severely considered in checker module and
  the related features of core module.
  This module does billions of calculations for checking,
  so its performance is so important.
* All modules have dependencies to common and __version__ module.

Other important files in mcdecoder
================================================

.. table::

    +----------------+--------------------------------------------------+
    |Module          |Description                                       |
    +================+==================================================+
    |mcdecoder       |Shell script to run mcdecoder                     |
    |                |                                                  |
    |                |Automatically generated by Setuptools.            |
    +----------------+--------------------------------------------------+
    |templates/\*/\* |Jinja2 template files to generate a decoder       |
    +----------------+--------------------------------------------------+
    |schemas/\*.json |JSON Schema files to validate an MC description   |
    +----------------+--------------------------------------------------+
    |grammars/\*.lark|Lark files to parse an MC description             |
    +----------------+--------------------------------------------------+

Dependencies to external packages
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
    |deprecation  |Used to warn users about deprecated specifications|
    +-------------+--------------------------------------------------+

*********************************
Development environment
*********************************

Development structure and dependencies
================================================

.. digraph:: develop

    compound = true
    node [shape=box]
    edge [style=dotted]

    subgraph cluster_cmake {
        label = "CMake"

        cucumber_cpp [label = "Cucumber-Cpp"]
        google_test [label = "Google Test"]

        cucumber_cpp -> google_test
    }

    subgraph cluster_sphinx {
        label = "Sphinx"

        sphinx_argparse [label = "sphinx-\nargparse"]
        sphinx_jsonschema [label = "Sphinx\nJSON Schema"]
        sphinx_rtd_theme [label = "Read the Docs\nSphinx Theme"]
    }

    subgraph cluster_bundler {
        label = "Bundler"

        cucumber [label = "Cucumber"]
    }

    subgraph cluster_pytest {
        label = "pytest"

        pytest_cov [label = "pytest-cov"]
    }

    behave [label = "Behave"]
    graphviz [label = "Graphviz"]

    mcdecoder -> pytest_cov [lhead=cluster_pytest]
    mcdecoder -> behave
    mcdecoder -> cucumber_cpp [lhead=cluster_cmake]
    mcdecoder -> cucumber -> cucumber_cpp
    mcdecoder -> sphinx_rtd_theme [lhead=cluster_sphinx]
    sphinx_rtd_theme -> graphviz [ltail=cluster_sphinx]

Packages
================================================

.. table::

    ============================= ==========================================================
    Package                       Description
    ============================= ==========================================================
    mcdecoder                     This project
    pytest                        Used for unit tests for mcdecoder 
    pytest-cov                    Used to measure code coverage of unit tests
    Behave                        Used for feature tests for mcdecoder
    Bundler                       Used to fix the version of Cucumber.
                                  Cucumber-Cpp requires Cucumber v2.0
    CMake                         Used to build mcdecoder feature tests.
                                  It is also used to fetch and build packages of C/C++
    Cucumber                      Used for feature tests for generated decoders
    Cucumber-Cpp                  Used for feature tests for generated decoders in C/C++
    Google Test                   Provides testing functionalities to Cucumber-Cpp
    Sphinx                        Used to build documents
    sphinx-argparse               Used to build documents about command line options
    Sphinx JSON Schema            Used to build documents about the schema of MC description
    Read the Docs Sphinx Theme    Used to improve usability of generated documents
    Graphviz                      Used to show diagrams in documents
    ============================= ==========================================================

Directories
==================================

.. table::

    ============================= ==========================================================
    Directory                     Description of contents
    ============================= ==========================================================
    docs                          Documents published to GitHub Pages
    examples                      Example files used in tutorials and other documents
    src                           Source files to implement a mcdecoder
    src_docs                      RST files to generate documents in docs directory
    tests/common                  Common files used for both unit tests and feature tests
    tests/feature                 Feature tests for mcdecoders.
                                  This is mainly for testing generated decoders
    tests/module                  Unit tests for mcdecoder modules
    ============================= ==========================================================
