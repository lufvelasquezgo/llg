import numpy


def compute_exchange_energy(num_sites, state, j_exchange, num_neighbors, neighbors):
    total = 0
    for i in range(num_sites):
        sum_nhbs = sum(num_neighbors[:i])
        for j in range(num_neighbors[i]):
            index = j + sum_nhbs
            j_int = j_exchange[index]
            nhb = neighbors[index]
            total -= j_int * numpy.dot(state[i], state[nhb])
    total = 0.5 * total
    return total


def compute_anisotropy_energy(num_sites, state, anisotropy_constant, anisotropy_vector):
    total = numpy.zeros(shape=(num_sites, 3))
    for i in range(num_sites):
        total -= anisotropy_constant[i] * numpy.dot(state[i], anisotropy_vector[i]) ** 2

    return total


def compute_magnetic_energy(
    num_sites, magnitude_spin_moment, state, intensities, directions
):
    total = 0
    for i in range(num_sites):
        total -= (
            magnitude_spin_moment[i]
            * numpy.dot(state[i], directions[i])
            * intensities[i]
        )
    return total
