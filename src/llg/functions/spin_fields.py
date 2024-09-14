import numpy
from numba import jit


def exchange_interaction_field(
    state,
    magnitude_spin_moment,
    exchanges,
    neighbors,
):
    return (exchanges.reshape(tuple((*exchanges.shape, 1))) * state[neighbors]).sum(
        axis=1
    ) / magnitude_spin_moment.reshape(tuple((*magnitude_spin_moment.shape, 1)))


@jit(nopython=True)
def anisotropy_interaction_field(
    state,
    magnitude_spin_moment,
    anisotropy_constants,
    anisotropy_vectors,
):
    values = (
        anisotropy_constants
        * (state * anisotropy_vectors).sum(axis=1)
        / magnitude_spin_moment
    )
    values_repeated = numpy.repeat(values, 3)
    values_repeated_reshaped = values_repeated.reshape((len(values), 3))
    return 2 * values_repeated_reshaped * anisotropy_vectors
