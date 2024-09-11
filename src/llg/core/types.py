from typing import List, Tuple, TypedDict, Union

from numpy import typing

Scalar = Union[int, float]
Matrix = typing.ArrayLike
Vector = Tuple[Scalar, Scalar, Scalar]


class RangeDict(TypedDict):
    start: Scalar
    final: Scalar
    step: Scalar


class JexInteractionDict(TypedDict):
    neighbor_index: int
    jex: float


class SiteDict(TypedDict):
    index: int
    position: List[Scalar]
    type: str
    mu: float
    anisotropy_constant: float
    anisotropy_axis: List[Scalar]
    magnetic_field_axis: List[Scalar]
    jex_interactions: List[JexInteractionDict]
