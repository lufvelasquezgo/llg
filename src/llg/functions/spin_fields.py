import numpy
from nptyping import NDArray
from typing import Any


def exchange_interaction_field(
    state: NDArray[(Any, 3), float],
    magnitude_spin_moment: NDArray[Any, float],
    exchanges: NDArray[(Any, Any), float],
    neighbors: NDArray[(Any, Any), float],
) -> NDArray[(Any, 3), float]:
    N = len(magnitude_spin_moment)
    out = numpy.zeros(shape=(N, 3))
    for i in range(N):
        exchanges_i = exchanges[i]
        neighbors_i = state[neighbors[i]]
        out[i] = (exchanges_i * neighbors_i).sum() / magnitude_spin_moment[i]
    return out


def anisotropy_interaction_field(
    state: NDArray[(Any, 3), float],
    magnitude_spin_moment: NDArray[Any, float],
    anisotropy_constants: NDArray[Any, float],
    anisotropy_vectors: NDArray[(Any, 3), float],
) -> NDArray[(Any, 3), float]:
    value = (
        anisotropy_constants
        * (state * anisotropy_vectors).sum(axis=1)
        / magnitude_spin_moment
    )
    return 2 * numpy.array([value, value, value]).T * anisotropy_vectors
