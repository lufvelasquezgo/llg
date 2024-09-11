import json
from typing import List, Optional

from llg.core.parameters import Parameters
from llg.core.types import Matrix
from llg.scalar_list import ScalarList
from llg.site import Site


class System:
    def __init__(
        self,
        sites: List[Site],
        parameters: Parameters,
        temperatures: ScalarList,
        magnetic_field_intensities: ScalarList,
        num_iterations: int,
        initial_state: Optional[Matrix] = None,
        seed: Optional[int] = None,
    ):
        self._sites = sites
        self._parameters = parameters
        self._temperatures = temperatures
        self._magnetic_field_intensities = magnetic_field_intensities
        self._num_iterations = num_iterations
        self._initial_state = initial_state
        self._seed = seed

    def save(self, filename):
        data = {
            "sites": [site.to_dict() for site in self._sites],
            "parameters": self._parameters.to_dict(),
            "temperatures": list(self._temperatures),
            "magnetic_field_intensities": list(self._magnetic_field_intensities),
            "num_iterations": self._num_iterations,
            "initial_state": self._initial_state,
            "seed": self._seed,
        }
        print(data)
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)
