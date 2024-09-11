import json


class Sample:
    """This is a class for construct the sample with all the attributes presented below.

    :param sites: It receives a list with the index values, and the positions of the
    sites in the system.
    :type sites: list
    :param neighbors: It receives the list of neighbors of the sites in the system.
    :type neighbors: list
    :param units: It receives the units of the Boltzmann constant.
    :type units: str
    :param damping: It receives the damping constant of the sites in the system.
    :type damping: float
    :param gyromagnetic: It receives the gyromagnetic constant of the sites in the
    system.
    :type gyromagnetic: float
    :param deltat: It receives the step of time.
    :type deltat: float
    :param num_iterations: It receives the number of iterations per simulation.
    :type num_iterations: int
    :param temperature: It receives the temperature information of the sites in the
    system.
    :type temperature: float/list/dict, optional.
    :param field: It receives the field information of the sites in the system.
    :type field: float/list/dict, optional.
    :param jex: It receives the exchange interaction of the sites in the system.
    :type jex: float
    :param mu: It receives the spin norms of the sites in the system.
    :type mu: float
    :param field_axis: It receives the field axis of the sites in the system
    :type field_axis: list
    :param type: It receives the type of the sites in the system.
    :type type: str, optional.
    :param anisotropy_constant: It receives the anisotropy constants of the sites in
    the system.
    :type anisotropy_constant: float
    :param anisotropy_axis: It receives the anisotropy axis of the sites in the system.
    :type anisotropy_axis: list
    :param seed: It receives the number of the seed, this is because we want to
    generate the same number every time before calling ``random.randint()``.
    :type seed: int, optional.
    :param initial_state: It receives the initial state of the sites in the system.
    :type initial_state: list, optional.
    """

    def __init__(
        self,
        sites,
        neighbors,
        units,
        damping,
        gyromagnetic_ratio,
        deltat,
        num_iterations,
        temperature,
        magnetic_field,
        initial_state,
        seed,
    ):
        """
        The constructor for Sample class.
        """
        self.sites = sites
        self.neighbors = neighbors
        self.units = units
        self.damping = damping
        self.gyromagnetic = gyromagnetic_ratio
        self.deltat = deltat
        self.num_iterations = num_iterations
        self.temperature = temperature
        self.field = magnetic_field

        self.seed = initial_state
        self.initial_state = seed

    def build(self):
        """It is a function responsible for building the sample. It receives all the
        attributes of the Sample class. This function ensures that all attributes were
        entered. If any of them is missing, the function throw an ``Exception``.

        :raises :class:`Exception`: index and positions are required !

        :return: It is a dictionary with all the attributes organized.
        :rtype: dict
        """
        for site in self.sites:
            if "index" not in site or "position" not in site:
                raise Exception("index and positions are required !")

            if "type" not in site:
                site["type"] = self.type

            if "mu" not in site:
                site["mu"] = self.mu

            if "anisotropy_constant" not in site:
                site["anisotropy_constant"] = self.anisotropy_constant

            if "anisotropy_axis" not in site:
                site["anisotropy_axis"] = self.anisotropy_axis

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
        """It is a function to save all the information created in the ``build``
        function in a json file."""
        with open(output, "w") as outfile:
            json.dump(self.build(), outfile, sort_keys=False, indent=2)
