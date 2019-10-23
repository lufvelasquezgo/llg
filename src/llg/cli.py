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


@main.command("store-hdf")
@click.argument("output")
def store_hdf_cli(output):
    extension = output.split(".")[-1]
    if extension not in ["hdf"]:
        raise Exception("Extension does not supported !")

    with h5py.File(output, mode="w") as dataset:
        system_information = pickle.loads(eval(input()))
        num_iterations = pickle.loads(eval(input()))
        initial_state = pickle.loads(eval(input()))

        num_TH = len(system_information["temperature"])
        num_sites = system_information["num_sites"]
        dataset.attrs["num_sites"] = num_sites
        dataset.attrs["seed"] = system_information["seed"]
        dataset.attrs["units"] = system_information["parameters"]["units"]
        dataset.attrs["damping"] = system_information["parameters"]["damping"]
        dataset.attrs["gyromagnetic"] = system_information["parameters"]["gyromagnetic"]
        dataset.attrs["deltat"] = system_information["parameters"]["deltat"]
        dataset.attrs["kb"] = system_information["parameters"]["kb"]
        dataset.attrs["num_iterations"] = num_iterations
        dataset.attrs["num_TH"] = num_TH

        dataset["initial_state"] = initial_state
        dataset["temperature"] = system_information["temperature"]
        dataset["field"] = system_information["field"]

        states_dataset = dataset.create_dataset(
            "states",
            (num_TH, num_iterations, num_sites, 3),
            dtype=float,
            chunks=True,
            compression="gzip",
        )
        for i in range(num_TH):
            for j in range(num_iterations):
                state = pickle.loads(eval(input()))
                states_dataset[i, j, :] = state
