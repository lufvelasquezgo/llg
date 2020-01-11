Readme
===============================

The llg library has been used to simulate the spin evolution of magnetics
materials. It consists on pass a sample with the following form

.. code-block::

   {
      "geometry":{
         "sites": [
            {
               "index":__,
               "position":__,
               "type":__,
               "mu":__,
               "anisotropy_constant":__,
               "anisotopy_axis":__,
               "field_axis":__
            } ...
         ],
         "neighbors": [
            {
               "source":__,
               "target":__,
               "jex":__
            } ...
         ],
      },
      "parameters": {
         "units":__,
         "damping":__,
         "gyromagnetic":__,
         "deltat":__
      },
      "temperature": {
         "start":__,
         "final":__,
         "step":__
      },
      "field":__,
      "num_iterations":__
   }

The llg library has six functions.

* build-samples:
               It creates a sample with some predefined structures and with
               the form presented above.
* compute-averages:
                  It computes the averages of magnetization and energy with
                  respect of the temperature and field. It allows to compute
                  averages `by-types`, `components` and, `discard` a number
                  of iterations.
* plot:
      It creates plots of averages and, the states. Also, it creates a video or
      a gif of the states.

      .. code-block:: console

         Usage: llg plot [OPTIONS] COMMAND [ARGS]...

         Options:
         --help  Show this message and exit.

         Commands:
         animate-states
         plot-averages
         plot-states

* read-hdf:
         It reads the hdf file with the information of the simulation.
* simulate:
         It makes the simulation and, it provides information about the
         states, each energy, and the total energy. It holds the completely
         information needed for the construction of the spin system.
* store-hdf:
            It saves the information of the simulation in a hdf file. This way
            of storing is an efficient movement of data from one stored
            representation to another stored representation.

.. code-block:: console

   $ llg --help
   Usage: llg [OPTIONS] COMMAND [ARGS]...

   Console script for llg.

   Options:
   --help  Show this message and exit.

   Commands:
   build-samples
   compute-averages
   plot
   read-hdf
   simulate
   store-hdf

**LLG library is very useful to study the properties of magnetic materials.**
