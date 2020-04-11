import numpy
import pytest


@pytest.fixture
def random_intensity(num_sites):
    return numpy.random.uniform(-1, 1)


@pytest.fixture
def random_intensities(num_sites):
    return numpy.random.uniform(-1, 1, size=num_sites)


@pytest.fixture
def random_directions(num_sites):
    return numpy.random.uniform(-1, 1, size=(num_sites, 3))


@pytest.fixture
def random_temperature(num_sites):
    return numpy.random.uniform(0, 1, size=num_sites)


@pytest.fixture
def random_magnitude_spin(num_sites):
    return numpy.random.uniform(0, 1, size=num_sites)
