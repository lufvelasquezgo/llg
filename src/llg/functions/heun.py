import numpy
from nptyping import NDArray
from typing import Any
from llg.functions.external_fields import thermal_field, magnetic_field
from llg.functions.spin_fields import (
    exchange_interaction_field,
    anisotropy_interaction_field,
)
from numba import jit


@jit(nopython=True)
def dS_llg(
    state: NDArray[(Any, 3), float],
    Heff: NDArray[(Any, 3), float],
    damping: float,
    gyromagnetic: float,
) -> NDArray[(Any, 3), float]:
    alpha = -gyromagnetic / (1 + damping * damping)
    cross1 = numpy.cross(state, Heff)
    cross2 = numpy.cross(state, cross1)
    return alpha * (cross1 + damping * cross2)


@jit(nopython=True)
def normalize(matrix: NDArray[(Any, 3), float]) -> NDArray[(Any, 3), float]:
    norms = numpy.sqrt((matrix * matrix).sum(axis=1))
    norms_repeated = numpy.repeat(norms, 3)
    norms_repeated_reshaped = norms_repeated.reshape((len(norms), 3))
    return matrix / norms_repeated_reshaped


def integrate(
    state: NDArray[(Any, 3), float],
    magnitude_spin_moment: NDArray[Any, float],
    temperature: NDArray[Any, float],
    damping: float,
    deltat: float,
    gyromagnetic: float,
    kB: float,
    magnetic_fields: NDArray[(Any, 3), float],
    exchanges: NDArray[(Any, Any), float],
    neighbors: NDArray[(Any, Any), float],
    anisotropy_constants: NDArray[Any, float],
    anisotropy_vectors: NDArray[(Any, 3), float],
) -> float:
    # compute external fields. These fields does not change
    # because they don't depend on the state
    Hext = thermal_field(
        temperature, magnitude_spin_moment, damping, deltat, gyromagnetic, kB
    )
    Hext += magnetic_field(magnetic_fields)

    # predictor step

    # compute the effective field as the sum of external fields and
    # spin fields
    Heff = Hext + exchange_interaction_field(
        state, magnitude_spin_moment, exchanges, neighbors
    )
    Heff = Heff + anisotropy_interaction_field(
        state, magnitude_spin_moment, anisotropy_constants, anisotropy_vectors
    )

    # compute dS based on the LLG equation
    dS = dS_llg(state, Heff, damping, gyromagnetic)

    # compute the state_prime
    state_prime = state + deltat * dS

    # normalize state_prime
    state_prime = normalize(state_prime)

    # corrector step

    # compute the effective field prime by using the state_prime. We
    # use the Heff variable for this in order to reutilize the memory.
    Heff = Hext + exchange_interaction_field(
        state_prime, magnitude_spin_moment, exchanges, neighbors
    )
    Heff = Heff + anisotropy_interaction_field(
        state_prime, magnitude_spin_moment, anisotropy_constants, anisotropy_vectors
    )

    # compute dS_prime employing the Heff prime and the state_prime
    dS_prime = dS_llg(state_prime, Heff, damping, gyromagnetic)

    # compute the new state
    integrate = state + 0.5 * (dS + dS_prime) * deltat

    # normalize the new state
    return normalize(integrate)
