from __future__ import annotations

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
        type: str,
        mu: float,
        anisotropy_constant: float,
        anisotropy_axis: Vector,
        magnetic_field_axis: Vector,
        jex_interactions: Optional[List[JexInteraction]] = None,
    ):
        self._index = index
        self._position = position
        self._type = type
        self._mu = mu
        self._anisotropy_constant = anisotropy_constant
        self._anisotropy_axis = anisotropy_axis
        self._magnetic_field_axis = magnetic_field_axis
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
            f"magnetic_field_axis={self._magnetic_field_axis!r})"
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
    def magnetic_field_axis(self) -> Vector:
        return self._magnetic_field_axis

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
            "magnetic_field_axis": list(self._magnetic_field_axis),
            "jex_interactions": [
                {
                    "neighbor_index": jex_interaction.neighbor_index,
                    "jex": jex_interaction.jex,
                }
                for jex_interaction in self._jex_interactions
            ],
        }

    @classmethod
    def from_dict(cls, site_dict: SiteDict) -> Site:
        return cls(
            index=site_dict["index"],
            position=(
                site_dict["position"][0],
                site_dict["position"][1],
                site_dict["position"][2],
            ),
            type=site_dict["type"],
            mu=site_dict["mu"],
            anisotropy_constant=site_dict["anisotropy_constant"],
            anisotropy_axis=(
                site_dict["anisotropy_axis"][0],
                site_dict["anisotropy_axis"][1],
                site_dict["anisotropy_axis"][2],
            ),
            magnetic_field_axis=(
                site_dict["magnetic_field_axis"][0],
                site_dict["magnetic_field_axis"][1],
                site_dict["magnetic_field_axis"][2],
            ),
            jex_interactions=[
                JexInteraction(
                    neighbor_index=jex_dict["neighbor_index"], jex=jex_dict["jex"]
                )
                for jex_dict in site_dict["jex_interactions"]
            ],
        )
