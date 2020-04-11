from llg import Site
import json
from collections import namedtuple
import numpy


class Geometry:
    """ This is a class is created to get the object sites. 

    :param sites: The dictionary that contains an index, position, type, mu, anisotropy_constant, anisotopy_axis, and field_axis of each site. 
    :type sites: dict
    :param neighbors: The dictionary that contains a source, target, and jex.
    :type neighbors: dict
    """

    def __init__(self, sites):
        """ The constructor for Geometry class. 

        :param sites: The dictionary that contains an index, position, type, mu, anisotropy_constant, anisotopy_axis, and field_axis of each site.
        :type sites: dict
        """
        self.__sites = sites

    @classmethod
    def from_file(cls, geometry_file):
        """It creates the geometry file.

        :param geometry_file: File that contains index, position, type, mu, anisotropy_constant, anisotopy_axis, and field_axis of each site. Also it contains a source, target, and jex. 
        :type geometry_file: file

        :return: Object that contains the complete information.
        :rtype: Object
        """

        with open(geometry_file) as file:
            geometry = json.load(file)["geometry"]

        return Geometry.from_dict(geometry)

    @classmethod
    def from_dict(cls, geometry_dict):
        """ It creates the geometry dictionary. The dictionary contain the indexes as keys but the values are the same objects,such as, if we alter ``sites_dict`` values, we also alter the corresponding one in ``sites``.

        :param geometry_dict: Dictionary that contains index, position, type, mu, anisotropy_constant, anisotopy_axis, and field_axis of each site. Also it contains a source, target, and jex.
        :type geometry_dict: dict
        """
        sites = geometry_dict["sites"]
        neighbors = geometry_dict["neighbors"]

        sites = Geometry.read_sites(sites)
        sites_dict = {site.index: site for site in sites}

        neighbors = Geometry.read_neighbors(neighbors)

        for link in neighbors:
            site = sites_dict[link.source]
            nhb = sites_dict[link.target]
            site.append_neighbor(nhb, link.jex)

        return cls(sites)

    @property
    def positions(self):
        """It provides an interface to instance attribute position. It encapsulates instance attribute position and provides a property Site class.

        :return: Return a property attribute of position.
        """
        return [site.position for site in self.__sites]

    @property
    def types(self):
        """It provides an interface to instance attribute types. It encapsulates instance attribute types and provides a property Site class.

        :return: Return a property attribute of types.
        """
        return [site.type for site in self.__sites]

    @staticmethod
    def read_sites(site_dicts: list):
        """It is an instance for read sites. It just gets the arguments site.

        :param site_dicts: Dictionary that contains index, position, type, mu, anisotropy_constant, anisotopy_axis, and field_axis of each site.
        :type site_dicts: dict

        :return: Object that contains the sites values.
        :rtype: Object
        """
        output_sites = []
        for site_dict in site_dicts:
            site = Site.from_dict(site_dict)
            if site in output_sites:
                raise Exception(f"Site with the index {site.index} already exists !!!")
            output_sites.append(site)
        return output_sites

    @staticmethod
    def read_neighbors(neighbors_dicts: list):
        """It is an instance for read neighbors. It just gets the arguments neighbors.

        :param neighbors_dicts: Dictionary that contains a source, target, and jex of each site.
        :type neighbors_dicts: dict

        :return: Object that contains the neighbor values.
        :rtype: Object
        """
        Link = namedtuple("Link", ["source", "target", "jex"])
        links = []
        for link in neighbors_dicts:
            source = link["source"]
            target = link["target"]
            jex = link["jex"]

            links.append(Link(source=source, target=target, jex=jex))

        return links

    @property
    def num_interactions(self):
        """It provides an interface to instance attribute num_interactions. It encapsulates instance attribute num_interactions and provides a property Site class.

        :return: Return a property attribute of num_interactions.
        """
        count = 0
        for site in self.__sites:
            count += len(site.neighbors)
        return count

    @property
    def num_sites(self):
        """It provides an interface to instance attribute num_sites. It encapsulates instance attribute num_sites and provides a property Site class.

        :return: Return a property attribute of num_sites.
        """
        return len(self.__sites)

    @property
    def spin_norms(self):
        """It provides an interface to instance attribute spin_norms. It encapsulates instance attribute spin_norms and provides a property Site class.

        :return: Return a property attribute of spin_norms.
        """
        return numpy.array([site.mu for site in self.__sites])

    @property
    def field_axes(self):
        """It provides an interface to instance attribute field_axes. It encapsulates instance attribute field_axes and provides a property Site class.

        :return: Return a property attribute of field_axes.
        """
        return numpy.array([site.field_axis for site in self.__sites])

    @property
    def num_neighbors(self):
        """It provides an interface to instance attribute num_neighbors. It encapsulates instance attribute num_neighbors and provides a property Site class.

        :return: Return a property attribute of num_neighbors.
        """
        return [len(site.neighbors) for site in self.__sites]

    @property
    def anisotropy_constants(self):
        """It provides an interface to instance attribute anisotropy_constants. It encapsulates instance attribute anisotropy_constants and provides a property Site class.

        :return: Return a property attribute of anisotropy_constants.
        """
        return numpy.array([site.anisotropy_constant for site in self.__sites])

    @property
    def anisotropy_axes(self):
        """It provides an interface to instance attribute anisotropy_axes. It encapsulates instance attribute anisotropy_axes and provides a property Site class.

        :return: Return a property attribute of anisotropy_axes.
        """
        return numpy.array([site.anisotopy_axis for site in self.__sites])

    @property
    def exchanges(self):
        """It provides an interface to instance attribute exchanges. It encapsulates instance attribute exchanges and provides a property Site class.

        :return: Return a property attribute of exchanges.
        """
        jexs = []
        for site in self.__sites:
            jexs.append(site.jexs)
        return numpy.array(jexs)

    @property
    def neighbors(self):
        """It provides an interface to instance attribute neighbors. It encapsulates instance attribute neighbors and provides a property Site class.

        :return: Return a property attribute of neighbors.
        """
        neighbors_ = []
        for site in self.__sites:
            neighbors_.append([nbh.index for nbh in site.neighbors])
        return numpy.array(neighbors_)
