import json


class Sample:
    def __init__(self):
        self.sites = []
        self.neighbors = []
        self.units = None
        self.damping = 1.0
        self.gyromagnetic = 1.0
        self.deltat = 1.0
        self.num_iterations = 100
        self.temperature = 0.0
        self.field = 0.0

        self.jex = 1.0
        self.mu = 1.0
        self.field_axis = [0.0, 0.0, 0.0]
        self.type = "generic"
        self.anisotropy_constant = 0.0
        self.anisotopy_axis = [0.0, 0.0, 0.0]

        self.seed = None
        self.initial_state = None

    def build(self):
        for site in self.sites:
            if "index" not in site or "position" not in site:
                raise Exception("index and positions are required !")

            if "type" not in site:
                site["type"] = self.type

            if "mu" not in site:
                site["mu"] = self.mu

            if "anisotropy_constant" not in site:
                site["anisotropy_constant"] = self.anisotropy_constant

            if "anisotopy_axis" not in site:
                site["anisotopy_axis"] = self.anisotopy_axis

            if "field_axis" not in site:
                site["field_axis"] = self.field_axis

        for neighbor in self.neighbors:
            if "source" not in neighbor or "target" not in neighbor:
                raise Exception("index and positions are required !")

            if "jex" not in neighbor:
                neighbor["jex"] = self.jex

        sample = {
            "geometry": {"sites": self.sites, "neighbors": self.neighbors},
            "parameters": {
                "units": self.units,
                "damping": self.damping,
                "gyromagnetic": self.gyromagnetic,
                "deltat": self.deltat,
            },
            "temperature": self.temperature,
            "field": self.field,
            "num_iterations": self.num_iterations,
        }

        if self.seed:
            sample["seed"] = self.seed

        if self.initial_state:
            sample["initial_state"] = self.initial_state

        return sample

    def save(self, output):
        with open(output, "w") as outfile:
            json.dump(self.build(), outfile, sort_keys=False, indent=2)

