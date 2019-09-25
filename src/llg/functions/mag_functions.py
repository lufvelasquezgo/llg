"""Module for the computation of the magnetization"""
import numpy


def magnetization_vector(state):
    """Computes the net magnetization vector of a given state"""
    state = numpy.array(state)
    num_sites = len(state)
    return numpy.sum(state, axis=0) / num_sites


def magnetization_vector_by_type(state, num_types, types):
    """Computes the net magnetization vector for each ion type"""
    state = numpy.array(state)
    types = numpy.array(types)
    num_sites = len(state)
    out = numpy.zeros(shape=(num_types, 3))
    for i in range(num_sites):
        out[types[i]] += state[i]

    for i in range(num_types):
        out[i] /= len(numpy.where(types == i)[0])

    return out


def total_magnetization(state):
    """Computes the norm of the magnetization vector of a given state"""
    state = numpy.array(state)
    mag = magnetization_vector(state)
    return numpy.linalg.norm(mag)


def magnetization_by_type(state, num_types, types):
    """Computes the norm of the magnetization vector for the state
    of each ion type"""
    state = numpy.array(state)
    types = numpy.array(types)
    mag_by_type = magnetization_vector_by_type(state, num_types, types)
    out = numpy.zeros(shape=(num_types, 3))

    for i in range(num_types):
        out[i] = numpy.linalg.norm(mag_by_type[i])

    return out
