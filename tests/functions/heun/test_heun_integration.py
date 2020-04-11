import numpy
import pytest
from llg.functions import heun


def sech(x):
    return 1 / numpy.cosh(x)


def single_spin_analytical(field, damping, gyromagnetic, t):
    A = (gyromagnetic * field) / (1 + damping * damping)
    Sx = sech(damping * A * t) * numpy.cos(A * t)
    Sy = sech(damping * A * t) * numpy.sin(A * t)
    Sz = numpy.tanh(damping * A * t)
    return [Sx, Sy, Sz]


@pytest.mark.repeat(100)
def test_single_spin():
    H = numpy.random.uniform(-1, 1)
    damping = numpy.random.uniform(0, 1)
    gyromagnetic = 1.76e11

    # For deltat >= 1e-13, the assertions fail, which means there is a
    # significant loss of numerical precision
    deltat = 1e-15

    state = numpy.array([[1, 0, 0]])

    # Here, we are asserting that for every time step, both implementations
    # are in agreement with each other and with the analytical solution
    iterations = 100
    for it in range(iterations):
        t = (it + 1) * deltat
        state = heun.integrate(
            state,
            numpy.array([1.0]),
            numpy.array([0.0]),
            damping,
            deltat,
            gyromagnetic,
            1.0,
            numpy.array([[0, 0, H]]),
            numpy.array([[0]]),
            numpy.array([[0]]),
            numpy.array([0]),
            numpy.array([[0.0] * 3]),
        )
        analytical = single_spin_analytical(H, damping, gyromagnetic, t)
        assert numpy.allclose(analytical, state[0])
