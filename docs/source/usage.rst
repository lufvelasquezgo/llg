Usage
===============================

To use the llg library in a project. First you have to `install <https://pypi.org/>`_
the library. After the `installation`, you have to write in your program the
following:

.. code-block:: python

    import llg

You can do the following in an interactive Python session:

+---------------------------------------------+
| NOTE: This is an example to create a sample |
| with the predefined structures that the     |
| library support.                            |
+---------------------------------------------+

.. code-block:: python

    import llg
    from llg import predefined_structures
    import json

    output = "sample.json"
    sample = predefined_structures.GenericSc(3)
    sample.save(output)

This will generate a sample.json file in the same directory as the original
FILENAME.py file.

Furthermore, the library can be used in the command line through pipes,
as follow:

+---------------------------------------------+
| NOTE: With the library you can input a      |
| value, a list, a dictionary or a file of    |
| temperature and field.                      |
+---------------------------------------------+

.. code-block:: console

    $ llg build-samples generic-sc --length 2 sample.json
    Your sample file will not contain a valid value for temperature.
    Do you want to insert some values ? [Y/n]: __
    Select an option to the temperature (value, list, dict, file) [value]: __
    Insert 'start final step' values separated with spaces: __
    Your sample file will not contain a valid value for field.
    Do you want to insert some values ? [Y/n]: __
    Select an option to the field (value, list, dict, file) [value]: __
    Insert the field value: __

This tool is used just for create the sample, and as this documantation shows
in the readme the six functions that it was created for.

The library can produce the following plots:

PLOT OF THE AVERAGES

PLOT OF THE STATES

ANIMATION OF THE STATES
