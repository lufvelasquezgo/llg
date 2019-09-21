import numpy


def thermal_field(random_normal_matrix, temperature, magnitude_spin_moment, damping, deltat, gyromagnetic, kB):
    num_sites = len(random_normal_matrix)
    out = numpy.zeros((num_sites, 3))
    for i in range(num_sites):
        factor = numpy.sqrt((2 * kB * temperature[i] * damping) / (
            gyromagnetic * deltat * magnitude_spin_moment[i]))
        out[i] = random_normal_matrix[i] * factor
    return out


def magnetic_field(intensities, directions):
    intensities = numpy.array(intensities)
    directions = numpy.array(directions)
    num_sites = len(intensities)
    out = numpy.zeros((num_sites, 3))
    for i in range(num_sites):
        out[i] = intensities[i] * directions[i]
    return out
