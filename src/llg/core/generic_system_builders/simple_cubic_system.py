from itertools import product
from typing import List

from llg.core.generic_system_builders.generic_system import GenericSystem, SpatialPoint
from llg.core.types import Scalar


class SimpleCubicSystem(GenericSystem):
    def _build_spatial_points(self, length: int) -> List[SpatialPoint]:
        spatial_points = [
            SpatialPoint(
                index=i,
                position=(x, y, z),
            )
            for i, (x, y, z) in enumerate(product(range(length), repeat=3))
        ]

        for spatial_point in spatial_points:
            spatial_point.neighbors_indexes = self._get_neighbors_indexes(
                spatial_point, length
            )

        return spatial_points

    def _get_neighbors_indexes(
        self, spatial_point: SpatialPoint, length: int
    ) -> List[int]:
        x, y, z = spatial_point.position
        return [
            self._get_neighbor_index((x + 1) % length, y, z, length),
            self._get_neighbor_index((x - 1) % length, y, z, length),
            self._get_neighbor_index(x, (y + 1) % length, z, length),
            self._get_neighbor_index(x, (y - 1) % length, z, length),
            self._get_neighbor_index(x, y, (z + 1) % length, length),
            self._get_neighbor_index(x, y, (z - 1) % length, length),
        ]

    @staticmethod
    def _get_neighbor_index(x: Scalar, y: Scalar, z: Scalar, length: int) -> int:
        return int(x) * length * length + int(y) * length + int(z)
