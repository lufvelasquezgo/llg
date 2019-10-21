# -*- coding: utf-8 -*-

"""Console script for llg."""
import click
from llg import Simulation
import sys
import pickle
import h5py


@click.group()
def main():
    """Console script for llg."""
    pass


@main.command("simulate")
@click.argument("configuration_file")
def simulate(configuration_file):
    simulation = Simulation.from_file(configuration_file)
    print(pickle.dumps(simulation.system.information))
    print(pickle.dumps(simulation.num_iterations))
    print(pickle.dumps(simulation.initial_state))
    for state in simulation.run():
        print(pickle.dumps(state))

    # click.echo("Replace this message by putting your code into "
    #            "llg.cli.main")
    # click.echo("See click documentation at http://click.pocoo.org/")


@main.command("store")
@click.argument("output")
def store_cli(output):
    extension = output.split(".")[-1]
    if extension not in ["hdf"]:
        raise Exception("Extension does not supported !")

    with h5py.File(output, mode="w") as data_file:

        system_information = pickle.loads(eval(input()))
        num_iterations = pickle.loads(eval(input()))
        initial_state = pickle.loads(eval(input()))

        for _ in range(num_iterations):
            state = pickle.loads(eval(input()))

        print(system_information)


if __name__ == "__main__":
    store()
