import numpy
import pytest

from llg.functions import magnetization


@pytest.mark.repeat(10)
def test_total_magnetization_random_state(num_sites, random_state):
    assert numpy.allclose(
        magnetization.total_magnetization(random_state),
        numpy.linalg.norm(numpy.sum(random_state, axis=0) / num_sites),
    )


def test_total_magnetization_FM_state_x_up(num_sites):
    state = numpy.array([[1.0, 0.0, 0.0]] * num_sites)
    assert numpy.allclose(magnetization.total_magnetization(state), 1.0)


def test_total_magnetization_FM_state_x_down(num_sites):
    state = numpy.array([[-1.0, 0.0, 0.0]] * num_sites)
    assert numpy.allclose(magnetization.total_magnetization(state), 1.0)


def test_total_magnetization_FM_state_y_up(num_sites):
    state = numpy.array([[0.0, 1.0, 0.0]] * num_sites)
    assert numpy.allclose(magnetization.total_magnetization(state), 1.0)


def test_total_magnetization_FM_state_y_down(num_sites):
    state = numpy.array([[0.0, -1.0, 0.0]] * num_sites)
    assert numpy.allclose(magnetization.total_magnetization(state), 1.0)


def test_total_magnetization_FM_state_z_up(num_sites):
    state = numpy.array([[0.0, 0.0, 1.0]] * num_sites)
    assert numpy.allclose(magnetization.total_magnetization(state), 1.0)


def test_total_magnetization_FM_state_z_down(num_sites):
    state = numpy.array([[0.0, 0.0, -1.0]] * num_sites)
    assert numpy.allclose(magnetization.total_magnetization(state), 1.0)


def test_total_magnetization_AFM_state_x(num_sites):
    state = numpy.array([[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]] * (num_sites // 2))
    assert numpy.allclose(magnetization.total_magnetization(state), 0.0)


def test_total_magnetization_AFM_state_y(num_sites):
    state = numpy.array([[0.0, 1.0, 0.0], [0.0, -1.0, 0.0]] * (num_sites // 2))
    assert numpy.allclose(magnetization.total_magnetization(state), 0.0)


def test_total_magnetization_AFM_state_z(num_sites):
    state = numpy.array([[0.0, 0.0, 1.0], [0.0, 0.0, -1.0]] * (num_sites // 2))
    assert numpy.allclose(magnetization.total_magnetization(state), 0.0)
