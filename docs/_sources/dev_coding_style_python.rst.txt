################################
Python coding style
################################

The coding style of mcdecoder in Python is based on `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`__.
The mcdecoder adds some modifications to it
because of the environment for development.

*********************************
Exceptions to the rule
*********************************

Python Language Rules / Imports
=========================================================================

This project
    Use relative names in imports if the module is in the same package.
Original
    Do not use relative names in imports.
    Even if the module is in the same package, use the full package name.
    This helps prevent unintentionally importing a package twice.
Rationale
    Pyright cannot resolve the conflict between
    the packages in relative directories and those in pip,
    so you must specify the packages in relative directories
    to resolve the conflict.

You can see also `the original 'Python Language Rules / Imports' <https://google.github.io/styleguide/pyguide.html#22-imports>`__.
