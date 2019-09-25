"""
Module for the computation of the external fields of the LLG equation.
These external fields are the thermal field and the magnetic field.
"""
import numpy


def thermal_field(random_normal_matrix, temperature, magnitude_spin_moment, damping,
                  deltat, gyromagnetic, kB):
    """Function that returns the thermal field on each site"""
    random_normal_matrix = numpy.array(random_normal_matrix)
    num_sites = len(random_normal_matrix)
    out = numpy.zeros((num_sites, 3))
    for i in range(num_sites):
        factor = numpy.sqrt((2 * kB * temperature[i] * damping) / (
            gyromagnetic * deltat * magnitude_spin_moment[i]))
        out[i] = random_normal_matrix[i] * factor
    return out


def magnetic_field(intensities, directions):
    """Function that returns the magnetic field on each site"""
    intensities = numpy.array(intensities)
    directions = numpy.array(directions)
    num_sites = len(intensities)
    out = numpy.zeros((num_sites, 3))
    for i in range(num_sites):
        out[i] = intensities[i] * directions[i]
    return out
