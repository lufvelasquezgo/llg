from itertools import product
from collections import defaultdict
from llg import Sample


class GenericSc(Sample):
    """This is a class for create a simple cubic structure. The unit cell therefore contains in total one atom.

    :param sites: : It receives a list with the index values, and the positions of the sites in the system.
    :type sites: list
    :param neighbors: : It receives the list of neighbors of the sites in the system.
    :type neighbors: list
    :param units: : It receives the units of the Boltzmann constant.
    :type units: str
    :param damping: : It receives the damping constant of the sites in the system.
    :type damping: float
    :param gyromagnetic: : It receives the gyromagnetic constant of the sites in the system.
    :type gyromagnetic: float
    :param deltat: : It receives the step of time.
    :type deltat: float
    :param num_iterations: : It receives the number of iterations per simulation.
    :type num_iterations: int
    :param temperature: It receives the temperature information of the sites in the system.
    :type temperature: float/list/dict
    :param field: : It receives the field information of the sites in the system.
    :type field: float/list/dict
    :param jex: : It receives the exchange interaction of the sites in the system.
    :type jex: float
    :param mu: : It receives the spin norms of the sites in the system.
    :type mu: float
    :param field_axis: : It receives the field axis of the sites in the system.
    :type field_axis: list
    :param type: : It receives the type of the sites in the system.
    :type type: str
    :param anisotropy_constant: : It receives the anisotropy constants of the sites in the system.
    :type anisotropy_constant: float
    :param anisotopy_axis: : It receives the anisotropy axis of the sites in the system.
    :type anisotopy_axis: list
    :param seed: : It receives the number of the seed, this is because we want to generate the same number every time before calling ``random.randint()``.
    :type seed: int
    :param initial_state: : It receives the initial state of the sites in the system.
    :type initial_state: list
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
    This is a class for create a body-centered cubic structure. The unit cell therefore contains in total two atoms.

    :param sites: : It receives a list with the index values, and the positions of the sites in the system.
    :type sites: list
    :param neighbors: : It receives the list of neighbors of the sites in the system.
    :type neighbors: list
    :param units: : It receives the units of the Boltzmann constant.
    :type units: str
    :param damping: : It receives the damping constant of the sites in the system.
    :type damping: float
    :param gyromagnetic: : It receives the gyromagnetic constant of the sites in the system.
    :type gyromagnetic: float
    :param deltat: : It receives the step of time.
    :type deltat: float
    :param num_iterations: : It receives the number of iterations per simulation.
    :type num_iterations: int
    :param temperature: It receives the temperature information of the sites in the system.
    :type temperature: float/list/dict
    :param field: : It receives the field information of the sites in the system.
    :type field: float/list/dict
    :param jex: : It receives the exchange interaction of the sites in the system.
    :type jex: float
    :param mu: : It receives the spin norms of the sites in the system.
    :type mu: float
    :param field_axis: : It receives the field axis of the sites in the system.
    :type field_axis: list
    :param type: : It receives the type of the sites in the system.
    :type type: str
    :param anisotropy_constant: : It receives the anisotropy constants of the sites in the system.
    :type anisotropy_constant: float
    :param anisotopy_axis: : It receives the anisotropy axis of the sites in the system.
    :type anisotopy_axis: list
    :param seed: : It receives the number of the seed, this is because we want to generate the same number every time before calling ``random.randint()``.
    :type seed: int
    :param initial_state: : It receives the initial state of the sites in the system.
    :type initial_state: list
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
    This is a class for create a face-centered cubic structure. The unit cell therefore contains in total four atoms.

    :param sites: : It receives a list with the index values, and the positions of the sites in the system.
    :type sites: list
    :param neighbors: : It receives the list of neighbors of the sites in the system.
    :type neighbors: list
    :param units: : It receives the units of the Boltzmann constant.
    :type units: str
    :param damping: : It receives the damping constant of the sites in the system.
    :type damping: float
    :param gyromagnetic: : It receives the gyromagnetic constant of the sites in the system.
    :type gyromagnetic: float
    :param deltat: : It receives the step of time.
    :type deltat: float
    :param num_iterations: : It receives the number of iterations per simulation.
    :type num_iterations: int
    :param temperature: It receives the temperature information of the sites in the system.
    :type temperature: float/list/dict
    :param field: : It receives the field information of the sites in the system.
    :type field: float/list/dict
    :param jex: : It receives the exchange interaction of the sites in the system.
    :type jex: float
    :param mu: : It receives the spin norms of the sites in the system.
    :type mu: float
    :param field_axis: : It receives the field axis of the sites in the system.
    :type field_axis: list
    :param type: : It receives the type of the sites in the system.
    :type type: str
    :param anisotropy_constant: : It receives the anisotropy constants of the sites in the system.
    :type anisotropy_constant: float
    :param anisotopy_axis: : It receives the anisotropy axis of the sites in the system.
    :type anisotopy_axis: list
    :param seed: : It receives the number of the seed, this is because we want to generate the same number every time before calling ``random.randint()``.
    :type seed: int
    :param initial_state: : It receives the initial state of the sites in the system.
    :type initial_state: list
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
