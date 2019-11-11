from llg.ffunctions import energy
import pytest
import numpy


def compute_magnetic_energy(
    num_sites, magnitude_spin_moment, state, intensities, directions
):
    total = 0
    for i in range(num_sites):
        total -= (
            magnitude_spin_moment[i]
            * numpy.dot(state[i], directions[i])
            * intensities[i]
        )
    return total


@pytest.mark.repeat(100)
def test_magnetic_energy_null_intensity(random_spin_moments, random_state_spins):
    num_sites = len(random_spin_moments)
    intensities = [0.0] * num_sites
    directions = numpy.ones(shape=(num_sites, 3))
    total = compute_magnetic_energy(
        num_sites, random_spin_moments, random_state_spins, intensities, directions
    )

    assert numpy.allclose(
        energy.magnetic_energy(
            random_spin_moments, random_state_spins, intensities, directions
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_magnetic_energy_random_intensity(random_spin_moments, random_state_spins):
    num_sites = len(random_spin_moments)
    random_intensities = numpy.random.normal(size=(num_sites))
    directions = numpy.ones(shape=(num_sites, 3))
    total = compute_magnetic_energy(
        num_sites,
        random_spin_moments,
        random_state_spins,
        random_intensities,
        directions,
    )

    assert numpy.allclose(
        energy.magnetic_energy(
            random_spin_moments, random_state_spins, random_intensities, directions
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_magnetic_energy_null_directions(random_spin_moments, random_state_spins):
    num_sites = len(random_spin_moments)
    intensities = [1.0] * num_sites
    directions = numpy.zeros(shape=(num_sites, 3))
    total = compute_magnetic_energy(
        num_sites, random_spin_moments, random_state_spins, intensities, directions
    )

    assert numpy.allclose(
        energy.magnetic_energy(
            random_spin_moments, random_state_spins, intensities, directions
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_magnetic_energy_random_directions(random_spin_moments, random_state_spins):
    num_sites = len(random_spin_moments)
    intensities = [1.0] * num_sites
    random_directions = numpy.random.normal(size=(num_sites, 3))
    total = compute_magnetic_energy(
        num_sites,
        random_spin_moments,
        random_state_spins,
        intensities,
        random_directions,
    )

    assert numpy.allclose(
        energy.magnetic_energy(
            random_spin_moments, random_state_spins, intensities, random_directions
        ),
        total,
    )


@pytest.mark.repeat(100)
def test_magnetic_energy_all_random(random_spin_moments, random_state_spins):
    num_sites = len(random_spin_moments)
    random_intensities = numpy.random.normal(size=(num_sites))
    random_directions = numpy.random.normal(size=(num_sites, 3))
    total = compute_magnetic_energy(
        num_sites,
        random_spin_moments,
        random_state_spins,
        random_intensities,
        random_directions,
    )

    assert numpy.allclose(
        energy.magnetic_energy(
            random_spin_moments,
            random_state_spins,
            random_intensities,
            random_directions,
        ),
        total,
    )


# @pytest.mark.repeat()
# def test_magnetic_energy_constant_direction_x(random_spin_moments, random_state_spins):
#     num_sites = len(random_spin_moments)
#     random_intensities = numpy.random.normal(size=(num_sites))
#     directions = [[1.0, 0.0, 0.0]] * num_sites
#     total = compute_magnetic_energy(
#         num_sites,
#         random_spin_moments,
#         random_state_spins,
#         random_intensities,
#         directions,
#     )

#     assert numpy.allclose(
#         energy.magnetic_energy(
#             random_spin_moments, random_state_spins, random_intensities, directions
#         ),
#         total,
#     )
