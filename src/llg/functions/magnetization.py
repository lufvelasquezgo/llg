import numpy
from nptyping import NDArray
from typing import Any


def magnetization_vector(state: NDArray[(Any, 3), float]) -> NDArray[(Any, 3), float]:
    return state.mean(axis=1)


def magnetization_vector_by_type(
    state: NDArray[(Any, 3), float], num_types: int, types: NDArray[Any, float]
) -> NDArray[(Any, Any, 3), float]:
    out = numpy.zeros(shape=(num_types, 3))
    for t in range(num_types):
        mask = types == t
        out[t] = state[mask].mean(axis=1)
    return out


def total_magnetization(state: NDArray[(Any, 3), float]) -> float:
    return numpy.linalg.norm(magnetization_vector(state))


def magnetization_by_type(
    state: NDArray[(Any, 3), float], num_types: int, types: NDArray[Any, float]
) -> NDArray[Any, float]:
    mag = magnetization_vector_by_type(state, num_types, types)
    return numpy.linalg.norm(mag, axis=1)
