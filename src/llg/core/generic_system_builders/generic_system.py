from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, List, Tuple, Union

from llg.core.constants import GENERIC_TYPE, EnergyUnit
from llg.core.parameters import Parameters
from llg.core.system import System
from llg.core.types import RangeDict, Scalar, Vector
from llg.scalar_list import ScalarList
from llg.site import JexInteraction, Site


@dataclass
class SpatialPoint:
    index: int
    position: Tuple[Scalar, Scalar, Scalar]
    neighbors_indexes: List[int] = field(default_factory=list)


class GenericSystem(System, ABC):
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
        self,
        length: int,
        jex: float,
        mu: float,
        magnetic_field_axis: Vector,
        anisotropy_axis: Vector,
        anisotropy_constant: float,
    ) -> List[Site]:
        spatial_points = self._build_spatial_points(length)
        return [
            Site(
                index=spatial_point.index,
                position=spatial_point.position,
                type=GENERIC_TYPE,
                mu=mu,
                anisotropy_constant=anisotropy_constant,
                anisotropy_axis=anisotropy_axis,
                magnetic_field_axis=magnetic_field_axis,
                jex_interactions=[
                    JexInteraction(neighbor_index, jex)
                    for neighbor_index in spatial_point.neighbors_indexes
                ],
            )
            for spatial_point in spatial_points
        ]

    @abstractmethod
    def _build_spatial_points(self, length: int) -> List[SpatialPoint]:
        pass
