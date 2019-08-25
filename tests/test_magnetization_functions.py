#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ffortran/functions` package."""

from llg import ffunctions
import numpy
import pytest
from pytest_fixtures import *
from llg.ffunctions import mag_functions


@pytest.mark.repeat(100)
def test_total_magnetization_random_state(num_sites, random_state):
    assert numpy.allclose(
        mag_functions.total_magnetization(random_state),
        numpy.linalg.norm(numpy.sum(random_state, axis=0) / num_sites)
    )


def test_total_magnetization_FM_state_x_up(num_sites):
    state = [[1.0, 0.0, 0.0]] * num_sites
    assert numpy.allclose(
        mag_functions.total_magnetization(state),
        1.0
    )


def test_total_magnetization_FM_state_x_down(num_sites):
    state = [[-1.0, 0.0, 0.0]] * num_sites
    assert numpy.allclose(
        mag_functions.total_magnetization(state),
        1.0
    )


def test_total_magnetization_FM_state_y_up(num_sites):
    state = [[0.0, 1.0, 0.0]] * num_sites
    assert numpy.allclose(
        mag_functions.total_magnetization(state),
        1.0
    )


def test_total_magnetization_FM_state_y_down(num_sites):
    state = [[0.0, -1.0, 0.0]] * num_sites
    assert numpy.allclose(
        mag_functions.total_magnetization(state),
        1.0
    )


def test_total_magnetization_FM_state_z_up(num_sites):
    state = [[0.0, 0.0, 1.0]] * num_sites
    assert numpy.allclose(
        mag_functions.total_magnetization(state),
        1.0
    )


def test_total_magnetization_FM_state_z_down(num_sites):
    state = [[0.0, 0.0, -1.0]] * num_sites
    assert numpy.allclose(
        mag_functions.total_magnetization(state),
        1.0
    )


def test_total_magnetization_AFM_state_x(num_sites):
    state = [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]] * (num_sites // 2)
    assert numpy.allclose(
        mag_functions.total_magnetization(state),
        0.0
    )


def test_total_magnetization_AFM_state_y(num_sites):
    state = [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0]] * (num_sites // 2)
    assert numpy.allclose(
        mag_functions.total_magnetization(state),
        0.0
    )


def test_total_magnetization_AFM_state_z(num_sites):
    state = [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]] * (num_sites // 2)
    assert numpy.allclose(
        mag_functions.total_magnetization(state),
        0.0
    )


@pytest.mark.repeat(100)
def test_magnetization_by_type_random_state(num_sites, random_num_types, random_state):
    assert random_num_types <= num_sites

    types = numpy.random.randint(0, random_num_types, size=num_sites)
    assert sorted(numpy.unique(types)) == list(range(0, random_num_types))

    magnetization_by_type = mag_functions.magnetization_by_type(
        random_state, random_num_types, types)

    assert len(magnetization_by_type) == random_num_types

    values = [numpy.linalg.norm(numpy.sum(random_state[types == t], axis=0) / (types == t).sum())
              for t in range(random_num_types)]

    assert numpy.allclose(magnetization_by_type, values)


def test_magnetization_by_type_AFM_state_x(num_sites):
    state = [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]] * (num_sites // 2)
    types = [0, 1] * (num_sites // 2)

    magnetization_by_type = mag_functions.magnetization_by_type(
        state, 2, types)

    assert numpy.allclose(magnetization_by_type, [1.0, 1.0])


def test_magnetization_by_type_AFM_state_y(num_sites):
    state = [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0]] * (num_sites // 2)
    types = [0, 1] * (num_sites // 2)

    magnetization_by_type = mag_functions.magnetization_by_type(
        state, 2, types)

    assert numpy.allclose(magnetization_by_type, [1.0, 1.0])


def test_magnetization_by_type_AFM_state_z(num_sites):
    state = [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]] * (num_sites // 2)
    types = [0, 1] * (num_sites // 2)

    magnetization_by_type = mag_functions.magnetization_by_type(
        state, 2, types)

    assert numpy.allclose(magnetization_by_type, [1.0, 1.0])


@pytest.mark.repeat(100)
def test_magnetization_vector_random_state(num_sites, random_state):
    assert numpy.allclose(
        mag_functions.magnetization_vector(random_state),
        numpy.sum(random_state, axis=0) / num_sites
    )


def test_magnetization_vector_FM_state_x_up(num_sites):
    state = [[1.0, 0.0, 0.0]] * num_sites
    assert numpy.allclose(
        mag_functions.magnetization_vector(state),
        [1.0, 0.0, 0.0]
    )


def test_magnetization_vector_FM_state_x_down(num_sites):
    state = [[-1.0, 0.0, 0.0]] * num_sites
    assert numpy.allclose(
        mag_functions.magnetization_vector(state),
        [-1.0, 0.0, 0.0]
    )


def test_magnetization_vector_FM_state_y_up(num_sites):
    state = [[0.0, 1.0, 0.0]] * num_sites
    assert numpy.allclose(
        mag_functions.magnetization_vector(state),
        [0.0, 1.0, 0.0]
    )


def test_magnetization_vector_FM_state_y_down(num_sites):
    state = [[0.0, -1.0, 0.0]] * num_sites
    assert numpy.allclose(
        mag_functions.magnetization_vector(state),
        [0.0, -1.0, 0.0]
    )


def test_magnetization_vector_FM_state_z_up(num_sites):
    state = [[0.0, 0.0, 1.0]] * num_sites
    assert numpy.allclose(
        mag_functions.magnetization_vector(state),
        [0.0, 0.0, 1.0]
    )


def test_magnetization_vector_FM_state_z_down(num_sites):
    state = [[0.0, 0.0, -1.0]] * num_sites
    assert numpy.allclose(
        mag_functions.magnetization_vector(state),
        [0.0, 0.0, -1.0]
    )


def test_magnetization_vector_AFM_state_x(num_sites):
    state = [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]] * (num_sites // 2)
    assert numpy.allclose(
        mag_functions.magnetization_vector(state),
        [0.0, 0.0, 0.0]
    )


def test_magnetization_vector_AFM_state_y(num_sites):
    state = [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0]] * (num_sites // 2)
    assert numpy.allclose(
        mag_functions.magnetization_vector(state),
        [0.0, 0.0, 0.0]
    )


def test_magnetization_vector_AFM_state_z(num_sites):
    state = [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]] * (num_sites // 2)
    assert numpy.allclose(
        mag_functions.magnetization_vector(state),
        [0.0, 0.0, 0.0]
    )


@pytest.mark.repeat(100)
def test_magnetization_vector_by_type_random_state(num_sites, random_num_types, random_state):
    assert random_num_types <= num_sites

    types = numpy.random.randint(0, random_num_types, size=num_sites)
    assert sorted(numpy.unique(types)) == list(range(0, random_num_types))

    magnetization_vector_by_type = mag_functions.magnetization_vector_by_type(
        random_state, random_num_types, types)

    assert len(magnetization_vector_by_type) == random_num_types
    assert magnetization_vector_by_type.shape == (random_num_types, 3)

    values = [numpy.sum(random_state[types == t], axis=0) / (types == t).sum()
              for t in range(random_num_types)]

    assert numpy.allclose(magnetization_vector_by_type, values)


def test_magnetization_vector_by_type_AFM_state_x(num_sites):
    state = [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]] * (num_sites // 2)
    types = [0, 1] * (num_sites // 2)

    magnetization_vector_by_type = mag_functions.magnetization_vector_by_type(
        state, 2, types)

    assert numpy.allclose(magnetization_vector_by_type,
                          [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]])


def test_magnetization_vector_by_type_AFM_state_y(num_sites):
    state = [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0]] * (num_sites // 2)
    types = [0, 1] * (num_sites // 2)

    magnetization_vector_by_type = mag_functions.magnetization_vector_by_type(
        state, 2, types)

    assert numpy.allclose(magnetization_vector_by_type,
                          [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0]])


def test_magnetization_vector_by_type_AFM_state_z(num_sites):
    state = [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]] * (num_sites // 2)
    types = [0, 1] * (num_sites // 2)

    magnetization_vector_by_type = mag_functions.magnetization_vector_by_type(
        state, 2, types)

    assert numpy.allclose(magnetization_vector_by_type,
                          [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]])
