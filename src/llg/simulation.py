import random

import numpy

from llg.core.system import System
from llg.functions import energy, heun
from llg.scalar_list_matcher import ScalarListMatcher


def get_random_state(num_sites):
    random_state = numpy.random.normal(size=(num_sites, 3))
    norms = numpy.linalg.norm(random_state, axis=1)
    random_state = [vec / norms[i] for i, vec in enumerate(random_state)]
    return random_state


class Simulation:
    def __init__(self, system: System):
        self._system = system
        self.seed = self._system.seed or random.getrandbits(32)
        self.initial_state = numpy.array(
            self._system.initial_state or get_random_state(self._system.num_sites)
        )

        numpy.random.seed(self.seed)

    @property
    def information(self):
        return {
            "num_sites": self._system.num_sites,
            "parameters": self._system.parameters,
            "temperatures": self._system.temperatures,
            "magnetic_field_intensities": self._system.magnetic_field_intensities,
            "seed": self.seed,
            "num_iterations": self._system.num_iterations,
            "positions": self._system.sites_positions,
            "types": self._system.sites_types,
            "initial_state": self.initial_state,
            "num_TH": self._system.num_th_points,
        }

    def run(self):
        spin_norms = self._system.sites_mus
        damping = self._system.parameters.damping
        deltat = self._system.parameters.delta_time
        gyromagnetic = self._system.parameters.gyromagnetic
        kb = self._system.parameters.kb
        field_axes = self._system.sites_magnetic_field_axes
        exchanges = self._system.sites_jex_interactions_values
        neighbors = self._system.sites_neighbors_indexes
        anisotropy_constants = self._system.sites_anisotropy_constants
        anisotropy_vectors = self._system.sites_anisotropy_axes
        num_sites = self._system.num_sites
        state = self.initial_state

        for th_index, (T, H) in enumerate(
            ScalarListMatcher(
                self._system.temperatures, self._system.magnetic_field_intensities
            )
        ):
            temperatures = numpy.array([T] * num_sites)
            magnetic_fields = H * field_axes

            for iteration in range(self._system.num_iterations):
                state = heun.integrate(
                    state,
                    spin_norms,
                    temperatures,
                    damping,
                    deltat,
                    gyromagnetic,
                    kb,
                    magnetic_fields,
                    exchanges,
                    neighbors,
                    anisotropy_constants,
                    anisotropy_vectors,
                )

                exchange_energy_value = energy.compute_exchange_energy(
                    state, exchanges, neighbors
                )
                anisotropy_energy_value = energy.compute_anisotropy_energy(
                    state, anisotropy_constants, anisotropy_vectors
                )
                magnetic_field_energy_value = energy.compute_magnetic_energy(
                    state, spin_norms, magnetic_fields
                )
                total_energy_value = (
                    exchange_energy_value
                    + anisotropy_energy_value
                    + magnetic_field_energy_value
                )

                yield (
                    th_index,
                    iteration,
                    state,
                    exchange_energy_value,
                    anisotropy_energy_value,
                    magnetic_field_energy_value,
                    total_energy_value,
                )
