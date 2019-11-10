# -*- coding: utf-8 -*-

"""Console script for llg."""
import click
from llg import Simulation, StoreHDF
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
    print(pickle.dumps(simulation.information))
    for values in simulation.run():
        (
            state,
            exchange_energy,
            anisotropy_energy,
            magnetic_energy,
            total_energy,
        ) = values
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


@main.command("read-hdf")
@click.argument("file")
def read_hdf(file):
    with h5py.File(file, mode="r") as dataset:
        simulation_information = {
            "num_sites": dataset.attrs["num_sites"],
            "parameters": {
                "units": dataset.attrs["units"],
                "damping": dataset.attrs["damping"],
                "gyromagnetic": dataset.attrs["gyromagnetic"],
                "deltat": dataset.attrs["deltat"],
                "kb": dataset.attrs["deltat"],
            },
            "temperature": dataset["temperature"][:],
            "field": dataset["field"][:],
            "seed": dataset.attrs["seed"],
            "num_iterations": dataset.attrs["num_iterations"],
            "positions": dataset["positions"][:],
            "types": dataset["types"][:],
            "initial_state": dataset["initial_state"][:],
            "num_TH": dataset.attrs["num_TH"],
        }
        print(pickle.dumps(simulation_information))

        for i in range(dataset.attrs["num_TH"]):
            for j in range(dataset.attrs["num_iterations"]):
                print(pickle.dumps(dataset["states"][i, j]))
                print(pickle.dumps(dataset["exchange_energy"][i, j]))
                print(pickle.dumps(dataset["anisotropy_energy"][i, j]))
                print(pickle.dumps(dataset["magnetic_energy"][i, j]))
                print(pickle.dumps(dataset["total_energy"][i, j]))
