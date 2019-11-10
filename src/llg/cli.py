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
    for values in simulation.run():
        state, exchange_energy, anisotropy_energy, magnetic_energy, total_energy = (
            values
        )
        print(pickle.dumps(state))
        print(pickle.dumps(exchange_energy))
        print(pickle.dumps(anisotropy_energy))
        print(pickle.dumps(magnetic_energy))
        print(pickle.dumps(total_energy))


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
                # reads
                state = pickle.loads(eval(input()))
                exchange_energy = pickle.loads(eval(input()))
                anisotropy_energy = pickle.loads(eval(input()))
                magnetic_energy = pickle.loads(eval(input()))
                total_energy = pickle.loads(eval(input()))

                # stores
                hdf5_file.store_state(state, i, j)
                hdf5_file.store_exchange_energy(exchange_energy, i, j)
                hdf5_file.store_anisotropy_energy(anisotropy_energy, i, j)
                hdf5_file.store_magnetic_energy(magnetic_energy, i, j)
                hdf5_file.store_total_energy(total_energy, i, j)
