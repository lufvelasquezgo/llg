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
    print(pickle.dumps(simulation.system.information))
    print(pickle.dumps(simulation.num_iterations))
    print(pickle.dumps(simulation.system.geometry.positions))
    print(pickle.dumps(simulation.system.geometry.types))
    print(pickle.dumps(simulation.initial_state))
    for state in simulation.run():
        print(pickle.dumps(state))


@main.command("store-hdf")
@click.argument("output")
def store_hdf_cli(output):
    extension = output.split(".")[-1]
    if extension not in ["hdf"]:
        raise Exception("Extension does not supported !")

    system_information = pickle.loads(eval(input()))
    num_iterations = pickle.loads(eval(input()))
    positions = pickle.loads(eval(input()))
    types = pickle.loads(eval(input()))
    initial_state = pickle.loads(eval(input()))

    with StoreHDF(output) as hdf5_file:
        hdf5_file.store_attributes(system_information)
        hdf5_file.store_types(types)

        hdf5_file.store_positions(positions)
        hdf5_file.store_initial_state(initial_state)
        hdf5_file.store_temperature(system_information["temperature"])
        hdf5_file.store_field(system_information["field"])

        hdf5_file.create_states(
            len(system_information["temperature"]),
            num_iterations,
            system_information["num_sites"],
        )

        for i in range(len(system_information["temperature"])):
            for j in range(num_iterations):
                state = pickle.loads(eval(input()))
                hdf5_file.store_state(state, i, j)
