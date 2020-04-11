import numpy
from nptyping import NDArray
from typing import Any
from numba import jit


def thermal_field(
    temperature: NDArray[(Any, 3), float],
    magnitude_spin_moment: NDArray[Any, float],
    damping: float,
    deltat: float,
    gyromagnetic: float,
    kB: float,
) -> NDArray[(Any, 3), float]:
    N = len(magnitude_spin_moment)
    gamma = numpy.random.normal(size=(N, 3))
    values = (2 * damping * kB * temperature) / (
        gyromagnetic * magnitude_spin_moment * deltat
    )
    values = numpy.sqrt(values)
    values = numpy.repeat(values, 3).reshape((len(values), 3))
    return gamma * values


@jit(nopython=True)
def magnetic_field(
    magnetic_fields: NDArray[(Any, 3), float]
) -> NDArray[(Any, 3), float]:
    return magnetic_fields
