import json
from llg import Geometry


class System:
    def __init__(self, geometry: Geometry, parameters: dict):
        self.geometry = geometry
        self.parameters = parameters

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

        return cls(geometry, parameters)

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
