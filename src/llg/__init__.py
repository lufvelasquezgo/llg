"""
llg
=====

  >>> import llg

Use the built-in ``help`` function to view a function's docstring::

  >>> llg --help

Utilities
---------


Viewing documentation using IPython
-----------------------------------


"""


__author__ = """Juan David Alzate Cardona"""
__email__ = "jdalzatec@unal.edu.co"
__version__ = "0.1.1"

from llg import ffunctions
from llg.site import Site
from llg.geometry import Geometry
from llg.bucket import Bucket
from llg.system import System
from llg.simulation import Simulation
from llg.store import StoreHDF
from llg.sample import Sample
from llg import predefined_structures
from llg import _tools
from llg import plot_states
