# -*- coding: utf-8 -*-

"""Console script for llg."""
import click
import numpy
from matplotlib import pyplot
from tqdm import tqdm
from llg.ffunctions import heun, mag_functions

from llg import System


def get_random_state(num_sites):
    random_state = numpy.random.normal(size=(num_sites, 3))
    norms = numpy.linalg.norm(random_state, axis=1)
    random_state = [vec / norms[i] for i, vec in enumerate(random_state)]
    return random_state


@click.command()
@click.argument("file", type=click.Path(exists=True))
def main(file, args=None):
    """Console script for llg."""
    system = System.from_file(file)

    spin_norms = system.geometry.spin_norms
    damping = system.damping
    deltat = system.deltat
    gyromagnetic = system.gyromagnetic
    kb = system.kb
    field_axes = system.geometry.field_axes
    j_exchanges = system.geometry.exchanges
    num_neighbors = system.geometry.num_neighbors
    neighbors = system.geometry.neighbors
    anisotropy_constants = system.geometry.anisotropy_constants
    anisotropy_axes = system.geometry.anisotropy_axes
    num_sites = system.geometry.num_sites
    state = [[1.0, 0.0, 0.0]] * num_sites

    for T, H in zip(system.temperatures, system.fields):
        print(T, H)
        temperatures_sites = [T] * num_sites
        fields_sites = [H] * num_sites
        mx_arr = []
        my_arr = []
        mz_arr = []

        for i in tqdm(range(10000)):
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
    main()
