import numpy
import pytest


@pytest.fixture
def num_sites():
    N = numpy.random.randint(100, 500) * 2
    assert N % 2 == 0
    return N


@pytest.fixture
def random_num_types():
    return numpy.random.randint(1, 10)


@pytest.fixture
def random_state(num_sites):
    state = numpy.random.normal(size=(num_sites, 3))
    norms = numpy.linalg.norm(state, axis=1)
    state = state / numpy.repeat(norms, 3).reshape(num_sites, 3)
    norms = numpy.linalg.norm(state, axis=1)
    assert numpy.allclose(norms, numpy.ones_like(norms))
    return state
