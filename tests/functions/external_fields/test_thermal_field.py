from llg.functions import external_fields
import numpy
import pytest


@pytest.mark.repeat(100)
def test_thermal_field_null_temperature(num_sites):
    assert numpy.allclose(
        external_fields.thermal_field(
            numpy.array([0] * num_sites),
            numpy.array([1] * num_sites),
            1.0,
            1.0,
            1.0,
            1.0,
        ),
        numpy.zeros((num_sites, 3)),
    )


@pytest.mark.repeat(100)
def test_thermal_field_zero_denominator(num_sites):
    with pytest.warns(RuntimeWarning):
        assert numpy.all(
            numpy.isinf(
                external_fields.thermal_field(
                    numpy.array([1] * num_sites),
                    numpy.array([0] * num_sites),
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                )
            )
        )

        assert numpy.all(
            numpy.isinf(
                external_fields.thermal_field(
                    numpy.array([1] * num_sites),
                    numpy.array([1] * num_sites),
                    1.0,
                    0.0,
                    1.0,
                    1.0,
                )
            )
        )

        assert numpy.all(
            numpy.isinf(
                external_fields.thermal_field(
                    numpy.array([1] * num_sites),
                    numpy.array([1] * num_sites),
                    1.0,
                    1.0,
                    0.0,
                    1.0,
                )
            )
        )


@pytest.mark.filterwarnings("ignore:api v1")
@pytest.mark.repeat(100)
def test_thermal_field_invalid_argument_for_square_root(num_sites):
    with pytest.warns(RuntimeWarning):
        assert numpy.all(
            numpy.isnan(
                external_fields.thermal_field(
                    numpy.array([-1] * num_sites),
                    numpy.array([1] * num_sites),
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                )
            )
        )

        assert numpy.all(
            numpy.isnan(
                external_fields.thermal_field(
                    numpy.array([1] * num_sites),
                    numpy.array([-1] * num_sites),
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                )
            )
        )

        assert numpy.all(
            numpy.isnan(
                external_fields.thermal_field(
                    numpy.array([1] * num_sites),
                    numpy.array([1] * num_sites),
                    -1.0,
                    1.0,
                    1.0,
                    1.0,
                )
            )
        )

        assert numpy.all(
            numpy.isnan(
                external_fields.thermal_field(
                    numpy.array([1] * num_sites),
                    numpy.array([1] * num_sites),
                    1.0,
                    -1.0,
                    1.0,
                    1.0,
                )
            )
        )

        assert numpy.all(
            numpy.isnan(
                external_fields.thermal_field(
                    numpy.array([1] * num_sites),
                    numpy.array([1] * num_sites),
                    1.0,
                    1.0,
                    -1.0,
                    1.0,
                )
            )
        )

        assert numpy.all(
            numpy.isnan(
                external_fields.thermal_field(
                    numpy.array([1] * num_sites),
                    numpy.array([1] * num_sites),
                    1.0,
                    1.0,
                    1.0,
                    -1.0,
                )
            )
        )
