from llg.functions import energy
import pytest
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


@pytest.mark.repeat(100)
def test_exchange_energy_null_J_exchange(random_state_spins, build_sample):
    num_sites, _, neighbors, _ = build_sample
    exchanges = numpy.zeros(shape=(num_sites, 6))
    neighbors = numpy.array(neighbors).reshape(num_sites, 6)
    expected = 0
    total = energy.compute_exchange_energy(random_state_spins, exchanges, neighbors)
    assert numpy.allclose(expected, total)


@pytest.mark.repeat(100)
def test_exchange__energy_constant_J_exchange(random_state_spins, build_sample):
    num_sites, num_interactions, neighbors, num_neighbors = build_sample
    j_exchange = numpy.full(num_interactions, numpy.random.uniform(-10, 10))
    exchanges = j_exchange.reshape(num_sites, 6)
    neighbors_ = numpy.array(neighbors).reshape(num_sites, 6)
    expected = compute_exchange_energy(
        num_sites, random_state_spins, j_exchange, num_neighbors, neighbors
    )
    total = energy.compute_exchange_energy(random_state_spins, exchanges, neighbors_)
    assert numpy.allclose(expected, total)


@pytest.mark.repeat(100)
def test_exchange_energy_random_J_exchange(
    random_state_spins, build_sample, random_j_exchange
):
    num_sites, _, neighbors, num_neighbors = build_sample
    exchanges = random_j_exchange.reshape(num_sites, 6)
    neighbors_ = numpy.array(neighbors).reshape(num_sites, 6)
    expected = compute_exchange_energy(
        num_sites, random_state_spins, random_j_exchange, num_neighbors, neighbors
    )
    total = energy.compute_exchange_energy(random_state_spins, exchanges, neighbors_)
    assert numpy.allclose(expected, total)
