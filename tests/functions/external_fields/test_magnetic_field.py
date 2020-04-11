from llg.functions import external_fields
import pytest
import numpy


def test_magnetic_field_shapes(num_sites, random_intensities, random_directions):
    assert random_intensities.shape == (num_sites,)
    assert random_directions.shape == (num_sites, 3)


@pytest.mark.repeat(100)
def test_magnetic_field_null_intensity(num_sites, random_directions):
    assert numpy.allclose(
        external_fields.magnetic_field(0.0 * random_directions),
        numpy.zeros((num_sites, 3)),
    )


@pytest.mark.repeat(100)
def test_magnetic_field_intensity_1(num_sites, random_directions):
    assert numpy.allclose(
        external_fields.magnetic_field(random_directions), random_directions,
    )


@pytest.mark.repeat(100)
def test_magnetic_field_intensity_constant(
    num_sites, random_intensity, random_directions
):
    assert numpy.allclose(
        external_fields.magnetic_field(random_intensity * random_directions),
        random_intensity * random_directions,
    )


@pytest.mark.repeat(100)
def test_magnetic_field_all_random(num_sites, random_intensities, random_directions):
    magnetic_fields = (
        numpy.array([random_intensities, random_intensities, random_intensities]).T
        * random_directions
    )
    assert numpy.allclose(
        external_fields.magnetic_field(magnetic_fields),
        numpy.repeat(random_intensities, 3).reshape(num_sites, 3) * random_directions,
    )


@pytest.mark.repeat(100)
def test_magnetic_field_null_direction(num_sites, random_intensities):
    assert numpy.allclose(
        external_fields.magnetic_field(numpy.zeros((num_sites, 3))),
        numpy.zeros((num_sites, 3)),
    )


@pytest.mark.repeat(100)
def test_magnetic_field_constant_direction_x(num_sites, random_intensities):
    values = numpy.zeros((num_sites, 3))
    values[:, 0] = random_intensities
    assert numpy.allclose(external_fields.magnetic_field(values), values,)


@pytest.mark.repeat(100)
def test_magnetic_field_constant_direction_y(num_sites, random_intensities):
    values = numpy.zeros((num_sites, 3))
    values[:, 1] = random_intensities
    assert numpy.allclose(external_fields.magnetic_field(values), values,)


@pytest.mark.repeat(100)
def test_magnetic_field_constant_direction_z(num_sites, random_intensities):
    values = numpy.zeros((num_sites, 3))
    values[:, 2] = random_intensities
    assert numpy.allclose(external_fields.magnetic_field(values), values,)
