from itertools import product
from typing import Iterable, Union

from llg.core.constants import GENERIC_SAMPLE_TYPE, EnergyUnit
from llg.core.parameters import Parameters
from llg.core.system import System
from llg.core.types import RangeDict, Scalar, Vector
from llg.scalar_list import ScalarList
from llg.site import Site


class SimpleCubicSystem(System):
    def __init__(
        self,
        length: int,
        temperature: Union[Scalar, RangeDict, Iterable[Scalar]],
        magnetic_field_intensity: Union[Scalar, RangeDict, Iterable[Scalar]],
        energy_unit: EnergyUnit,
        damping: float,
        gyromagnetic: float,
        delta_time: float,
        jex: float,
        mu: float,
        magnetic_field_axis: Vector,
        anisotropy_axis: Vector,
        anisotropy_constant: float,
        num_iterations: int,
    ):
        sites = self._build_sites(
            length, jex, mu, magnetic_field_axis, anisotropy_axis, anisotropy_constant
        )
        parameters = Parameters(
            energy_unit=energy_unit,
            damping=damping,
            gyromagnetic=gyromagnetic,
            delta_time=delta_time,
        )
        temperatures = ScalarList(temperature)
        magnetic_field_intensities = ScalarList(magnetic_field_intensity)
        super().__init__(
            sites=sites,
            parameters=parameters,
            temperatures=temperatures,
            magnetic_field_intensities=magnetic_field_intensities,
            num_iterations=num_iterations,
        )

    def _build_sites(
        self, length, jex, mu, magnetic_field_axis, anisotropy_axis, anisotropy_constant
    ):
        sites = [
            Site(
                index=i,
                position=(x, y, z),
                type_=GENERIC_SAMPLE_TYPE,
                mu=mu,
                anisotropy_constant=anisotropy_constant,
                anisotropy_axis=anisotropy_axis,
                magnetic_field_axis=magnetic_field_axis,
            )
            for i, (x, y, z) in enumerate(product(range(length), repeat=3))
        ]

        for site in sites:
            x, y, z = site.position
            site.add_jex_interaction(
                self._get_neighbor_index((x + 1) % length, y, z, length), jex
            )
            site.add_jex_interaction(
                self._get_neighbor_index((x - 1) % length, y, z, length), jex
            )
            site.add_jex_interaction(
                self._get_neighbor_index(x, (y + 1) % length, z, length), jex
            )
            site.add_jex_interaction(
                self._get_neighbor_index(x, (y - 1) % length, z, length), jex
            )
            site.add_jex_interaction(
                self._get_neighbor_index(x, y, (z + 1) % length, length), jex
            )
            site.add_jex_interaction(
                self._get_neighbor_index(x, y, (z - 1) % length, length), jex
            )

        return sites

    @staticmethod
    def _get_neighbor_index(x, y, z, length):
        return x * length * length + y * length + z
