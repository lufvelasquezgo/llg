from typing import Any

import numpy
from numba import jit
from numpy import ndarray


@jit(nopython=True)
def magnetization_vector(state: ndarray[(Any, 3), float]) -> ndarray[(Any, 3), float]:
    return state.sum(axis=0) / len(state)


@jit(nopython=True)
def magnetization_vector_by_type(
    state: ndarray[(Any, 3), float], num_types: int, types: ndarray[Any, float]
) -> ndarray[(Any, Any, 3), float]:
    out = numpy.zeros(shape=(num_types, 3))
    for t in range(num_types):
        mask = types == t
        out[t] = state[mask].sum(axis=0) / numpy.sum(mask)
    return out


@jit(nopython=True)
def total_magnetization(state: ndarray[(Any, 3), float]) -> float:
    mag = magnetization_vector(state)
    mag_sum = (mag * mag).sum(axis=0)
    return numpy.sqrt(mag_sum)


@jit(nopython=True)
def magnetization_by_type(
    state: ndarray[(Any, 3), float], num_types: int, types: ndarray[Any, float]
) -> ndarray[Any, float]:
    mag = magnetization_vector_by_type(state, num_types, types)
    return numpy.sqrt((mag * mag).sum(axis=1))
