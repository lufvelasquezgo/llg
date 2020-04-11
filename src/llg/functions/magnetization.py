import numpy
from nptyping import NDArray
from typing import Any
from numba import jit


@jit(nopython=True)
def magnetization_vector(state: NDArray[(Any, 3), float]) -> NDArray[(Any, 3), float]:
    return state.sum(axis=0) / len(state)


@jit(nopython=True)
def magnetization_vector_by_type(
    state: NDArray[(Any, 3), float], num_types: int, types: NDArray[Any, float]
) -> NDArray[(Any, Any, 3), float]:
    out = numpy.zeros(shape=(num_types, 3))
    for t in range(num_types):
        mask = types == t
        out[t] = state[mask].sum(axis=0) / numpy.sum(mask)
    return out


@jit(nopython=True)
def total_magnetization(state: NDArray[(Any, 3), float]) -> float:
    mag = magnetization_vector(state)
    mag_sum = (mag * mag).sum(axis=0)
    return numpy.sqrt(mag_sum)


@jit(nopython=True)
def magnetization_by_type(
    state: NDArray[(Any, 3), float], num_types: int, types: NDArray[Any, float]
) -> NDArray[Any, float]:
    mag = magnetization_vector_by_type(state, num_types, types)
    return numpy.sqrt((mag * mag).sum(axis=1))
