from llg.ffunctions import energy
import pytest
import numpy


def compute_exchange_energy(num_sites, state, j_exchange, num_neighbors, neighbors):
    total = numpy.zeros(shape=(num_sites, 3))
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
def test_exchange_energy__null_J_exchange(random_state_spins, build_sample):
    num_sites, num_interactions, neighbors, num_neighbors = build_sample
    j_exchange = numpy.zeros(shape=num_interactions)
    total = numpy.zeros(shape=(num_sites, 3))
    assert numpy.allclose(
        energy.exchange_energy(
            random_state_spins, j_exchange, num_neighbors, neighbors
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_exchange__energy_constant_J_exchange(random_state_spins, build_sample):
    num_sites, num_interactions, neighbors, num_neighbors = build_sample
    j_exchange = numpy.full(num_interactions, numpy.random.uniform(-10, 10))
    total = compute_exchange_energy(
        num_sites, random_state_spins, j_exchange, num_neighbors, neighbors
    )
    assert numpy.allclose(
        energy.exchange_energy(
            random_state_spins, j_exchange, num_neighbors, neighbors
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_exchange_energy_random_J_exchange(
    random_state_spins, build_sample, random_j_exchange
):
    num_sites, _, neighbors, num_neighbors = build_sample
    total = compute_exchange_energy(
        num_sites, random_state_spins, random_j_exchange, num_neighbors, neighbors
    )
    assert numpy.allclose(
        energy.exchange_energy(
            random_state_spins, random_j_exchange, num_neighbors, neighbors
        ),
        total,
    )


# @pytest.mark.repeat(1)
# def test_exchange_energy_null_interactions(random_state_spins, build_sample):
#     num_sites, _, _, _ = build_sample
#     j_exchange = []
#     num_neighbors = numpy.zeros(shape=num_sites, dtype=int)
#     neighbors = []
#     total = numpy.zeros(shape=(num_sites, 3))
#     assert numpy.allclose(
#         energy.exchange_energy(
#             random_state_spins, j_exchange, num_neighbors, neighbors
#         ),
#         total,
#     )
