from __future__ import annotations

import json
from typing import List, Optional

import numpy

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

    def to_dict(self):
        return {
            "sites": [site.to_dict() for site in self._sites],
            "parameters": self._parameters.to_dict(),
            "temperatures": list(self._temperatures),
            "magnetic_field_intensities": list(self._magnetic_field_intensities),
            "num_iterations": self._num_iterations,
            "initial_state": self._initial_state,
            "seed": self._seed,
        }

    def save(self, filename):
        data = self.to_dict()
        with open(filename, "w") as file:
            json.dump(data, file, indent=2)

    @property
    def sites(self):
        return self._sites

    @property
    def parameters(self):
        return self._parameters

    @property
    def temperatures(self):
        return numpy.array(self._temperatures)

    @property
    def magnetic_field_intensities(self):
        return numpy.array(self._magnetic_field_intensities)

    @property
    def num_iterations(self):
        return self._num_iterations

    @property
    def initial_state(self):
        return self._initial_state

    @property
    def seed(self):
        return self._seed

    @property
    def num_sites(self):
        return len(self._sites)

    @property
    def sites_positions(self):
        return [site.position for site in self._sites]

    @property
    def sites_types(self):
        return [site.type for site in self._sites]

    @property
    def sites_mus(self):
        return numpy.array([site.mu for site in self._sites])

    @property
    def sites_magnetic_field_axes(self):
        return numpy.array([site.magnetic_field_axis for site in self._sites])

    @property
    def sites_jex_interactions_values(self):
        return numpy.array(
            [
                [jex_interaction.jex for jex_interaction in site.jex_interactions]
                for site in self._sites
            ]
        )

    @property
    def sites_neighbors_indexes(self):
        return numpy.array(
            [
                [
                    jex_interaction.neighbor_index
                    for jex_interaction in site.jex_interactions
                ]
                for site in self._sites
            ]
        )

    @property
    def sites_anisotropy_constants(self):
        return numpy.array([site.anisotropy_constant for site in self._sites])

    @property
    def sites_anisotropy_axes(self):
        return numpy.array([site.anisotropy_axis for site in self._sites])

    @property
    def num_th_points(self):
        return len(self._temperatures)

    @classmethod
    def from_file(cls, file_path) -> System:
        with open(file_path) as file:
            system_dict = json.load(file)

        sites = [Site.from_dict(site_dict) for site_dict in system_dict["sites"]]
        parameters = Parameters.from_dict(system_dict["parameters"])
        num_iterations = system_dict["num_iterations"]
        initial_state = system_dict.get("initial_state")
        seed = system_dict.get("seed")
        temperatures = ScalarList(system_dict["temperatures"])
        magnetic_field_intensities = ScalarList(
            system_dict["magnetic_field_intensities"]
        )

        return cls(
            sites=sites,
            parameters=parameters,
            temperatures=temperatures,
            magnetic_field_intensities=magnetic_field_intensities,
            num_iterations=num_iterations,
            initial_state=initial_state,
            seed=seed,
        )
