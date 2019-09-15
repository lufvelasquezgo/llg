"""Python version of Heun scheme"""

import numpy
from llg.ffunctions import external_fields
from llg.ffunctions import spin_fields


def dS_llg(state, Heff, damping, gyromagnetic):
    """Computes the delta_S of a given state"""
    
    alpha = -gyromagnetic / (1.0 + damping * damping)
    cross1 = numpy.cross(state, Heff)
    cross2 = numpy.cross(state, cross1)
    return alpha * (cross1 + damping * cross2)


def integrate(num_sites, state, magnitud_spin_moment, random_normal_matrix,
              temperature, damping, deltat, gyromagnetic, kB,
              field_intensities, field_directions, num_interactions, j_exchange,
              num_neighbors, neighbors, anisotropy_constant, anisotropy_vector):
    """Performs one iteration of the Heun scheme on a given state"""
    
    # compute external fields. These fields do not change
    # because they don't depend on the state
    Hext = extenal_fields.thermal_field(
        num_sites, random_normal_matrix, temperature, magnitud_spin_moment, damping, deltat,
        gyromagnetic, kB)
    Hext += external_fields.magnetic_field(num_sites,
                                           field_intensities, field_directions)

    # predictor step

    # compute the effective field as the sum of external fields and
    # spin fields
    Heff = Hext + spin_fields.exchange_interaction_field(
        num_sites, state, magnitude_spin_moment, num_interactions, j_exchange, num_neighbors,
        neighbors)
    Heff += spin_fields.anisotropy_interaction_field(
        num_sites, state, magnitude_spin_moment, anisotropy_constant, anisotropy_vector)

    # compute dS based on the LLG equation
    dS = dS_llg(state, Heff, damping, gyromagnetic)

    # compute the state_prime
    state_prime = state + deltat * dS

    # normalize state_prime
    state_prime /= numpy.linalg.norm(state_prime, axis=1)[:, numpy.newaxis]

    # corrector step
    # compute the effective field prime by using the state_prime. We
    # use the Heff variable for this in order to reutilize the memory.
    Heff = Hext + spin_fields.exchange_interaction_field(
        num_sites, state_prime, magnitude_spin_moment, num_interactions, j_exchange,
        num_neighbors, neighbors)
    Heff += spin_fields.anisotropy_interaction_field(
        num_sites, state_prime, magnitude_spin_moment, anisotropy_constant, anisotropy_vector)

    # compute dS_prime employing the Heff prime and the state_prime
    dS_prime = dS_llg(state_prime, Heff, damping, gyromagnetic)

    # compute the new state
    new_state = state + 0.5 * (dS + dS_prime) * deltat

    # normalize the new state
    new_state /= numpy.linalg.norm(new_state, axis=1)[:, numpy.newaxis]

    return new_state
