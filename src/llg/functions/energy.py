from typing import Any

from numba import jit
from numpy import ndarray


@jit(nopython=True)
def compute_exchange_energy(
    state: ndarray[(Any, 3), float],
    exchanges: ndarray[(Any, Any), float],
    neighbors: ndarray[(Any, Any), float],
) -> float:
    total = 0
    N = len(state)
    for i in range(N):
        state_i = state[i]
        exchanges_i = exchanges[i]
        neighbors_i = state[neighbors[i]]
        total -= (exchanges_i * (state_i * neighbors_i).sum(axis=1)).sum()
    return 0.5 * total


@jit(nopython=True)
def compute_anisotropy_energy(
    state: ndarray[(Any, 3), float],
    anisotropy_constants: ndarray[Any, float],
    anisotropy_vectors: ndarray[(Any, 3), float],
) -> float:
    return -(anisotropy_constants * (state * anisotropy_vectors).sum(axis=1) ** 2).sum()


@jit(nopython=True)
def compute_magnetic_energy(
    state: ndarray[(Any, 3), float],
    magnitude_spin_moment: ndarray[Any, float],
    magnetic_fields: ndarray[(Any, 3), float],
) -> float:
    return -(magnitude_spin_moment * (state * magnetic_fields).sum(axis=1)).sum()
