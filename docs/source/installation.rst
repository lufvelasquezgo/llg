.. highlight:: shell

============
Installation
============


Stable release
--------------

To install llg, run this command in your terminal:

.. code-block:: console

    $ pip install llg

This is the preferred method to install llg, as it will always install the
most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for llg can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/jdalzatec/llg

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/jdalzatec/llg/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/jdalzatec/llg
.. _tarball: https://github.com/jdalzatec/llg/tarball/master


Prerequisite: POV-Ray
-------------------------

It is important to know that for use the tool plot is requirement `POV-Ray <http://www.povray.org/>`_.
POV-Ray is used to create the arrows that represent the spin moments.
It shows the evolution during the iteration step with a set temperature and
field.
