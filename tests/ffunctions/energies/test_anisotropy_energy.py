from llg.ffunctions import energy
import pytest
import numpy


def compute_anisotropy_energy(num_sites, state, anisotropy_constant, anisotropy_vector):
    total = numpy.zeros(shape=(num_sites, 3))
    for i in range(num_sites):
        total -= anisotropy_constant[i] * numpy.dot(state[i], anisotropy_vector[i]) ** 2

    return total


@pytest.mark.repeat(100)
def test_anisotropy_interaction_energy_null_anisotropy_constant(
    random_state_spins, build_sample, random_anisotropy_vector
):
    num_sites, _, _, _ = build_sample
    anisotropy_constant = numpy.zeros(shape=num_sites)
    total = compute_anisotropy_energy(
        num_sites, random_state_spins, anisotropy_constant, random_anisotropy_vector
    )
    assert numpy.allclose(
        energy.anisotropy_energy(
            random_state_spins, anisotropy_constant, random_anisotropy_vector
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_anisotropy_interaction_field_null_anisotropy_vector(
    random_state_spins, build_sample, random_anisotropy_constant
):
    num_sites, _, _, _ = build_sample
    anisotropy_vector = numpy.zeros(shape=(num_sites, 3))
    total = compute_anisotropy_energy(
        num_sites, random_state_spins, random_anisotropy_constant, anisotropy_vector
    )
    assert numpy.allclose(
        spin_fields.anisotropy_interaction_field(
            random_state_spins, random_anisotropy_constant, anisotropy_vector
        ),
        total,
    )
