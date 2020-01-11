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

For this example, we put the following parameters:

.. code-block::

    "temperature": {
    "start": 5.0,
    "final": 0.05,
    "step": 0.05
    },
    "field": 1.0,

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

The plot that we get with this command of the library is the follow:

.. image:: /images/image1.png
.. image:: /images/image2.png

Furthermore, the command ``compute-averages`` has other options for calculate
the averages of energy and magnetization.

.. code-block:: console

    $ llg compute-averages --help
    Usage: llg compute-averages [OPTIONS]

    Options:
    --by-types         It allows to compute avarages by type.
    --components       It allows to compute avarages by components.
    --discard INTEGER  It allows to discard some iterations at the time to
                        compute avarages.
    --help             Show this message and exit.

Also, if we want to get a graph of the spin system evolution we can do it
with the library as follow:

.. code-block:: console

    $ llg read-hdf sample.hdf | llg plot plot-states figure

The library create a folder with the name that you give when you used the
command. In our example we named `figure`. This is a picture of how and where
it is created.

.. image:: /images/image3.png
.. image:: /images/image4.png

We get an amount of images. Each one represents an state of the spin system.
This is the first plot that we get:

.. image:: /images/image5.png

Moreover, the command ``plot-states`` has other options for plot the
spin system evolution.

.. code-block:: console

    $ llg plot plot-states --help
    Usage: llg plot plot-states [OPTIONS] OUTPUT

    Options:
    --step TEXT               Step separation between plots. If step=max, it
                                will be the amount of iterations.
    --size INTEGER            Figure length size in pixels.
    --mode [azimuthal|polar]  Color mode
    --colormap TEXT           Color map. Matplotlib supported colormaps: https:/
                                /matplotlib.org/examples/color/colormaps_reference
                                .html
    --help                    Show this message and exit.

Finally, we can get an animation video with the spin system evolution.

.. code-block:: console

    $ llg read-hdf sample.hdf | llg plot animate-states video.mp4
    Moviepy - Building video video.mp4.
    Moviepy - Writing video video.mp4

    Moviepy - Done !
    Moviepy - video ready video.mp4

It creates a video mp4 in the folder where the library is.

.. image:: /images/image6.png

Example two
-----------

The library can be used in a program file, as follow:

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

Also, you can do everything that we did in the previous example.
