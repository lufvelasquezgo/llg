from numbers import Real


class Site:
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
        if not isinstance(neighbor, Site):
            raise Exception("`neighbor` is not an instance of Site.")

        if not isinstance(jex, Real):
            raise Exception("`jex` is not an instance of Real.")

        self.__neighbors.append(neighbor)
        self.__jexs.append(jex)

    def set_neighbors(self, neighbors: list, jexs: list):
        for neighbor, jex in zip(neighbors, jexs):
            self.append_neighbor(neighbor, jex)

    @property
    def neighbors(self):
        return self.__neighbors

    @property
    def jexs(self):
        return self.__jexs

    def __eq__(self, other_site):
        return self.index == other_site.index
