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


@pytest.mark.repeat(1)
def test_magnetic_energy_null_intensity(
    num_sites, random_spin_moments, random_state_spins, random_directions, build_sample
):
    num_sites, _, _, _ = build_sample
    intensities = [0.0] * num_sites
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


# num_sites, magnitude_spin_moment, state, intensities, directions
