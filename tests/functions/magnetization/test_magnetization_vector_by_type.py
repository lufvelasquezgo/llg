#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ffortran/functions` package."""

import numpy
import pytest
from llg.functions import magnetization


@pytest.mark.repeat(100)
def test_magnetization_vector_by_type_random_state(
    num_sites, random_num_types, random_state
):
    assert random_num_types <= num_sites

    types = numpy.random.randint(0, random_num_types, size=num_sites)
    assert sorted(numpy.unique(types)) == list(range(0, random_num_types))

    magnetization_vector_by_type = magnetization.magnetization_vector_by_type(
        random_state, random_num_types, types
    )

    assert len(magnetization_vector_by_type) == random_num_types
    assert magnetization_vector_by_type.shape == (random_num_types, 3)

    values = [
        numpy.sum(random_state[types == t], axis=0) / (types == t).sum()
        for t in range(random_num_types)
    ]

    assert numpy.allclose(magnetization_vector_by_type, values)


def test_magnetization_vector_by_type_AFM_state_x(num_sites):
    state = numpy.array([[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]] * (num_sites // 2))
    types = numpy.array([0, 1] * (num_sites // 2))

    magnetization_vector_by_type = magnetization.magnetization_vector_by_type(
        state, 2, types
    )

    assert numpy.allclose(
        magnetization_vector_by_type, [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]]
    )


def test_magnetization_vector_by_type_AFM_state_y(num_sites):
    state = numpy.array([[0.0, 1.0, 0.0], [0.0, -1.0, 0.0]] * (num_sites // 2))
    types = numpy.array([0, 1] * (num_sites // 2))

    magnetization_vector_by_type = magnetization.magnetization_vector_by_type(
        state, 2, types
    )

    assert numpy.allclose(
        magnetization_vector_by_type, [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0]]
    )


def test_magnetization_vector_by_type_AFM_state_z(num_sites):
    state = numpy.array([[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]] * (num_sites // 2))
    types = numpy.array([0, 1] * (num_sites // 2))

    magnetization_vector_by_type = magnetization.magnetization_vector_by_type(
        state, 2, types
    )

    assert numpy.allclose(
        magnetization_vector_by_type, [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]]
    )
