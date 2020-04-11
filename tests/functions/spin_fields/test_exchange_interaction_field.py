from llg.functions import spin_fields
import numpy
import pytest


def compute_exchange_field(
    num_sites, state, j_exchange, spin_moments, num_neighbors, neighbors
):
    total = numpy.zeros(shape=(num_sites, 3))
    for i in range(num_sites):
        sum_nhbs = sum(num_neighbors[:i])
        for j in range(num_neighbors[i]):
            index = j + sum_nhbs
            j_int = j_exchange[index]
            nhb = neighbors[index]
            total[i] += j_int * state[nhb]
    total /= spin_moments[:, numpy.newaxis]
    return total


@pytest.mark.repeat(100)
def test_exchange_interaction_field_null_J_exchange(random_state_spins, build_sample):
    num_sites, num_interactions, neighbors, num_neighbors = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    j_exchange = numpy.zeros(shape=num_interactions)
    exchanges = j_exchange.reshape(num_sites, 6)
    neighbors_ = numpy.array(neighbors).reshape(num_sites, 6)
    expected = numpy.zeros(shape=(num_sites, 3))
    total = spin_fields.exchange_interaction_field(
        random_state_spins, spin_moments, exchanges, neighbors_
    )
    assert numpy.allclose(expected, total)


@pytest.mark.repeat(100)
def test_exchange_interaction_field_constant_J_exchange(
    random_state_spins, build_sample
):
    num_sites, num_interactions, neighbors, num_neighbors = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    j_exchange = numpy.full(num_interactions, numpy.random.uniform(-10, 10))
    exchanges = j_exchange.reshape(num_sites, 6)
    neighbors_ = numpy.array(neighbors).reshape(num_sites, 6)
    expected = compute_exchange_field(
        num_sites,
        random_state_spins,
        j_exchange,
        spin_moments,
        num_neighbors,
        neighbors,
    )
    assert numpy.allclose(
        spin_fields.exchange_interaction_field(
            random_state_spins, spin_moments, exchanges, neighbors_
        ),
        expected,
    )


@pytest.mark.repeat(100)
def test_exchange_interaction_field_random_J_exchange(
    random_state_spins, build_sample, random_j_exchange
):
    num_sites, _, neighbors, num_neighbors = build_sample
    exchanges = random_j_exchange.reshape(num_sites, 6)
    neighbors_ = numpy.array(neighbors).reshape(num_sites, 6)
    spin_moments = numpy.ones(shape=num_sites)
    expected = compute_exchange_field(
        num_sites,
        random_state_spins,
        random_j_exchange,
        spin_moments,
        num_neighbors,
        neighbors,
    )
    assert numpy.allclose(
        spin_fields.exchange_interaction_field(
            random_state_spins, spin_moments, exchanges, neighbors_,
        ),
        expected,
    )


@pytest.mark.repeat(100)
def test_exchange_interaction_field_random_spin_moments(
    random_state_spins, build_sample, random_spin_moments, random_j_exchange
):
    num_sites, _, neighbors, num_neighbors = build_sample
    exchanges = random_j_exchange.reshape(num_sites, 6)
    neighbors_ = numpy.array(neighbors).reshape(num_sites, 6)
    expected = compute_exchange_field(
        num_sites,
        random_state_spins,
        random_j_exchange,
        random_spin_moments,
        num_neighbors,
        neighbors,
    )
    assert numpy.allclose(
        spin_fields.exchange_interaction_field(
            random_state_spins, random_spin_moments, exchanges, neighbors_,
        ),
        expected,
    )


@pytest.mark.repeat(100)
def test_exchange_interaction_field_null_magnetic_moments(
    random_state_spins, build_sample, random_j_exchange
):
    num_sites, _, neighbors, _ = build_sample
    exchanges = random_j_exchange.reshape(num_sites, 6)
    neighbors_ = numpy.array(neighbors).reshape(num_sites, 6)
    null_moments = numpy.array([0.0] * num_sites)
    expected = numpy.full((num_sites, 3), numpy.inf)
    total = numpy.abs(
        spin_fields.exchange_interaction_field(
            random_state_spins, null_moments, exchanges, neighbors_
        )
    )
    assert numpy.allclose(total, expected)
