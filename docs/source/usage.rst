Usage
===============================

To use the llg library in a project. First you have to `install <https://pypi.org/>`_
the library. After the `installation`, you have two options to use it. The
first one is by using the ``command line``, and the second one is to import
the library in your program.

Examples
********

Example one
-----------

The library can be used in the command line through pipes, as follow:

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

This will generate a sample.json file in the same directory where the
repository is saved.

With the file, we can do a simulation to get the evolution of the spin system,
and at the same time we can store the results on a HDF file.

.. code-block:: console

    $ llg simulate sample.json | llg store-hdf sample.hdf

This will generate a sample.hdf file in the same directory where the
repository is saved.

Then, we want to read the hdf file to compute the averages of the
magnetization and the energy, and make plots of each one, is as follow:

.. code-block:: console

    $ llg read-hdf sample.hdf | llg compute-averages | llg plot plot-averages images

It creates a PDF document with each plot.

* The first one is a graph of temperature versus anisotropy energy, exchange
  energy, field energy, and the total energy (all of them are in the same
  figure).
* The second one is a graph of field versus anisotropy energy, exchange energy,
  field energy, and the total energy (all of them are in the same figure).
* The third one is a graph of temperature versus magnetization.
* The last one is a graph of field versus magnetization.

Furthermore, the command ``compute-averages`` has other options for calculate
the averages of energy and magnetization.

For this example, the image is as follow:

.. figure:: images

.. code-block:: console

    $ llg compute-averages --help
    Usage: llg compute-averages [OPTIONS]

    Options:
    --by-types         It allows to compute avarages by type.
    --components       It allows to compute avarages by components.
    --discard INTEGER  It allows to discard some iterations at the time to
                        compute avarages.
    --help             Show this message and exit.



Example two
-----------

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


