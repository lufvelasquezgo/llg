#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ffortran/functions` package."""

from llg import ffunctions
import numpy
import pytest


@pytest.fixture
def num_sites():
    N = 1000
    assert N % 2 == 0
    return N


@pytest.fixture
def random_num_types():
    return numpy.random.randint(1, 5)


@pytest.fixture
def random_state(num_sites):
    state = numpy.random.normal(size=(num_sites, 3))
    norms = numpy.linalg.norm(state, axis=1)
    state = state / numpy.repeat(norms, 3).reshape(num_sites, 3)
    norms = numpy.linalg.norm(state, axis=1)
    assert numpy.allclose(norms, numpy.ones_like(norms))
    return state


@pytest.mark.repeat(100)
def test_total_magnetization_random_state(num_sites, random_state):
    assert numpy.allclose(
        ffunctions.mag_functions.total_magnetization(random_state),
        numpy.linalg.norm(numpy.sum(random_state, axis=0) / num_sites)
    )


def test_total_magnetization_FM_state_x(num_sites):
    state = [[1.0, 0.0, 0.0]] * num_sites
    assert numpy.allclose(
        ffunctions.mag_functions.total_magnetization(state),
        1.0
    )


def test_total_magnetization_FM_state_y(num_sites):
    state = [[0.0, 1.0, 0.0]] * num_sites
    assert numpy.allclose(
        ffunctions.mag_functions.total_magnetization(state),
        1.0
    )


def test_total_magnetization_FM_state_z(num_sites):
    state = [[0.0, 0.0, 1.0]] * num_sites
    assert numpy.allclose(
        ffunctions.mag_functions.total_magnetization(state),
        1.0
    )


def test_total_magnetization_AFM_state_x(num_sites):
    state = [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]] * (num_sites // 2)
    assert numpy.allclose(
        ffunctions.mag_functions.total_magnetization(state),
        0.0
    )


def test_total_magnetization_AFM_state_y(num_sites):
    state = [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0]] * (num_sites // 2)
    assert numpy.allclose(
        ffunctions.mag_functions.total_magnetization(state),
        0.0
    )


def test_total_magnetization_AFM_state_z(num_sites):
    state = [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]] * (num_sites // 2)
    assert numpy.allclose(
        ffunctions.mag_functions.total_magnetization(state),
        0.0
    )


@pytest.mark.repeat(100)
def test_magnetization_by_type_random_state(num_sites, random_num_types, random_state):
    types = numpy.random.randint(0, random_num_types, size=num_sites)
    assert sorted(numpy.unique(types)) == list(range(0, random_num_types))

    magnetization_by_type = ffunctions.mag_functions.magnetization_by_type(
        random_state, random_num_types, types)

    assert len(magnetization_by_type) == random_num_types

    values = [numpy.linalg.norm(numpy.sum(random_state[types == t], axis=0) / (types == t).sum())
              for t in range(random_num_types)]

    assert numpy.allclose(magnetization_by_type, values)


def test_magnetization_by_type_AFM_state_x(num_sites):
    state = [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]] * (num_sites // 2)
    types = [0, 1] * (num_sites // 2)

    magnetization_by_type = ffunctions.mag_functions.magnetization_by_type(
        state, 2, types)

    assert numpy.allclose(magnetization_by_type, [1.0, 1.0])


def test_magnetization_by_type_AFM_state_y(num_sites):
    state = [[0.0, 1.0, 0.0], [0.0, -1.0, 0.0]] * (num_sites // 2)
    types = [0, 1] * (num_sites // 2)

    magnetization_by_type = ffunctions.mag_functions.magnetization_by_type(
        state, 2, types)

    assert numpy.allclose(magnetization_by_type, [1.0, 1.0])


def test_magnetization_by_type_AFM_state_z(num_sites):
    state = [[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]] * (num_sites // 2)
    types = [0, 1] * (num_sites // 2)

    magnetization_by_type = ffunctions.mag_functions.magnetization_by_type(
        state, 2, types)

    assert numpy.allclose(magnetization_by_type, [1.0, 1.0])

# magnetization_vector_by_type
# magnetization_vector
