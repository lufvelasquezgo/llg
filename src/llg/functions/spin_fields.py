"""
Module for the computation of the spin fields of the LLG equation.
These spin fields are the exchange interaction field and the 
anisotropy interaction field.
"""
import numpy


def exchange_interaction_field(state, magnitude_spin_moment, j_exchange, num_neighbors,
                               neighbors):
    """Computes the exchange interaction field for each site of a given state"""
    state = numpy.array(state)
    magnitude_spin_moment = numpy.array(magnitude_spin_moment)
    j_exchange = numpy.array(j_exchange)
    num_neighbors = numpy.array(num_neighbors)
    neighbors = numpy.array(neighbors)
    num_sites = len(state)
    out = numpy.zeros((num_sites, 3))

    for i in range(num_sites):
        start = sum(num_neighbors[0:i+1]) - num_neighbors[0]
        final = start + num_neighbors[i] - 1

        for j in range(start, final + 1):
            nbh = neighbors[j]
            out[i] += j_exchange[j] * state[nbh]
        out[i] /= magnitude_spin_moment[i]

    return out


def anisotropy_interaction_field(state, magnitude_spin_moment, anisotropy_constant,
                                 anisotropy_vector):
    """Computes the anisotropy interaction field for each site of a given state"""
    state = numpy.array(state)
    magnitude_spin_moment = numpy.array(magnitude_spin_moment)
    anisotropy_constant = numpy.array(anisotropy_constant)
    anisotropy_vector = numpy.array(anisotropy_vector)
    num_sites = len(state)
    out = numpy.zeros((num_sites, 3))

    for i in range(num_sites):
        out[i] = 2 * anisotropy_constant[i] * \
            numpy.dot(state[i], anisotropy_vector[i]) * \
            anisotropy_vector[i] / magnitude_spin_moment[i]

    return out
