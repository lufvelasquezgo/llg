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
    values = numpy.sqrt(
        (2.0 * damping * kB * temperature)
        / (gyromagnetic * magnitude_spin_moment * deltat)
    )
    values = values.reshape(tuple((*values.shape, 1)))
    return gamma * values


@jit(nopython=True)
def magnetic_field(magnetic_fields):
    return magnetic_fields
