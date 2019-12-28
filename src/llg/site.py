from numbers import Real


class Site:
    """ 
    This is a class for create an object of sites. 

    Attributes: 
        index (int): The index of each site of the system
        position (float): The position of each site of the system
        type (str): The type of each site in the system
        mu (float): The spin norms of each site of the system.
        anisotropy_constant (float): The anisotropy constant of the system
        anisotropy_axis (float): The anisotropy axis of the system
        field_axis (float): The field axis of the system
        neighbors (list): The list of neighbors of the sites in the system.
        jexs (list): The list of the exchanges interactions of the sites in the system.
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
        """ 
        The constructor for Site class. 

        Parameters: 
            index (int): The index of each site of the system
            position (float): The position of each site of the system
            type__ (str): The type of each site in the system
            mu (float): The
            anisotropy_constant (float): The anisotropy constant of the system
            anisotropy_axis (float): The anisotropy axis of the system
            field_axis (float): The field axis of the system
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
        """ 
        The dictionary of the values for Site class. 

        It is a function decorator, it creates the dictionary with the attributes 
        that belong to the class method Site.

        Parameters:
            site_dict (dict): Dictionary that contains the attributes.

        Returns: 
            dict: Object that contains the values index, position, type_, mu, anisotropy_constant, anisotopy_axis and field_axis. 
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
        """ 
        Function to append the neighbors and it own jexs for Site class.

        Parameters: 
            neighbor (int): The neighbors of each site in the system.
            jex (float): The exchange interaction of each site in the system. 
        """
        if not isinstance(neighbor, Site):
            raise Exception("`neighbor` is not an instance of Site.")

        if not isinstance(jex, Real):
            raise Exception("`jex` is not an instance of Real.")

        self.__neighbors.append(neighbor)
        self.__jexs.append(jex)

    def set_neighbors(self, neighbors: list, jexs: list):
        """ 
        It is a function to set the neighbors. 

        Parameters:   
            neighbors (list): The list of neighbors of the sites in the system.
            jexs (list): The list of the exchanges interactions of the sites in the system.
        """
        for neighbor, jex in zip(neighbors, jexs):
            self.append_neighbor(neighbor, jex)

    @property
    def neighbors(self):
        """ 
        It is a function decorator, it provides an interface to instance attribute neighbors. 
        It encapsulates instance attribute neighbors and provides a property Site class. 

        Returns:
            neighbors: Return a property attribute of neighbors.
        """
        return self.__neighbors

    @property
    def jexs(self):
        """ 
        It is a function decorator, it provides an interface to instance attribute exchanges interactions. 
        It encapsulates instance attribute jexs and provides a property Site class. 

        Returns: 
            jexs: Return a property attribute of exchanges interactions.
        """
        return self.__jexs

    def __eq__(self, other_site):
        return self.index == other_site.index
