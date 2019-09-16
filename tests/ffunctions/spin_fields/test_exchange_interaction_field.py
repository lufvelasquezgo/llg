from llg.ffunctions import spin_fields
import numpy
import pytest


def compute_exchange_field(num_sites, state, j_exchange, spin_moments, num_neighbors, neighbors):
    total = numpy.zeros(shape=(num_sites, 3))
    for i in range(num_sites):
        sum_nhbs = sum(num_neighbors[:i])
        for j in range(num_neighbors[i]):
            index = j + sum_nhbs
            j_int = j_exchange[index]
            nhb = neighbors[index]
            total[i] -= j_int * state[nhb]
    total /= spin_moments[:, numpy.newaxis]
    return total


@pytest.mark.repeat(100)
def test_exchange_interaction_field_null_J_exchange(random_state_spins, build_sample):
    num_sites, num_interactions, neighbors, num_neighbors = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    j_exchange = numpy.zeros(shape=num_interactions)
    total = numpy.zeros(shape=(num_sites, 3))
    assert numpy.allclose(spin_fields.exchange_interaction_field(
        random_state_spins, spin_moments, j_exchange, num_neighbors, neighbors), total)


@pytest.mark.repeat(100)
def test_exchange_interaction_field_constant_J_exchange(random_state_spins, build_sample):
    num_sites, num_interactions, neighbors, num_neighbors = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    j_exchange = numpy.full(num_interactions, numpy.random.uniform(-10, 10))
    total = compute_exchange_field(
        num_sites, random_state_spins, j_exchange, spin_moments, num_neighbors, neighbors)
    assert numpy.allclose(spin_fields.exchange_interaction_field(
        random_state_spins, spin_moments, j_exchange, num_neighbors, neighbors), total)


@pytest.mark.repeat(100)
def test_exchange_interaction_field_random_J_exchange(random_state_spins, build_sample, random_j_exchange):
    num_sites, _, neighbors, num_neighbors = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    total = compute_exchange_field(
        num_sites, random_state_spins, random_j_exchange, spin_moments, num_neighbors, neighbors)
    assert numpy.allclose(spin_fields.exchange_interaction_field(
        random_state_spins, spin_moments, random_j_exchange, num_neighbors, neighbors), total)


@pytest.mark.repeat(100)
def test_exchange_interaction_field_random_spin_moments(random_state_spins, build_sample, random_spin_moments, random_j_exchange):
    num_sites, _, neighbors, num_neighbors = build_sample
    total = compute_exchange_field(
        num_sites, random_state_spins, random_j_exchange, random_spin_moments, num_neighbors, neighbors)
    assert numpy.allclose(spin_fields.exchange_interaction_field(
        random_state_spins, random_spin_moments, random_j_exchange, num_neighbors, neighbors), total)


@pytest.mark.repeat(100)
def test_exchange_interaction_field_null_magnetic_moments(random_state_spins, build_sample, random_j_exchange):
    num_sites, _, neighbors, num_neighbors = build_sample
    null_moments = [0.0] * num_sites
    total = numpy.full((num_sites, 3), numpy.inf)
    assert(numpy.allclose(
        numpy.abs(
            spin_fields.exchange_interaction_field(
                random_state_spins, null_moments, random_j_exchange, num_neighbors, neighbors
            )
        ),
        total
    ))


@pytest.mark.repeat(100)
def test_exchange_interaction_field_null_interactions(random_state_spins, build_sample):
    num_sites, _, _, _ = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    j_exchange = []
    num_neighbors = numpy.zeros(shape=num_sites, dtype=int)
    neighbors = []
    total = numpy.zeros(shape=(num_sites, 3))
    assert numpy.allclose(spin_fields.exchange_interaction_field(
        random_state_spins, spin_moments, j_exchange, num_neighbors, neighbors), total)
