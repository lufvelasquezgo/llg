import numpy
import pytest
from itertools import product
from collections import defaultdict


@pytest.fixture
def length():
    return numpy.random.randint(3, 10)


@pytest.fixture
def build_sample(length):
    sites = list()
    index = dict()
    for x, y, z in product(range(length), repeat=3):
        site = x, y, z
        sites.append(site)
        index[site] = sites.index(site)

    num_sites = len(sites)
    neigh = defaultdict(list)

    for site in sites:
        x, y, z = site
        neigh[site].append(sites.index(((x + 1) % length, y, z)))
        neigh[site].append(sites.index(((x - 1) % length, y, z)))
        neigh[site].append(sites.index((x, (y + 1) % length, z)))
        neigh[site].append(sites.index((x, (y - 1) % length, z)))
        neigh[site].append(sites.index((x, y, (z + 1) % length)))
        neigh[site].append(sites.index((x, y, (z - 1) % length)))

    neighbors = list()
    num_neighbors = list()
    for neighs in neigh.values():
        neighbors += neighs
        num_neighbors.append(len(neighs))

    num_interactions = len(neighbors)
    return num_sites, num_interactions, neighbors, num_neighbors


@pytest.fixture
def random_state_spins(build_sample):
    num_sites_spins, _, _, _ = build_sample
    state = numpy.random.normal(size=(num_sites_spins, 3))
    norms = numpy.linalg.norm(state, axis=1)
    state = state / numpy.repeat(norms, 3).reshape(num_sites_spins, 3)
    norms = numpy.linalg.norm(state, axis=1)
    assert numpy.allclose(norms, numpy.ones_like(norms))
    return state


@pytest.fixture
def random_j_exchange(build_sample):
    _, num_interactions, _, _ = build_sample
    return numpy.random.uniform(-1, 1, size=(num_interactions))

@pytest.fixture
def random_spin_moments(build_sample):
    num_sites, _, _, _ = build_sample
    return numpy.random.uniform(0, 1, size=num_sites)
