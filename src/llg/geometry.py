from llg import Site
import json
from collections import namedtuple


class Geometry:
    def __init__(self, sites):
        self.__sites = sites

    @classmethod
    def from_file(cls, geometry_file):
        with open(geometry_file) as file:
            geometry = json.load(file)["geometry"]

        return Geometry.from_dict(geometry)

    @classmethod
    def from_dict(cls, geometry_dict):
        sites = geometry_dict["sites"]
        neighbors = geometry_dict["neighbors"]

        sites = Geometry.read_sites(sites)
        # dictionary with the indexes as keys but the values are the same objects,
        # such as, if we alter `sites_dict` values, we also alter the corresponding
        # one in `sites`.
        sites_dict = {site.index: site for site in sites}

        neighbors = Geometry.read_neighbors(neighbors)

        for link in neighbors:
            site = sites_dict[link.source]
            nhb = sites_dict[link.target]
            site.append_neighbor(nhb, link.jex)

        return cls(sites)

    @property
    def positions(self):
        return [site.position for site in self.__sites]

    @property
    def types(self):
        return [site.type for site in self.__sites]

    @staticmethod
    def read_sites(site_dicts: list):
        output_sites = []
        for site_dict in site_dicts:
            site = Site.from_dict(site_dict)
            if site in output_sites:
                raise Exception(f"Site with the index {site.index} already exists !!!")
            output_sites.append(site)
        return output_sites

    @staticmethod
    def read_neighbors(neighbors_dicts: list):
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
        count = 0
        for site in self.__sites:
            count += len(site.neighbors)
        return count

    @property
    def num_sites(self):
        return len(self.__sites)

    @property
    def spin_norms(self):
        return [site.mu for site in self.__sites]

    @property
    def field_axes(self):
        return [site.field_axis for site in self.__sites]

    @property
    def num_neighbors(self):
        return [len(site.neighbors) for site in self.__sites]

    @property
    def anisotropy_constants(self):
        return [site.anisotropy_constant for site in self.__sites]

    @property
    def anisotropy_axes(self):
        return [site.anisotopy_axis for site in self.__sites]

    @property
    def exchanges(self):
        jexs = []
        for site in self.__sites:
            jexs.extend(site.jexs)
        return jexs

    @property
    def neighbors(self):
        neighbors_ = []
        for site in self.__sites:
            neighbors_.extend([nbh.index for nbh in site.neighbors])
        return neighbors_
