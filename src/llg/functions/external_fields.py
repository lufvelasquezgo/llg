import numpy
from nptyping import NDArray
from typing import Any


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
    value = (2 * damping * kB * temperature) / (
        gyromagnetic * magnitude_spin_moment * deltat
    )
    value = numpy.sqrt(value)
    return gamma * numpy.array([value, value, value]).T


def magnetic_field(
    magnetic_fields: NDArray[(Any, 3), float]
) -> NDArray[(Any, 3), float]:
    return magnetic_fields
