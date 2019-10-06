# -*- coding: utf-8 -*-

"""Console script for llg."""
import sys
import click
import yaml
import numpy
from matplotlib import pyplot, style
from tqdm import tqdm
from llg.llg import read_sample_file
from llg.ffunctions import heun, mag_functions
style.use("classic")


@click.command()
@click.argument("file")
def main(file, args=None):
    """Console script for llg."""
    with open(file, "r") as parameters:
        try:
            data = yaml.safe_load(parameters)
        except yaml.YAMLError as exc:
            print(exc)

    sample_file = data.get("sample")
    anisotropy_file = data.get("anisotropy", None)
    num_iterations = data.get("num_iterations", 1)
    damping = data.get("damping", 1.0)
    gyromagnetic = data.get("gyromagnetic", 1.76e11)
    deltat = data.get("deltat", 1e-15)
    H = data.get("field", 0)
    T = data.get("temperature", 10)
    seed = data.get("seed", 696969)
    units = data.get("units", "mev")
    skipping = data.get("skipping", 1)

    if units == "mev":
        kb = 0.08618
    elif units == "joules":
        kb = 1.38064852e-23
    else:
        kb = 1.0

    sample_info = read_sample_file(sample_file)
    num_sites = sample_info["num_sites"]
    num_interactions = sample_info["num_interactions"]
    state = sample_info["initial_state"]
    spin_moment = sample_info["spin_norm"]
    temperature = [T] * num_sites
    field_int = [H] * num_sites
    field_dir = sample_info["field_dir"]
    j_exchange = sample_info["j_exchange"]
    num_neighbors = sample_info["num_neighbors"]
    neighbors = sample_info["neighbors"]

    if not anisotropy_file:
        anis_const = [0.0] * num_sites
        anis_vect = [[0, 0, 1]] * num_sites

    magnetization_arr = []
    for i in tqdm(range(num_iterations)):
        matrix = numpy.random.normal(size=(num_sites, 3))
        state = heun.integrate(state, spin_moment, matrix,
                               temperature, damping, deltat, gyromagnetic, kb,
                               field_int, field_dir, j_exchange, num_neighbors,
                               neighbors, anis_const, anis_vect)
        mag = mag_functions.total_magnetization(state)
        magnetization_arr.append(mag)

    pyplot.figure()
    pyplot.plot(magnetization_arr)
    pyplot.ylim(0, 1)
    pyplot.savefig("magnetization.pdf")
    pyplot.close()

    # click.echo("Replace this message by putting your code into "
    #            "llg.cli.main")
    # click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
