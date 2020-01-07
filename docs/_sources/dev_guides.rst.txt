################################
Guides for developers
################################

=============================================
Requirements for development
=============================================

* Python 3.8 (with pip and venv)

=============================================
How to setup environment for development
=============================================

.. code-block:: bash

    # Clone mcdecoder
    git clone https://github.com/wildlarva/mcdecoder.git

    # Create virtual environment and switch to it
    cd mcdecoder
    python3.8 -m venv env
    source env/bin/activate

    # Install python tools and libraries
    pip install -r requirements.txt

    # Install mcdecoder
    pip install -e .

After the installation, changes to the cloned directory are
immediately reflected to mcdecoder you installed.

=============================================
How to run tests for mcdecoder
=============================================

.. code-block:: bash

    # Switch to virtual environment
    cd <path-to-cloned-directory>
    source env/bin/activate

    # Run tests
    pytest

=============================================
How to run tests for generated decoders
=============================================

.. code-block:: bash

    # Switch to virtual environment
    cd <path-to-cloned-directory>
    source env/bin/activate

    # Run tests
    make -C ctest clean test
