from typing import Any

import numpy
from numba import jit
from numpy import ndarray


@jit(nopython=True)
def exchange_interaction_field(
    state: ndarray[(Any, 3), float],
    magnitude_spin_moment: ndarray[Any, float],
    exchanges: ndarray[(Any, Any), float],
    neighbors: ndarray[(Any, Any), float],
) -> ndarray[(Any, 3), float]:
    N = len(magnitude_spin_moment)
    out = numpy.zeros(shape=(N, 3))
    for i in range(N):
        exchanges_i = exchanges[i]
        exchanges_i_repeated = numpy.repeat(exchanges_i, 3)
        exchanges_i_repeated_reshaped = exchanges_i_repeated.reshape(
            (len(exchanges_i), 3)
        )
        neighbors_i = state[neighbors[i]]
        out[i] = (exchanges_i_repeated_reshaped * neighbors_i).sum(
            axis=0
        ) / magnitude_spin_moment[i]
    return out


@jit(nopython=True)
def anisotropy_interaction_field(
    state: ndarray[(Any, 3), float],
    magnitude_spin_moment: ndarray[Any, float],
    anisotropy_constants: ndarray[Any, float],
    anisotropy_vectors: ndarray[(Any, 3), float],
) -> ndarray[(Any, 3), float]:
    values = (
        anisotropy_constants
        * (state * anisotropy_vectors).sum(axis=1)
        / magnitude_spin_moment
    )
    values_repeated = numpy.repeat(values, 3)
    values_repeated_reshaped = values_repeated.reshape((len(values), 3))
    return 2 * values_repeated_reshaped * anisotropy_vectors
