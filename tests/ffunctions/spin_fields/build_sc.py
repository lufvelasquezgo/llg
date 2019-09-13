import numpy
from itertools import product
from collections import defaultdict


def build_sc(l):
    sites = list()
    index = dict()
    for x, y in product(range(l), range(l)):
        site = x, y
        sites.append(site)
        index[site] = sites.index(site)

    num_sites = len(sites)
    neigh = defaultdict(list)

    for site in sites:
        x, y = site
        neigh[site].append(sites.index(((x+1) % l, y)))
        neigh[site].append(sites.index(((x-1) % l, y)))
        neigh[site].append(sites.index((x, (y+1) % l)))
        neigh[site].append(sites.index((x, (y-1) % l)))

    neighbors_indexes = list()
    num_neighbors = list()
    for neighs in neigh.values():
        neighbors_indexes += neighs
        num_neighbors.append(len(neighs))
    
    num_interactions = len(neighbors_indexes)

    return num_sites, num_interactions, neighbors_indexes, num_neighbors
