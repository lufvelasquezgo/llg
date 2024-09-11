from dataclasses import dataclass
from typing import List, Optional

from llg.core.types import SiteDict, Vector


@dataclass
class JexInteraction:
    neighbor_index: int
    jex: float


class Site:
    def __init__(
        self,
        index: int,
        position: Vector,
        type_: str,
        mu: float,
        anisotropy_constant: float,
        anisotropy_axis: Vector,
        field_axis: Vector,
        jex_interactions: Optional[List[JexInteraction]] = None,
    ):
        self._index = index
        self._position = position
        self._type = type_
        self._mu = mu
        self._anisotropy_constant = anisotropy_constant
        self._anisotropy_axis = anisotropy_axis
        self._field_axis = field_axis
        self._jex_interactions = jex_interactions or []

    def __repr__(self) -> str:
        return (
            f"Site("
            f"index={self._index!r}, "
            f"position={self._position!r}, "
            f"type={self._type!r}, "
            f"mu={self._mu!r}, "
            f"anisotropy_constant={self._anisotropy_constant!r}, "
            f"anisotropy_axis={self._anisotropy_axis!r}, "
            f"field_axis={self._field_axis!r})"
        )

    @property
    def index(self) -> int:
        return self._index

    @property
    def position(self) -> Vector:
        return self._position

    @property
    def type(self) -> str:
        return self._type

    @property
    def mu(self) -> float:
        return self._mu

    @property
    def anisotropy_constant(self) -> float:
        return self._anisotropy_constant

    @property
    def anisotropy_axis(self) -> Vector:
        return self._anisotropy_axis

    @property
    def field_axis(self) -> Vector:
        return self._field_axis

    @property
    def jex_interactions(self) -> List[JexInteraction]:
        return self._jex_interactions

    def add_jex_interaction(self, neighbor_index: int, jex: float) -> None:
        self._jex_interactions.append(JexInteraction(neighbor_index, jex))

    def to_dict(self) -> SiteDict:
        return {
            "index": self._index,
            "position": list(self._position),
            "type": self._type,
            "mu": self._mu,
            "anisotropy_constant": self._anisotropy_constant,
            "anisotropy_axis": list(self._anisotropy_axis),
            "field_axis": list(self._field_axis),
            "jex_interactions": [
                {
                    "neighbor_index": jex_interaction.neighbor_index,
                    "jex": jex_interaction.jex,
                }
                for jex_interaction in self._jex_interactions
            ],
        }
