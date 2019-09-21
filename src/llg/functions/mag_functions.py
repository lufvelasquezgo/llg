import numpy


def magnetization_vector(state):
    state = numpy.array(state)
    num_sites = len(state)
    return numpy.sum(state, axis=0) / num_sites


def magnetization_vector_by_type(state, num_types, types):
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
    state = numpy.array(state)
    num_sites = len(state)
    mag = magnetization_vector(state)
    return numpy.linalg.norm(mag)


def magnetization_by_type(state, num_types, types):
    state = numpy.array(state)
    types = numpy.array(types)
    num_sites = len(state)
    mag_by_type = magnetization_vector_by_type(state, num_types, types)
    out = numpy.zeros(shape=(num_types, 3))

    for i in range(num_types):
        out[i] = numpy.linalg.norm(mag_by_type[i])

    return out
