################################
Developer guides
################################

=============================================
Requirements for development
=============================================

* Ubuntu 18.x or above
* Python 3.8 or above (with pip and venv)
* Ruby 2.5 or above (with RubyGems)

=============================================
How to setup environment for development
=============================================

.. code-block:: bash

    # Install platform tools
    sudo apt install graphviz

    # Clone mcdecoder
    git clone https://github.com/wildlarva/mcdecoder.git

    # Create virtual environment and switch to it
    cd mcdecoder
    python3.8 -m venv env
    source env/bin/activate

    # Install python tools and libraries
    pip install -r requirements.txt
    conan remote add helmesjo https://api.bintray.com/conan/helmesjo/public-conan

    # Install ruby tools
    sudo gem install bundler
    bundle install

    # Install mcdecoder
    pip install -e .

After the installation, changes to the cloned directory will be
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


=============================================
How to build documents
=============================================

.. code-block:: bash

    # Switch to virtual environment
    cd <path-to-cloned-directory>
    source env/bin/activate

    # Build documents
    make -C src_docs clean apply-html
