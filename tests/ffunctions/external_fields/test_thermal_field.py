from llg.ffunctions import external_fields
import numpy
import pytest


@pytest.mark.repeat(100)
def test_thermal_field_null_matrix(num_sites):
    assert numpy.allclose(
        external_fields.thermal_field(
            numpy.zeros((num_sites, 3)),
            [1] * num_sites, [1] * num_sites, 1.0, 1.0, 1.0, 1.0),
        numpy.zeros((num_sites, 3))
    )


@pytest.mark.repeat(100)
def test_thermal_field_null_temperature(num_sites, random_directions):
    assert numpy.allclose(
        external_fields.thermal_field(
            random_directions, [0] * num_sites, [1] * num_sites, 1.0, 1.0, 1.0, 1.0),
        numpy.zeros((num_sites, 3))
    )


@pytest.mark.repeat(100)
def test_thermal_field_zero_denominator(num_sites, random_directions):
    assert numpy.all(numpy.isinf(
        external_fields.thermal_field(random_directions, [1] * num_sites,
                                      [0] * num_sites, 1.0, 1.0, 1.0, 1.0)
    ))

    assert numpy.all(numpy.isinf(
        external_fields.thermal_field(random_directions, [1] * num_sites,
                                      [1] * num_sites, 1.0, 0.0, 1.0, 1.0)
    ))

    assert numpy.all(numpy.isinf(
        external_fields.thermal_field(random_directions, [1] * num_sites,
                                      [1] * num_sites, 1.0, 1.0, 0.0, 1.0)
    ))


@pytest.mark.repeat(100)
def test_thermal_field_invalid_argument_for_square_root(num_sites, random_directions):
    assert numpy.all(numpy.isnan(
        external_fields.thermal_field(random_directions, [-1] * num_sites,
                                      [1] * num_sites, 1.0, 1.0, 1.0, 1.0
                                      )))

    assert numpy.all(numpy.isnan(
        external_fields.thermal_field(random_directions, [1] * num_sites,
                                      [-1] * num_sites, 1.0, 1.0, 1.0, 1.0
                                      )))

    assert numpy.all(numpy.isnan(
        external_fields.thermal_field(random_directions, [1] * num_sites,
                                      [1] * num_sites, -1.0, 1.0, 1.0, 1.0
                                      )))

    assert numpy.all(numpy.isnan(
        external_fields.thermal_field(random_directions, [1] * num_sites,
                                      [1] * num_sites, 1.0, -1.0, 1.0, 1.0
                                      )))

    assert numpy.all(numpy.isnan(
        external_fields.thermal_field(random_directions, [1] * num_sites,
                                      [1] * num_sites, 1.0, 1.0, -1.0, 1.0
                                      )))

    assert numpy.all(numpy.isnan(
        external_fields.thermal_field(random_directions, [1] * num_sites,
                                      [1] * num_sites, 1.0, 1.0, 1.0, -1.0
                                      )))


@pytest.mark.repeat(100)
def test_thermal_field_ones_matrix(num_sites):
    assert numpy.allclose(
        external_fields.thermal_field(
            numpy.ones((num_sites, 3)), [1] * num_sites,
            [1] * num_sites, 1.0, 1.0, 1.0, 1.0),
        numpy.ones((num_sites, 3)) * numpy.sqrt(2))


@pytest.mark.repeat(100)
def test_thermal_field_random_matrix(num_sites, random_directions):
    mat = random_directions
    assert numpy.allclose(
        external_fields.thermal_field(
            mat, [1] * num_sites,
            [1] * num_sites, 1.0, 1.0, 1.0, 1.0), mat * numpy.sqrt(2))


@pytest.mark.repeat(100)
def test_thermal_field_random_temperature(num_sites, random_temperature):
    tem = random_temperature
    values = numpy.transpose(numpy.transpose(numpy.ones(
        (num_sites, 3))) * numpy.sqrt(2 * tem))

    assert numpy.allclose(
        external_fields.thermal_field(
            numpy.ones((num_sites, 3)), tem,
            [1] * num_sites, 1.0, 1.0, 1.0, 1.0), values)


@pytest.mark.repeat(100)
def test_thermal_field_random_magnitude_spin(num_sites, random_temperature, random_magnitude_spin):
    rms = random_magnitude_spin
    values = numpy.transpose(numpy.transpose(numpy.ones(
        (num_sites, 3))) * numpy.sqrt(2 / rms))

    assert numpy.allclose(
        external_fields.thermal_field(
            numpy.ones((num_sites, 3)), [1] * num_sites,
            rms, 1.0, 1.0, 1.0, 1.0), values)
