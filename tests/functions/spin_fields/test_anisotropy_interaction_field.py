from llg.functions import spin_fields
import pytest
import numpy


def compute_anisotropy_field(
    num_sites, state, magnitude_spin_moment, anisotropy_constant, anisotropy_vector
):
    total = numpy.zeros(shape=(num_sites, 3))
    for i in range(num_sites):
        total[i] += (
            2.0
            * anisotropy_constant[i]
            * numpy.dot(state[i], anisotropy_vector[i])
            * anisotropy_vector[i]
        )

    total /= magnitude_spin_moment[:, numpy.newaxis]

    return total


@pytest.mark.repeat(100)
def test_anisotropy_interaction_field_null_spin_moments(
    random_state_spins,
    build_sample,
    random_anisotropy_constant,
    random_anisotropy_vector,
):
    num_sites, _, _, _ = build_sample
    spin_moments = numpy.zeros(shape=num_sites)
    assert numpy.all(
        numpy.isinf(
            spin_fields.anisotropy_interaction_field(
                random_state_spins,
                spin_moments,
                random_anisotropy_constant,
                random_anisotropy_vector,
            )
        )
    )


@pytest.mark.repeat(100)
def test_anisotropy_interaction_field_null_anisotropy_constant(
    random_state_spins, build_sample, random_anisotropy_vector
):
    num_sites, _, _, _ = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    anisotropy_constant = numpy.zeros(shape=num_sites)
    total = compute_anisotropy_field(
        num_sites,
        random_state_spins,
        spin_moments,
        anisotropy_constant,
        random_anisotropy_vector,
    )
    assert numpy.allclose(
        spin_fields.anisotropy_interaction_field(
            random_state_spins,
            spin_moments,
            anisotropy_constant,
            random_anisotropy_vector,
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_anisotropy_interaction_field_null_anisotropy_vector(
    random_state_spins, build_sample, random_anisotropy_constant
):
    num_sites, _, _, _ = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    anisotropy_vector = numpy.zeros(shape=(num_sites, 3))
    total = compute_anisotropy_field(
        num_sites,
        random_state_spins,
        spin_moments,
        random_anisotropy_constant,
        anisotropy_vector,
    )
    assert numpy.allclose(
        spin_fields.anisotropy_interaction_field(
            random_state_spins,
            spin_moments,
            random_anisotropy_constant,
            anisotropy_vector,
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_anisotropy_interaction_field_random_spin_moments(
    random_state_spins, build_sample, random_spin_moments
):
    num_sites, _, _, _ = build_sample
    anisotropy_constant = numpy.ones(shape=num_sites)
    anisotropy_vector = numpy.ones(shape=(num_sites, 3))
    total = compute_anisotropy_field(
        num_sites,
        random_state_spins,
        random_spin_moments,
        anisotropy_constant,
        anisotropy_vector,
    )
    assert numpy.allclose(
        spin_fields.anisotropy_interaction_field(
            random_state_spins,
            random_spin_moments,
            anisotropy_constant,
            anisotropy_vector,
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_anisotropy_interaction_field_random_anisotropy_constant(
    random_state_spins, build_sample, random_anisotropy_constant
):
    num_sites, _, _, _ = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    anisotropy_vector = numpy.ones(shape=(num_sites, 3))
    total = compute_anisotropy_field(
        num_sites,
        random_state_spins,
        spin_moments,
        random_anisotropy_constant,
        anisotropy_vector,
    )
    assert numpy.allclose(
        spin_fields.anisotropy_interaction_field(
            random_state_spins,
            spin_moments,
            random_anisotropy_constant,
            anisotropy_vector,
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_anisotropy_interaction_field_random_anisotropy_vector(
    random_state_spins, build_sample, random_anisotropy_vector
):
    num_sites, _, _, _ = build_sample
    spin_moments = numpy.ones(shape=num_sites)
    anisotropy_constants = numpy.ones(shape=num_sites)
    total = compute_anisotropy_field(
        num_sites,
        random_state_spins,
        spin_moments,
        anisotropy_constants,
        random_anisotropy_vector,
    )
    assert numpy.allclose(
        spin_fields.anisotropy_interaction_field(
            random_state_spins,
            spin_moments,
            anisotropy_constants,
            random_anisotropy_vector,
        ),
        total,
    )
