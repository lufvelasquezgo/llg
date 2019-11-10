import json
import numpy
from tqdm import tqdm
from llg.ffunctions import heun
from llg.ffunctions import energy
from llg import System
from llg import Bucket
import random


def get_random_state(num_sites):
    random_state = numpy.random.normal(size=(num_sites, 3))
    norms = numpy.linalg.norm(random_state, axis=1)
    random_state = [vec / norms[i] for i, vec in enumerate(random_state)]
    return random_state


class Simulation:
    def __init__(
        self,
        system,
        temperature: Bucket,
        field: Bucket,
        num_iterations=None,
        seed=None,
        initial_state=None,
    ):
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
        with open(simulation_file) as file:
            simulation_dict = json.load(file)

        system = System.from_file(simulation_file)
        initial_state = simulation_dict.get("initial_state")
        num_iterations = simulation_dict.get("num_iterations")
        temperature = Bucket(simulation_dict["temperature"])
        field = Bucket(simulation_dict["field"])
        seed = simulation_dict.get("seed")

        temperature, field = Bucket.match_sizes(temperature, field)

        return cls(system, temperature, field, num_iterations, seed, initial_state)

    def set_num_iterations(self, num_iterations):
        self.num_iterations = num_iterations

    def set_initial_state(self, initial_state):
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
            temperature_sites = [T] * num_sites
            field_sites = [H] * num_sites

            for _ in tqdm(range(self.num_iterations)):
                random_normal_matrix = numpy.random.normal(size=(num_sites, 3))
                state = heun.integrate(
                    state,
                    spin_norms,
                    random_normal_matrix,
                    temperature_sites,
                    damping,
                    deltat,
                    gyromagnetic,
                    kb,
                    field_sites,
                    field_axes,
                    j_exchanges,
                    num_neighbors,
                    neighbors,
                    anisotropy_constants,
                    anisotropy_axes,
                )

                exchange_energy_value = energy.exchange_energy(
                    state, j_exchanges, num_neighbors, neighbors
                )
                anisotropy_energy_value = energy.anisotropy_energy(
                    state, anisotropy_constants, anisotropy_axes
                )
                magnetic_energy_value = energy.magnetic_energy(
                    spin_norms, state, field_sites, field_axes
                )
                total_energy_value = (
                    exchange_energy_value
                    + anisotropy_energy_value
                    + magnetic_energy_value
                )

                yield state, exchange_energy_value, anisotropy_energy_value, magnetic_energy_value, total_energy_value
