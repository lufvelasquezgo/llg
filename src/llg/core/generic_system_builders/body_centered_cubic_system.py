from itertools import product
from typing import List

from llg.core.generic_system_builders.generic_system import GenericSystem, SpatialPoint
from llg.core.types import Scalar


class BodyCenteredCubicSystem(GenericSystem):
    def _build_spatial_points(self, length: int) -> List[SpatialPoint]:
        spatial_points = []
        for i, (x, y, z) in enumerate(product(range(length), repeat=3)):
            spatial_points.extend(
                [
                    SpatialPoint(index=2 * i, position=(x, y, z)),
                    SpatialPoint(index=2 * i + 1, position=(x + 0.5, y + 0.5, z + 0.5)),
                ]
            )

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
            self._get_neighbor_index(
                (x + 0.5) % length, (y + 0.5) % length, (z + 0.5) % length, length
            ),
            self._get_neighbor_index(
                (x + 0.5) % length, (y + 0.5) % length, (z - 0.5) % length, length
            ),
            self._get_neighbor_index(
                (x + 0.5) % length, (y - 0.5) % length, (z + 0.5) % length, length
            ),
            self._get_neighbor_index(
                (x + 0.5) % length, (y - 0.5) % length, (z - 0.5) % length, length
            ),
            self._get_neighbor_index(
                (x - 0.5) % length, (y + 0.5) % length, (z + 0.5) % length, length
            ),
            self._get_neighbor_index(
                (x - 0.5) % length, (y + 0.5) % length, (z - 0.5) % length, length
            ),
            self._get_neighbor_index(
                (x - 0.5) % length, (y - 0.5) % length, (z + 0.5) % length, length
            ),
            self._get_neighbor_index(
                (x - 0.5) % length, (y - 0.5) % length, (z - 0.5) % length, length
            ),
        ]

    @staticmethod
    def _get_neighbor_index(x: Scalar, y: Scalar, z: Scalar, length: int) -> int:
        base = 2 * (int(x) * length * length + int(y) * length + int(z))
        if int(x) == x and int(y) == y and int(z) == z:
            return base
        else:
            return base + 1
