import random
import json
from llg import Bucket
from llg import Geometry


class System:
    def __init__(
        self,
        geometry: Geometry,
        parameters: dict,
        temperatures: Bucket,
        fields: Bucket,
        seed=random.getrandbits(32),
    ):
        self.geometry = geometry
        self.parameters = parameters
        self.temperatures = temperatures
        self.fields = fields
        self.seed = seed

        if parameters["units"] == "mev":
            parameters["kb"] = 0.08618
        elif parameters["units"] == "joules":
            parameters["kb"] = 1.38064852e-23
        else:
            parameters["kb"] = 1.0

    @classmethod
    def from_dict(cls, system_dict):
        geometry = Geometry.from_dict(system_dict["geometry"])
        parameters = system_dict["parameters"]
        temperatures = Bucket(system_dict["temperature"])
        fields = Bucket(system_dict["field"])
        temperatures, fields = Bucket.match_sizes(temperatures, fields)
        seed = system_dict.get("seed")

        return cls(geometry, parameters, temperatures, fields, seed)

    @classmethod
    def from_file(cls, system_file):
        with open(system_file) as file:
            system = json.load(file)

        return System.from_dict(system)

    def __getattr__(self, attr):
        if attr in self.parameters:
            return self.parameters[attr]

        raise AttributeError(
            f"{self.__class__.__name__} does not have an attribute {attr}"
        )

    @property
    def information(self):
        return {
            "num_sites": self.geometry.num_sites,
            "parameters": self.parameters,
            "temperatures": self.temperatures.values,
            "fields": self.fields.values,
            "seed": self.seed,
        }
