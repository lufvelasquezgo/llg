# -*- coding: utf-8 -*-

"""Console script for llg."""
import sys
import click
import json
import numpy
from matplotlib import pyplot, style
from tqdm import tqdm
from llg.ffunctions import heun, mag_functions
import random
from numbers import Real
from collections import defaultdict
from collections import namedtuple

style.use("classic")


def build_values(structure):
    if isinstance(structure, dict):
        start = structure["start"]
        final = structure["final"]
        step = structure["step"]
        step = numpy.sign(final - start) * abs(step)
        return numpy.arange(start, final + step, step)
    elif isinstance(structure, list):
        return structure
    elif isinstance(structure, Real):
        return [structure, ]
    else:
        raise Exception("No supported format.")


def read_geometry(geometry):
    geometry = {site["index"]: site for site in geometry}
    indexes = sorted(geometry.keys())

    positions = []
    types = []
    spin_norms = []
    field_axes = []
    anisotropy_constants = []
    anisotropy_axes = []
    for index in indexes:
        site = geometry[index]

        positions.append(site["position"])
        types.append(site.get("type", "generic"))
        spin_norms.append(site.get("mu", 1.0))
        anisotropy_constants.append(site.get("anisotropy_constant", 0.0))
        anisotropy_axes.append(site.get("anisotopy_axis", [0.0, 0.0, 1.0]))
        field_axes.append(site.get("field_axis", [0.0, 0.0, 1.0]))

    return {
        "num_sites": len(geometry),
        "num_types": len(set(types)),
        "indexes": numpy.array(indexes),
        "positions": numpy.array(positions),
        "spin_norms": numpy.array(spin_norms),
        "field_axes": numpy.array(field_axes),
        "types": numpy.array(types),
        "anisotropy_constants": numpy.array(anisotropy_constants),
        "anisotropy_axes": numpy.array(anisotropy_axes),
    }


def read_neighbors(links):
    Link = namedtuple("Link", ["source", "target", "jex"])

    dict_neighbors = defaultdict(list)
    for link in links:
        source = link["source"]
        target = link["target"]
        jex = link["jex"]

        dict_neighbors[source].append(Link(source=source, target=target, jex=jex))

    j_exchanges = []
    num_neighbors = []
    neighbors = []
    indexes = sorted(dict_neighbors.keys())
    for index in indexes:
        links_index = dict_neighbors[index]
        num_neighbors.append(len(links_index))
        for link in links_index:
            j_exchanges.append(link.jex)
            neighbors.append(link.target)

    return {
        "num_interactions": len(links),
        "j_exchanges": j_exchanges,
        "num_neighbors": num_neighbors,
        "neighbors": neighbors,
    }

def get_random_state(num_sites):
    random_state = numpy.random.normal(size=(num_sites, 3))
    norms = numpy.linalg.norm(random_state, axis=1)
    random_state = [vec / norms[i] for i, vec in enumerate(random_state)]
    return random_state

def match_sizes(arr1, arr2):
    if len(arr1) == len(arr2):
        return arr1, arr2
    
    if len(arr1) < len(arr2):
        while len(arr1) < len(arr2):
            arr1 = arr1 * 2
        return arr1[:len(arr2)], arr2
    
    if len(arr2) < len(arr1):
        while len(arr2) < len(arr1):
            arr2 = arr2 * 2
        return arr1, arr2[:len(arr1)]

@click.command()
@click.argument("file")
def main(file, args=None):
    """Console script for llg."""
    with open(file, "r") as parameters:
        data = json.load(parameters)

    num_iterations = data.get("parameters", {}).get("num_iterations", 1)
    damping = data.get("parameters", {}).get("damping", 1.0)
    gyromagnetic = data.get("parameters", {}).get("gyromagnetic", 1.0)
    deltat = data.get("parameters", {}).get("deltat", 1.0)
    units = data.get("parameters", {}).get("units", None)

    temperatures = build_values(data.get("temperature", 0.0))
    fields = build_values(data.get("field", 0.0))

    temperatures, fields = match_sizes(temperatures, fields)

    seed = data.get("seed", random.getrandbits(32))

    if units == "mev":
        kb = 0.08618
    elif units == "joules":
        kb = 1.38064852e-23
    else:
        kb = 1.0


    sample_info = read_geometry(data["geometry"])
    num_sites = sample_info["num_sites"]
    spin_norms = sample_info["spin_norms"]
    field_axes = sample_info["field_axes"]
    anisotropy_constants = sample_info["anisotropy_constants"]
    anisotropy_axes = sample_info["anisotropy_axes"]
    
    neighbors_info = read_neighbors(data["neighbors"])
    j_exchanges = neighbors_info["j_exchanges"]
    num_neighbors = neighbors_info["num_neighbors"]
    neighbors = neighbors_info["neighbors"]
    
    state = data.get("initial_state", get_random_state(num_sites))
    

    for T, H in zip(temperatures, fields):
        temperatures_sites = [T] * num_sites
        fields_sites = [H] * num_sites
        mx_arr = []
        my_arr = []
        mz_arr = []

        for i in tqdm(range(num_iterations)):
            random_normal_matrix = numpy.random.normal(size=(num_sites, 3))
            state = heun.integrate(
                state,
                spin_norms,
                random_normal_matrix,
                temperatures_sites,
                damping,
                deltat,
                gyromagnetic,
                kb,
                fields_sites,
                field_axes,
                j_exchanges,
                num_neighbors,
                neighbors,
                anisotropy_constants,
                anisotropy_axes,
            )
            mx, my, mz = mag_functions.magnetization_vector(state)
            mx_arr.append(mx)
            my_arr.append(my)
            mz_arr.append(mz)
            

        pyplot.figure()
        pyplot.plot(mx_arr, label="mx")
        pyplot.plot(my_arr, label="my")
        pyplot.plot(mz_arr, label="mz")
        pyplot.legend(loc="best")
        pyplot.ylim(0, 1)
        pyplot.savefig("magnetization.pdf")
        pyplot.close()

    # click.echo("Replace this message by putting your code into "
    #            "llg.cli.main")
    # click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
