import json
from llg import Geometry


class System:
    """
    This is a class for construct and separate the geometry and parameters.

    Attributes:
        geometry (dict): It contains index, position, type, mu, anisotropy_constant, 
        anisotopy_axis, and field_axis of each site. Also it contains a source, 
        target, and jex.
        parameters (dict): It contains units, damping, gyromagnetic, and deltat.
    """

    def __init__(self, geometry: Geometry, parameters: dict):
        """
        The constructor for System class.

        Parameters:
            geometry (dict): It contains index, position, type, mu, anisotropy_constant, 
            anisotopy_axis, and field_axis of each site. Also it contains a source, 
            target, and jex.
            parameters (dict): It contains units, damping, gyromagnetic, and deltat.
        """
        self.geometry = geometry
        self.parameters = parameters

        if parameters["units"] == "mev":
            parameters["kb"] = 0.08618
        elif parameters["units"] == "joules":
            parameters["kb"] = 1.38064852e-23
        elif parameters["units"] == "adim":
            parameters["kb"] = 1.0
        else:
            raise Exception("units not supported.")

    @classmethod
    def from_dict(cls, system_dict):
        """ 
        It is a function decorator, it creates the dictionary with the attributes 
        that belong to the class method System.

        Parameters:
            system_dict (dict): Dictionary that contains the attributes of the System class.

        Returns: 
            dict: Object that contains index, position, type_, mu, 
            anisotropy_constant, anisotopy_axis and field_axis (geometry). Also 
            it contains a source, target, and jex (neighbors). Finally it 
            contains units, damping, gyromagnetic, and deltat.  
        """
        geometry = Geometry.from_dict(system_dict["geometry"])
        parameters = system_dict["parameters"]

        return cls(geometry, parameters)

    @classmethod
    def from_file(cls, system_file):
        """ 
        It is a function decorator, it creates the geometry file.

        Parameters:
            system_file (file): File that contains the attributes of the System class.
        Returns: 
            system: Object that contains index, position, type_, mu, 
            anisotropy_constant, anisotopy_axis and field_axis (geometry). Also 
            it contains a source, target, and jex (neighbors). Finally it 
            contains units, damping, gyromagnetic, and deltat.
        """
        with open(system_file) as file:
            system = json.load(file)

        return System.from_dict(system)

    def __getattr__(self, attr):
        """
        It is a function that contains the parameters attributes of the System class.

        Parameters:
            attr: It receives the attribute parameter, that contains the units, 
            the damping constant, the gyromagnetic constant, and the deltat.
        """
        if attr in self.parameters:
            return self.parameters[attr]

        raise AttributeError(
            f"{self.__class__.__name__} does not have an attribute {attr}"
        )
