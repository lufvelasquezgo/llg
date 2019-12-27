import json
import numpy
from tqdm import tqdm
from llg.ffunctions import heun
from llg.ffunctions import energy
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
    """
    This is a class for make a simulation in order to evolve the state of the system.

    Attributes:
        system (): Object that contains index, position, type_, mu, 
            anisotropy_constant, anisotopy_axis and field_axis (geometry). Also 
            it contains a source, target, and jex (neighbors). Finally it 
            contains units, damping, gyromagnetic, and deltat.
        temperature (float-list): The temperature of the sites in the system.
        field (float-list): The field that acts under the sites in the system.
        num_iterations (int): The number of iterations for evolve the system.
        seed (int): The seed for the random state.
        initial_state (list): The initial state of the sites in te system.
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

        Parameters:
            system (): Object that contains index, position, type_, mu, 
            anisotropy_constant, anisotopy_axis and field_axis (geometry). Also 
            it contains a source, target, and jex (neighbors). Finally it 
            contains units, damping, gyromagnetic, and deltat.
            temperature (float-list): The temperature of the sites in the system.
            field (float-list): 
            num_iterations (int): The number of iterations for evolve the system.
            seed (int): The seed for the random state. 
            initial_state (list): The initial state of the sites in te system.
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

    @classmethod
    def from_file(cls, simulation_file):
        """ 
        It is a function decorator, it creates the simulation file.

        Parameters:
            simulation_file (file): File that contains index, position, type, 
            mu, anisotropy_constant, anisotopy_axis, and field_axis of each 
            site. Also it contains a source, target, and jex. 

        Returns: 
            simulation: Object that contains the. 
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
        """
        It is a function to set the number of iterations.

        Parameters:
            num_iterations (int): The number of iterations for evolve the system.
        """
        self.num_iterations = num_iterations

    def set_initial_state(self, initial_state):
        """
        It is a function to set the initial state for each site.

        Parameters:
            initial_state (list): The initial state of the sites in te system.
        """
        self.initial_state = initial_state

    @property
    def information(self):
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
        spin_norms = self.system.geometry.spin_norms
        damping = self.system.damping
        deltat = self.system.deltat
        gyromagnetic = self.system.gyromagnetic
        kb = self.system.kb
        field_axes = self.system.geometry.field_axes
        j_exchanges = self.system.geometry.exchanges
        num_neighbors = self.system.geometry.num_neighbors
        neighbors = self.system.geometry.neighbors
        anisotropy_constants = self.system.geometry.anisotropy_constants
        anisotropy_axes = self.system.geometry.anisotropy_axes
        num_sites = self.system.geometry.num_sites
        state = self.initial_state

        for T, H in zip(self.temperature, self.field):
            temperatures = [T] * num_sites
            field_intensities = [H] * num_sites

            for _ in tqdm(range(self.num_iterations)):
                random_normal_matrix = numpy.random.normal(size=(num_sites, 3))
                state = heun.integrate(
                    state,
                    spin_norms,
                    random_normal_matrix,
                    temperatures,
                    damping,
                    deltat,
                    gyromagnetic,
                    kb,
                    field_intensities,
                    field_axes,
                    j_exchanges,
                    num_neighbors,
                    neighbors,
                    anisotropy_constants,
                    anisotropy_axes,
                )

                exchange_energy_value = (
                    energy.exchange_energy(state, j_exchanges, num_neighbors, neighbors)
                    / num_sites
                )
                anisotropy_energy_value = (
                    energy.anisotropy_energy(
                        state, anisotropy_constants, anisotropy_axes
                    )
                    / num_sites
                )
                magnetic_energy_value = (
                    energy.magnetic_energy(
                        spin_norms, state, field_intensities, field_axes
                    )
                    / num_sites
                )
                total_energy_value = (
                    exchange_energy_value
                    + anisotropy_energy_value
                    + magnetic_energy_value
                )

                yield state, exchange_energy_value, anisotropy_energy_value, magnetic_energy_value, total_energy_value
