import numpy
from nptyping import NDArray
from typing import Any


def compute_exchange_energy(
    state: NDArray[(Any, 3), float],
    exchanges: NDArray[(Any, Any), float],
    neighbors: NDArray[(Any, Any), float],
) -> float:
    total = 0
    for i, state_i in enumerate(state):
        exchanges_i = exchanges[i]
        neighbors_i = state[neighbors[i]]
        total += (exchanges_i * (state_i * neighbors_i).sum(axis=1)).sum()
    return -total


def compute_anisotropy_energy(
    state: NDArray[(Any, 3), float],
    anisotropy_constants: NDArray[Any, float],
    anisotropy_vectors: NDArray[(Any, 3), float],
) -> float:
    return -(anisotropy_constants * (state * anisotropy_vectors).sum(axis=1)).sum()


def compute_magnetic_energy(
    magnitude_spin_moment: NDArray[Any, float],
    state: NDArray[(Any, 3), float],
    magnetic_fields: NDArray[(Any, 3), float],
) -> float:
    return -(magnitude_spin_moment * (state * magnetic_fields).sum(axis=1)).sum()
