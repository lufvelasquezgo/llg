"""
llg
=====

Provides


How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided
with the code, and a loose standing reference guide, available from
`the NumPy homepage <https://www.scipy.org>`_.

We recommend exploring the docstrings using
`IPython <https://ipython.org>`_, an advanced Python shell with
TAB-completion and introspection capabilities.  See below for further
instructions.

  >>> import llg

Use the built-in ``help`` function to view a function's docstring::

  >>> llg --help

General-purpose documents like a glossary and help on the basic concepts
of numpy are available under the ``doc`` sub-module::

  >>> from numpy import doc
  >>> help(doc)
  ... # doctest: +SKIP

Available subpackages
---------------------


Utilities
---------


Viewing documentation using IPython
-----------------------------------


Copies vs. in-place operation
-----------------------------
"""


__author__ = """Juan David Alzate Cardona"""
__email__ = "jdalzatec@unal.edu.co"
__version__ = "0.1.0"

from llg import _tools, ffunctions, plot_states, predefined_structures
from llg.bucket import Bucket
from llg.geometry import Geometry
from llg.sample import Sample
from llg.simulation import Simulation
from llg.site import Site
from llg.store import StoreHDF
from llg.system import System
