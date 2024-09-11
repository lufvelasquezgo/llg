import numpy
from numba import jit


def thermal_field(
    temperature,
    magnitude_spin_moment,
    damping: float,
    deltat: float,
    gyromagnetic: float,
    kB: float,
):
    N = len(magnitude_spin_moment)
    gamma = numpy.random.normal(size=(N, 3))
    values = (2 * damping * kB * temperature) / (
        gyromagnetic * magnitude_spin_moment * deltat
    )
    values = numpy.sqrt(values)
    values = numpy.repeat(values, 3).reshape((len(values), 3))
    return gamma * values


@jit(nopython=True)
def magnetic_field(magnetic_fields):
    return magnetic_fields
