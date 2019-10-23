# -*- coding: utf-8 -*-

"""Console script for llg."""
import click
from llg import Simulation, StoreHDF
import pickle


@click.group()
def main():
    """Console script for llg."""
    pass


@main.command("simulate")
@click.argument("configuration_file")
def simulate(configuration_file):
    simulation = Simulation.from_file(configuration_file)
    print(pickle.dumps(simulation.information))
    for state in simulation.run():
        print(pickle.dumps(state))


@main.command("store-hdf")
@click.argument("output")
def store_hdf_cli(output):
    extension = output.split(".")[-1]
    if extension not in ["hdf"]:
        raise Exception("Extension does not supported !")

    simulation_information = pickle.loads(eval(input()))
    num_TH = simulation_information["num_TH"]
    num_iterations = simulation_information["num_iterations"]

    with StoreHDF(output) as hdf5_file:
        hdf5_file.populate(simulation_information)

        for i in range(num_TH):
            for j in range(num_iterations):
                state = pickle.loads(eval(input()))
                hdf5_file.store_state(state, i, j)
