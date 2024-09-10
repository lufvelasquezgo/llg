from typing import Any

import numpy
from numba import jit
from numpy import ndarray


def thermal_field(
    temperature: ndarray[(Any, 3), float],
    magnitude_spin_moment: ndarray[Any, float],
    damping: float,
    deltat: float,
    gyromagnetic: float,
    kB: float,
) -> ndarray[(Any, 3), float]:
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
    magnetic_fields: ndarray[(Any, 3), float]
) -> ndarray[(Any, 3), float]:
    return magnetic_fields
