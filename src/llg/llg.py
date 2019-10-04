# -*- coding: utf-8 -*-
"""Main module."""

from collections import defaultdict
import numpy


def read_sample_file(file):
    indexes = []
    position = []
    spin_norm = []
    field_dir = []
    types = []
    initial_state = []
    j_exchange = []
    num_neighbors = []
    neighbors = []

    with open(file, "r") as input_file:
        lines = input_file.readlines()
        num_sites, num_interactions, num_types = list(
            map(int, lines[0].split(" ")))
        for i in range(1, num_types + 1):
            types.append(lines[i].replace("\n", ""))

        for i in range(num_types + 1, num_types + num_sites + 1):
            line = lines[i].split(" ")
            indexes.append(int(line[0]))
            position.append([float(line[1]), float(line[2]), float(line[3])])
            spin_norm.append(float(line[4]))
            field_dir.append([float(line[5]), float(line[6]), float(line[7])])
            types.append(str(line[8]))
            initial_state.append(
                [float(line[9]), float(line[10]), float(line[11])])

        dict_neighbors = defaultdict(list)
        for i in range(num_types + num_sites + 1, num_types + num_sites + num_interactions + 1):
            line = lines[i].split(" ")
            dict_neighbors[line[0]].append(line[1])
            neighbors.append(float(line[1]))
            j_exchange.append(float(line[2]))

    for site in dict_neighbors.keys():
        num_neighbors.append(len(dict_neighbors[site]))

    output = {
        "num_sites": num_sites,
        "num_interactions": num_interactions,
        "num_types": num_types,
        "indexes": numpy.array(indexes),
        "position": numpy.array(position),
        "spin_norm": numpy.array(spin_norm),
        "field_dir": numpy.array(field_dir),
        "types": numpy.array(types),
        "initial_state": numpy.array(initial_state),
        "j_exchange": numpy.array(j_exchange),
        "num_neighbors": numpy.array(num_neighbors),
        "neighbors": numpy.array(neighbors)
    }
    return output
