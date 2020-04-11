from llg.functions import energy
import pytest
import numpy


def compute_anisotropy_energy(num_sites, state, anisotropy_constant, anisotropy_vector):
    total = 0
    for i in range(num_sites):
        total -= anisotropy_constant[i] * numpy.dot(state[i], anisotropy_vector[i]) ** 2

    return total


@pytest.mark.repeat(100)
def test_anisotropy_energy_null_anisotropy_constant(
    random_state_spins, build_sample, random_anisotropy_vector
):
    num_sites, _, _, _ = build_sample
    anisotropy_constant = numpy.zeros(shape=num_sites)
    expected = compute_anisotropy_energy(
        num_sites, random_state_spins, anisotropy_constant, random_anisotropy_vector
    )
    total = energy.compute_anisotropy_energy(
        random_state_spins, anisotropy_constant, random_anisotropy_vector
    )
    assert numpy.allclose(expected, total)


@pytest.mark.repeat(100)
def test_anisotropy_energy_null_anisotropy_vector(
    random_state_spins, build_sample, random_anisotropy_constant
):
    num_sites, _, _, _ = build_sample
    anisotropy_vector = numpy.zeros(shape=(num_sites, 3))
    expected = compute_anisotropy_energy(
        num_sites, random_state_spins, random_anisotropy_constant, anisotropy_vector
    )
    total = energy.compute_anisotropy_energy(
        random_state_spins, random_anisotropy_constant, anisotropy_vector
    )
    assert numpy.allclose(expected, total)


@pytest.mark.repeat(100)
def test_anisotropy_energy_random_anisotropy_constant(
    random_state_spins, build_sample, random_anisotropy_constant
):
    num_sites, _, _, _ = build_sample
    anisotropy_vector = numpy.ones(shape=(num_sites, 3))
    expected = compute_anisotropy_energy(
        num_sites, random_state_spins, random_anisotropy_constant, anisotropy_vector
    )
    total = energy.compute_anisotropy_energy(
        random_state_spins, random_anisotropy_constant, anisotropy_vector
    )
    assert numpy.allclose(expected, total)


@pytest.mark.repeat(100)
def test_anisotropy_energy_random_anisotropy_vector(
    random_state_spins, build_sample, random_anisotropy_vector
):
    num_sites, _, _, _ = build_sample
    anisotropy_constants = numpy.ones(shape=num_sites)
    expected = compute_anisotropy_energy(
        num_sites, random_state_spins, anisotropy_constants, random_anisotropy_vector
    )
    total = energy.compute_anisotropy_energy(
        random_state_spins, anisotropy_constants, random_anisotropy_vector
    )
    assert numpy.allclose(expected, total)
