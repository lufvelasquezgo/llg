from itertools import product
from collections import defaultdict
from llg import Sample


class GenericSc(Sample):
    """
    This is a class for create a simple cubic structure. The unit cell therefore
    contains in total one atom.

    Attributes:
        sites (list): It receives a list with the index values, and the positions 
        of the sites in the system.
        neighbors (list): It receives the list of neighbors of the sites in the 
        system.
        units (str): It receives the units of the Boltzmann constant.
        damping (float): It receives the damping constant of the sites in the 
        system.
        gyromagnetic (float): It receives the gyromagnetic constant of the 
        sites in the system.
        deltat (float): It receives the step of time.
        num_iterations (int): It receives the number of iterations per 
        simulation.
        temperature (float/list/dict): It receives the temperature information 
        of the sites in the system.
        field (float/list/dict): It receives the field information of the sites 
        in the system.
        jex (float): It receives the exchange interaction of the sites in the 
        system.
        mu (float): It receives the spin norms of the sites in the system.
        field_axis (list): It receives the field axis of the sites in the system
        type (str): It receives the type of the sites in the system.
        anisotropy_constant (float): It receives the anisotropy constants of 
        the sites in the system.
        anisotopy_axis (list): It receives the anisotropy axis of the sites in 
        the system.
        seed (int): It receives the number of the seed, this is because we want 
        to generate the same number every time before calling ``random.randint()``.
        initial_state (list): It receives the initial state of the sites in the 
        system.
    """

    def __init__(self, length):
        """
        The constructor for GenericSc class. It looks periodic boundary conditions.
        """
        super().__init__()

        self.length = length

        index = {}
        for x, y, z in product(range(self.length), repeat=3):
            index[(x, y, z)] = len(index)

        for position, i in index.items():
            site = {"index": i, "position": position}
            self.sites.append(site)

        pairs = []
        for position, i in index.items():
            x, y, z = position
            pairs.append((i, index[((x + 1) % length, y, z)]))
            pairs.append((i, index[((x - 1) % length, y, z)]))
            pairs.append((i, index[(x, (y + 1) % length, z)]))
            pairs.append((i, index[(x, (y - 1) % length, z)]))
            pairs.append((i, index[(x, y, (z + 1) % length)]))
            pairs.append((i, index[(x, y, (z - 1) % length)]))

        for i, j in pairs:
            self.neighbors.append({"source": i, "target": j})


class GenericBcc(Sample):
    """
    This is a class for create a body-centered cubic structure. The unit cell therefore
    contains in total two atoms.

    Attributes:
        sites (list): It receives a list with the index values, and the positions 
        of the sites in the system.
        neighbors (list): It receives the list of neighbors of the sites in the 
        system.
        units (str): It receives the units of the Boltzmann constant.
        damping (float): It receives the damping constant of the sites in the 
        system.
        gyromagnetic (float): It receives the gyromagnetic constant of the 
        sites in the system.
        deltat (float): It receives the step of time.
        num_iterations (int): It receives the number of iterations per 
        simulation.
        temperature (float/list/dict): It receives the temperature information 
        of the sites in the system.
        field (float/list/dict): It receives the field information of the sites 
        in the system.
        jex (float): It receives the exchange interaction of the sites in the 
        system.
        mu (float): It receives the spin norms of the sites in the system.
        field_axis (list): It receives the field axis of the sites in the system
        type (str): It receives the type of the sites in the system.
        anisotropy_constant (float): It receives the anisotropy constants of 
        the sites in the system.
        anisotopy_axis (list): It receives the anisotropy axis of the sites in 
        the system.
        seed (int): It receives the number of the seed, this is because we want 
        to generate the same number every time before calling ``random.randint()``.
        initial_state (list): It receives the initial state of the sites in the 
        system.
    """

    def __init__(self, length):
        """
        The constructor for GenericBcc class.It looks periodic boundary conditions.
        """
        super().__init__()

        self.length = length

        index = {}
        for x, y, z in product(range(self.length), repeat=3):
            index[(x, y, z)] = len(index)
            index[(x + 0.5, y + 0.5, z + 0.5)] = len(index)

        for position, i in index.items():
            site = {"index": i, "position": position}
            self.sites.append(site)

        pairs = []
        for position, i in index.items():
            x, y, z = position
            pairs.append(
                (i, index[((x + 0.5) % length, (y + 0.5) % length, (z + 0.5) % length)])
            )
            pairs.append(
                (i, index[((x + 0.5) % length, (y + 0.5) % length, (z - 0.5) % length)])
            )
            pairs.append(
                (i, index[((x + 0.5) % length, (y - 0.5) % length, (z + 0.5) % length)])
            )
            pairs.append(
                (i, index[((x + 0.5) % length, (y - 0.5) % length, (z - 0.5) % length)])
            )
            pairs.append(
                (i, index[((x - 0.5) % length, (y + 0.5) % length, (z + 0.5) % length)])
            )
            pairs.append(
                (i, index[((x - 0.5) % length, (y + 0.5) % length, (z - 0.5) % length)])
            )
            pairs.append(
                (i, index[((x - 0.5) % length, (y - 0.5) % length, (z + 0.5) % length)])
            )
            pairs.append(
                (i, index[((x - 0.5) % length, (y - 0.5) % length, (z - 0.5) % length)])
            )

        for i, j in pairs:
            self.neighbors.append({"source": i, "target": j})


class GenericFcc(Sample):
    """
    This is a class for create a face-centered cubic structure. The unit cell therefore
    contains in total four atoms.

    Attributes:
        sites (list): It receives a list with the index values, and the positions 
        of the sites in the system.
        neighbors (list): It receives the list of neighbors of the sites in the 
        system.
        units (str): It receives the units of the Boltzmann constant.
        damping (float): It receives the damping constant of the sites in the 
        system.
        gyromagnetic (float): It receives the gyromagnetic constant of the 
        sites in the system.
        deltat (float): It receives the step of time.
        num_iterations (int): It receives the number of iterations per 
        simulation.
        temperature (float/list/dict): It receives the temperature information 
        of the sites in the system.
        field (float/list/dict): It receives the field information of the sites 
        in the system.
        jex (float): It receives the exchange interaction of the sites in the 
        system.
        mu (float): It receives the spin norms of the sites in the system.
        field_axis (list): It receives the field axis of the sites in the system
        type (str): It receives the type of the sites in the system.
        anisotropy_constant (float): It receives the anisotropy constants of 
        the sites in the system.
        anisotopy_axis (list): It receives the anisotropy axis of the sites in 
        the system.
        seed (int): It receives the number of the seed, this is because we want 
        to generate the same number every time before calling ``random.randint()``.
        initial_state (list): It receives the initial state of the sites in the 
        system.
    """

    def __init__(self, length):
        """
        The constructor for GenericFcc class. It looks periodic boundary conditions.
        """
        super().__init__()

        self.length = length

        index = {}

        for x, y, z in product(range(self.length), repeat=3):
            index[(x, y, z)] = len(index)
            index[(x + 0.5, y + 0.5, z)] = len(index)
            index[(x + 0.5, y, z + 0.5)] = len(index)
            index[(x, y + 0.5, z + 0.5)] = len(index)

        for position, i in index.items():
            site = {"index": i, "position": position}
            self.sites.append(site)

        pairs = []
        for position, i in index.items():
            x, y, z = position
            pairs.append((i, index[((x + 0.5) % length, (y + 0.5) % length, z)]))
            pairs.append((i, index[((x + 0.5) % length, (y - 0.5) % length, z)]))
            pairs.append((i, index[((x - 0.5) % length, (y + 0.5) % length, z)]))
            pairs.append((i, index[((x - 0.5) % length, (y - 0.5) % length, z)]))
            pairs.append((i, index[(x, (y + 0.5) % length, (z + 0.5) % length)]))
            pairs.append((i, index[(x, (y + 0.5) % length, (z - 0.5) % length)]))
            pairs.append((i, index[(x, (y - 0.5) % length, (z + 0.5) % length)]))
            pairs.append((i, index[(x, (y - 0.5) % length, (z - 0.5) % length)]))
            pairs.append((i, index[((x + 0.5) % length, y, (z + 0.5) % length)]))
            pairs.append((i, index[((x + 0.5) % length, y, (z - 0.5) % length)]))
            pairs.append((i, index[((x - 0.5) % length, y, (z + 0.5) % length)]))
            pairs.append((i, index[((x - 0.5) % length, y, (z - 0.5) % length)]))

        for i, j in pairs:
            self.neighbors.append({"source": i, "target": j})


# class GenericHcp(Sample):
#     """
#     This is a class for create a Hexagonal Closest Packed structure. The unit cell therefore
#     contains in total three atoms.

#     Attributes:
#         sites (list): It receives a list with the index values, and the positions
#         of the sites in the system.
#         neighbors (list): It receives the list of neighbors of the sites in the
#         system.
#         units (str): It receives the units of the Boltzmann constant.
#         damping (float): It receives the damping constant of the sites in the
#         system.
#         gyromagnetic (float): It receives the gyromagnetic constant of the
#         sites in the system.
#         deltat (float): It receives the step of time.
#         num_iterations (int): It receives the number of iterations per
#         simulation.
#         temperature (float/list/dict): It receives the temperature information
#         of the sites in the system.
#         field (float/list/dict): It receives the field information of the sites
#         in the system.
#         jex (float): It receives the exchange interaction of the sites in the
#         system.
#         mu (float): It receives the spin norms of the sites in the system.
#         field_axis (list): It receives the field axis of the sites in the system
#         type (str): It receives the type of the sites in the system.
#         anisotropy_constant (float): It receives the anisotropy constants of
#         the sites in the system.
#         anisotopy_axis (list): It receives the anisotropy axis of the sites in
#         the system.
#         seed (int): It receives the number of the seed, this is because we want
#         to generate the same number every time before calling ``random.randint()``.
#         initial_state (list): It receives the initial state of the sites in the
#         system.
#     """

#     def __init__(self, length):
#         """
#         The constructor for GenericHcp class. It looks periodic boundary conditions.
#         """
#         super().__init__()

#         self.length = length

#         index = {}

#         for x, y, z in product(range(self.length), repeat=3):
#             index[(x, y, z)] = len(index)
#             index[(x + 0.5, y + (numpy.sqrt(3) / 6), z + 0.5)] = len(index)

#         for position, i in index.items():
#             site = {"index": i, "position": position}
#             self.sites.append(site)

#         pairs = []
#         for position, i in index.items():
#             x, y, z = position
#             pairs.append(
#                 (
#                     i,
#                     index[
#                         (
#                             (x + 0.5) % length,
#                             (y + (numpy.sqrt(3) / 6)) % length,
#                             (z + 0.5) % length,
#                         )
#                     ],
#                 )
#             )
#             pairs.append(
#                 (
#                     i,
#                     index[
#                         (
#                             (x - 0.5) % length,
#                             (y + (numpy.sqrt(3) / 6)) % length,
#                             (z + 0.5) % length,
#                         )
#                     ],
#                 )
#             )
#             pairs.append(
#                 (
#                     i,
#                     index[
#                         (
#                             (x + 0.5) % length,
#                             (y - (numpy.sqrt(3) / 6)) % length,
#                             (z + 0.5) % length,
#                         )
#                     ],
#                 )
#             )
#             pairs.append(
#                 (
#                     i,
#                     index[
#                         (
#                             (x + 0.5) % length,
#                             (y + (numpy.sqrt(3) / 6)) % length,
#                             (z - 0.5) % length,
#                         )
#                     ],
#                 )
#             )
#             pairs.append(
#                 (
#                     i,
#                     index[
#                         (
#                             (x + 0.5) % length,
#                             (y - (numpy.sqrt(3) / 6)) % length,
#                             (z - 0.5) % length,
#                         )
#                     ],
#                 )
#             )
#             pairs.append(
#                 (
#                     i,
#                     index[
#                         (
#                             (x - 0.5) % length,
#                             (y + (numpy.sqrt(3) / 6)) % length,
#                             (z - 0.5) % length,
#                         )
#                     ],
#                 )
#             )
#             pairs.append((i, index[((x + 1) % length, y, z)]))
#             pairs.append((i, index[((x - 1) % length, y, z)]))
#             pairs.append((i, index[(x, (y + 1) % length, z)]))
#             pairs.append((i, index[(x, (y - 1) % length, z)]))
#             pairs.append((i, index[(x, y, (z + 1) % length)]))
#             pairs.append((i, index[(x, y, (z - 1) % length)]))

#         for i, j in pairs:
#             self.neighbors.append({"source": i, "target": j})
