import json
import numpy
from tqdm import tqdm
from llg.ffunctions import heun
from llg import System


def get_random_state(num_sites):
    random_state = numpy.random.normal(size=(num_sites, 3))
    norms = numpy.linalg.norm(random_state, axis=1)
    random_state = [vec / norms[i] for i, vec in enumerate(random_state)]
    return random_state


class Simulation:
    def __init__(self, system, num_iterations=1000, initial_state=None):
        self.system = system
        self.num_iterations = num_iterations

        numpy.random.seed(self.system.seed)
        if initial_state:
            self.initial_state = initial_state
        else:
            self.initial_state = get_random_state(self.system.geometry.num_sites)

    @classmethod
    def from_file(cls, sample_name):
        with open(sample_name) as file:
            sample = json.load(file)

        system = System.from_file(sample_name)
        initial_state = sample.get("initial_state")
        num_iterations = sample.get("num_iterations")

        return cls(system, num_iterations, initial_state)

    def set_num_iterations(self, num_iterations):
        self.num_iterations = num_iterations

    def set_initial_state(self, initial_state):
        self.initial_state = initial_state

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

        for T, H in zip(self.system.temperature, self.system.field):
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

                yield state
