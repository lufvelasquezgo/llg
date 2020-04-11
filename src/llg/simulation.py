import json
import numpy
from tqdm import tqdm
from llg.functions import heun
from llg.functions import energy
from llg import System
from llg import Bucket
import random
import click


def get_random_state(num_sites):
    random_state = numpy.random.normal(size=(num_sites, 3))
    norms = numpy.linalg.norm(random_state, axis=1)
    random_state = [vec / norms[i] for i, vec in enumerate(random_state)]
    return random_state


class Simulation:
    """This is a class for make a simulation in order to evolve the state of the system.

    :param system: Object that contains index, position, type_, mu, anisotropy_constant, anisotopy_axis and field_axis (geometry). Also it contains a source, target, and jex (neighbors). Finally it contains units, damping, gyromagnetic, and deltat.
    :type system: 
    :param temperature: The temperature of the sites in the system.
    :type temperature: float/list
    :param field: The field that acts under the sites in the system.
    :type field: float/list
    :param num_iterations: The number of iterations for evolve the system.
    :type num_iterations: int
    :param seed: The seed for the random state.
    :type seed: int
    :param initial_state: The initial state of the sites in te system.
    :type initial_state: list
    """

    def __init__(
        self,
        system,
        temperature: Bucket,
        field: Bucket,
        num_iterations=None,
        seed=None,
        initial_state=None,
    ):
        """
        The constructor for Simulation class.
        """
        self.system = system
        self.temperature = temperature
        self.field = field
        self.seed = seed

        if num_iterations:
            self.num_iterations = num_iterations
        else:
            self.num_iterations = 1000

        if seed:
            self.seed = seed
        else:
            self.seed = random.getrandbits(32)

        numpy.random.seed(self.seed)
        if initial_state:
            self.initial_state = initial_state
        else:
            self.initial_state = get_random_state(self.system.geometry.num_sites)

        self.initial_state = numpy.array(self.initial_state)

    @classmethod
    def from_file(cls, simulation_file):
        """ It is a function decorator, it creates the simulation file.

        :param simulation_file: File that contains index, position, type, mu, anisotropy_constant, anisotopy_axis, and field_axis of each site. Also it contains a source, target, and jex. 
        :type simulation_file: file

        :return: Object that contains the ``system object``, temperature, field, num_iterations, seed and initial_state.
        :rtype: Object 
        """
        with open(simulation_file) as file:
            simulation_dict = json.load(file)

        system = System.from_file(simulation_file)
        initial_state = simulation_dict.get("initial_state")
        num_iterations = simulation_dict.get("num_iterations")
        seed = simulation_dict.get("seed")

        temperature = Bucket(simulation_dict["temperature"])
        field = Bucket(simulation_dict["field"])
        temperature, field = Bucket.match_sizes(temperature, field)

        return cls(system, temperature, field, num_iterations, seed, initial_state)

    def set_num_iterations(self, num_iterations):
        """It is a function to set the number of iterations.

        :param num_iterations: The number of iterations for evolve the system.
        :type num_iterations: int
        """
        self.num_iterations = num_iterations

    def set_initial_state(self, initial_state):
        """It is a function to set the initial state for each site.

        :param initial_state: The initial state of the sites in te system.
        :type initial_state: list
        """
        self.initial_state = numpy.array(initial_state)

    @property
    def information(self):
        """It is a function decorator, it creates an object with the complete information needed for the ``run`` function.

        :return: num_sites
        :rtype: int
        :return: parameters
        :rtype: str
        :return: temperature
        :rtype: float/list
        :return: field
        :rtype: float/list
        :return: seed
        :rtype: int
        :return: num_iterations
        :rtype: int
        :return: positions
        :rtype: list
        :return: types
        :rtype: str
        :return: initial_state
        :rtype: list
        :return: num_TH
        :rtype: int
        """
        return {
            "num_sites": self.system.geometry.num_sites,
            "parameters": self.system.parameters,
            "temperature": self.temperature.values,
            "field": self.field.values,
            "seed": self.seed,
            "num_iterations": self.num_iterations,
            "positions": self.system.geometry.positions,
            "types": self.system.geometry.types,
            "initial_state": self.initial_state,
            "num_TH": len(self.temperature),
        }

    def run(self):
        """This function creates a generator. It calculates the evolve of the states through the implementation of the LLG equation. Also, it uses these states for calculate the exchange energy, anisotropy energy, magnetic energy, and hence, the total energy of the system.

        :param spin_norms: It receives the spin norms of the sites in the system.
        :type spin_norms: list
        :param damping: It receives the damping constant of the sites in the system.
        :type damping: float
        :param deltat: It receives the step of time.
        :type deltat: float
        :param gyromagnetic: It receives the gyromagnetic constant of the sites in the system.
        :type gyromagnetic: float
        :param kb: It receives the Boltzmann constant in an specific units.
        :type kb: float
        :param field_axes: It receives the field axis of the sites in the system.
        :type field_axes: float/list
        :param j_exchanges: It receives the list of the exchanges interactions of the sites in the system.
        :type j_exchanges: list
        :param num_neighbors: It receives the number of neighbors per site of the system.
        :type num_neighbors: list
        :param neighbors: It receives the list of neighbors of the sites in the system.
        :type neighbors: list
        :param anisotropy_constants: It receives the anisotropy constants of the sites in the system.
        :type anisotropy_constants: float
        :param anisotropy_vectors: It receives the anisotropy axis of the sites in the system.
        :type anisotropy_vectors: list
        :param num_sites: It receives the total of spin magnetic moments.
        :type num_sites: list
        :param state: It receives the initial state of the system.
        :type state: list
        """
        spin_norms = self.system.geometry.spin_norms
        damping = self.system.damping
        deltat = self.system.deltat
        gyromagnetic = self.system.gyromagnetic
        kb = self.system.kb
        field_axes = self.system.geometry.field_axes
        exchanges = self.system.geometry.exchanges
        neighbors = self.system.geometry.neighbors
        anisotropy_constants = self.system.geometry.anisotropy_constants
        anisotropy_vectors = self.system.geometry.anisotropy_axes
        num_sites = self.system.geometry.num_sites
        state = self.initial_state

        for T, H in zip(self.temperature, self.field):
            temperatures = numpy.array([T] * num_sites)
            magnetic_fields = H * field_axes

            for _ in tqdm(range(self.num_iterations)):
                state = heun.integrate(
                    state,
                    spin_norms,
                    temperatures,
                    damping,
                    deltat,
                    gyromagnetic,
                    kb,
                    magnetic_fields,
                    exchanges,
                    neighbors,
                    anisotropy_constants,
                    anisotropy_vectors,
                )

                exchange_energy_value = energy.compute_exchange_energy(
                    state, exchanges, neighbors
                )
                anisotropy_energy_value = energy.compute_anisotropy_energy(
                    state, anisotropy_constants, anisotropy_vectors
                )
                magnetic_energy_value = energy.compute_magnetic_energy(
                    state, spin_norms, magnetic_fields
                )
                total_energy_value = (
                    exchange_energy_value
                    + anisotropy_energy_value
                    + magnetic_energy_value
                )

                yield state, exchange_energy_value, anisotropy_energy_value, magnetic_energy_value, total_energy_value
