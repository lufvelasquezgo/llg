from numbers import Real


class Site:
    """This is a class for create an object of sites. 

    :param index: The index of each site of the system
    :type index: int
    :param position: The position of each site of the system
    :type position: float
    :param type: The type of each site in the system
    :type type: str
    :param mu: The spin norms of each site of the system.
    :type mu: float
    :param anisotropy_constant: The anisotropy constant of the system
    :type anisotropy_constant: float
    :param anisotropy_axis: The anisotropy axis of the system
    :type anisotropy_axis: float
    :param field_axis: The field axis of the system
    :type field_axis: float
    :param neighbors: The list of neighbors of the sites in the system.
    :type neighbors: list
    :param jexs: The list of the exchanges interactions of the sites in the system.
    :type jexs: list
    """

    def __init__(
        self,
        index,
        position,
        type_,
        mu,
        anisotropy_constant,
        anisotopy_axis,
        field_axis,
    ):
        """The constructor for Site class. 

        :param index: The index of each site of the system.
        :type index: int
        :param position: The position of each site of the system.
        :type position: float
        :param type__: The type of each site in the system.
        :type type__: str
        :param mu: The .
        :type mu: float
        :param anisotropy_constant: The anisotropy constant of the system.
        :type anisotropy_constant: float
        :param anisotropy_axis: The anisotropy axis of the system.
        :type anisotropy_axis: float
        :param field_axis: The field axis of the system.
        :type field_axis: float
        """
        self.index = index
        self.position = position
        self.type = type_
        self.mu = mu
        self.anisotropy_constant = anisotropy_constant
        self.anisotopy_axis = anisotopy_axis
        self.field_axis = field_axis
        self.__neighbors = []
        self.__jexs = []

    @classmethod
    def from_dict(cls, site_dict):
        """ The dictionary of the values for Site class. It is a function decorator, it creates the dictionary with the attributes that belong to the class method Site.

        :param site_dict: Dictionary that contains the attributes.
        :type site_dict: dict

        :return: Object that contains the values index, position, type_, mu, anisotropy_constant, anisotopy_axis and field_axis. 
        :rtype: dict
        """
        index = site_dict["index"]
        position = site_dict["position"]
        type_ = site_dict["type"]
        mu = site_dict["mu"]
        anisotropy_constant = site_dict["anisotropy_constant"]
        anisotopy_axis = site_dict["anisotopy_axis"]
        field_axis = site_dict["field_axis"]

        return cls(
            index, position, type_, mu, anisotropy_constant, anisotopy_axis, field_axis
        )

    def append_neighbor(self, neighbor, jex: float):
        """Function to append the neighbors and it own jexs for Site class.

        :param neighbor: The neighbors of each site in the system.
        :type neighbor: int
        :param jex: The exchange interaction of each site in the system. 
        :type jex: float
        """
        if not isinstance(neighbor, Site):
            raise Exception("`neighbor` is not an instance of Site.")

        if not isinstance(jex, Real):
            raise Exception("`jex` is not an instance of Real.")

        self.__neighbors.append(neighbor)
        self.__jexs.append(jex)

    def set_neighbors(self, neighbors: list, jexs: list):
        """It is a function to set the neighbors. 

        :param neighbors: The list of neighbors of the sites in the system.
        :type neighbors: list
        :param jexs: The list of the exchanges interactions of the sites in the system.
        :type jexs: list
        """
        for neighbor, jex in zip(neighbors, jexs):
            self.append_neighbor(neighbor, jex)

    @property
    def neighbors(self):
        """It is a function decorator, it provides an interface to instance attribute neighbors. It encapsulates instance attribute neighbors and provides a property Site class. 

        return: Return a property attribute of neighbors.
        """
        return self.__neighbors

    @property
    def jexs(self):
        """It is a function decorator, it provides an interface to instance attribute exchanges interactions. It encapsulates instance attribute jexs and provides a property Site class. 

        return: Return a property attribute of exchanges interactions.
        """
        return self.__jexs

    def __eq__(self, other_site):
        return self.index == other_site.index
