from llg.ffunctions import spin_fields
import numpy
import pytest


@pytest.mark.repeat(100)
def test_exchange_interaction_field_null_J_exchange(random_state_spins, build_sample):
    num_sites, num_interactions, neighbors_indexes, num_neighbors = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    j_exchange = [0.0] * num_interactions
    total = numpy.zeros(shape=(num_sites, 3))
    for i in range(num_sites):
        nhbs_i = num_neighbors[i]
        for j in range(nhbs_i):
            j_int = j_exchange[j + sum(num_neighbors[:i])]
            nhb_index = neighbors_indexes[j + sum(num_neighbors[:i])]
            total[i] -= j_int * random_state_spins[nhb_index]
    total /= spin_moments[:, numpy.newaxis]
    assert numpy.allclose(spin_fields.exchange_interaction_field(
        random_state_spins, spin_moments, j_exchange, num_neighbors, neighbors_indexes), total)


@pytest.mark.repeat(100)
def test_exchange_interaction_field_random_J_exchange(random_state_spins, build_sample, random_j_exchange):
    num_sites, _, neighbors_indexes, num_neighbors = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    total = numpy.zeros(shape=(num_sites, 3))
    for i in range(num_sites):
        nhbs_i = num_neighbors[i]
        for j in range(nhbs_i):
            j_int = random_j_exchange[j + sum(num_neighbors[:i])]
            nhb_index = neighbors_indexes[j + sum(num_neighbors[:i])]
            total[i] -= j_int * random_state_spins[nhb_index]
        total[i] /= spin_moments[i]
    assert numpy.allclose(spin_fields.exchange_interaction_field(
        random_state_spins, spin_moments, random_j_exchange, num_neighbors, neighbors_indexes), total)


@pytest.mark.repeat(100)
def test_exchange_interaction_field_random_spin_moments(random_state_spins, build_sample, random_spin_moments):
    num_sites, num_interactions, neighbors_indexes, num_neighbors = build_sample
    j_exchange = [1.0] * num_interactions
    total = numpy.zeros(shape=(num_sites, 3))
    for i in range(num_sites):
        nhbs_i = num_neighbors[i]
        for j in range(nhbs_i):
            j_int = j_exchange[j + sum(num_neighbors[:i])]
            nhb_index = neighbors_indexes[j + sum(num_neighbors[:i])]
            total[i] -= j_int * random_state_spins[nhb_index]
        total[i] /= random_spin_moments[i]
    assert numpy.allclose(spin_fields.exchange_interaction_field(
        random_state_spins, random_spin_moments, j_exchange, num_neighbors, neighbors_indexes), total)


@pytest.mark.repeat(100)
def test_exchange_interaction_field_without_neighbors(random_state_spins, build_sample, random_j_exchange):
    num_sites, num_interactions, _, _ = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    total = numpy.zeros(shape=(num_sites, 3))
    num_neighbors = [0] * num_sites
    neighbors = [-1] * num_interactions
    for i in range(num_sites):
        nhbs_i = num_neighbors[i]
        for j in range(nhbs_i):
            j_int = random_j_exchange[j + sum(num_neighbors[:i])]
            nhb_index = neighbors[j + sum(num_neighbors[:i])]
            if nhb_index >= 0:
                total[i] -= j_int * random_state_spins[nhb_index]
        total[i] /= spin_moments[i]
    assert numpy.allclose(spin_fields.exchange_interaction_field(
        random_state_spins, spin_moments, random_j_exchange, num_neighbors, neighbors), total)


