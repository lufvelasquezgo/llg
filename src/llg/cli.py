# -*- coding: utf-8 -*-

"""Console script for llg."""
import click
from llg import Simulation, StoreHDF
from llg.predefined_structures import GenericBcc
import pickle
import h5py
import numpy
from llg._tools import __ask_for_field, __ask_for_temperature


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


@main.command("compute-averages")
@click.option("--by-types", default=False, is_flag=True)
@click.option("--components", default=False, is_flag=True)
@click.option("--discard", default=0)
def compute_averages(by_types, components, discard):
    simulation_information = pickle.loads(eval(input()))
    
    if discard > simulation_information["num_iterations"]:
        raise Exception("Discard option should be less than the number of iterations !")

    temperature = simulation_information["temperature"]
    field = simulation_information["field"]
    types = numpy.array(simulation_information["types"])
    set_types = sorted(set(types))

    header = "#temperature field E_exchange E_anisotropy E_field E_total M_total"
    if components:
        header += " M_total_x M_total_y M_total_z"

    if by_types:
        for t in set_types:
            header += f" M_{t}"
            if components:
                header += f" M_{t}_x M_{t}_y M_{t}_z"

    print(header)

    num_TH = simulation_information["num_TH"]
    num_iterations = simulation_information["num_iterations"]

    for i in range(num_TH):
        state_arr = []
        exchange_energy_arr = []
        anisotropy_energy_arr = []
        magnetic_energy_arr = []
        total_energy_arr = []

        for j in range(num_iterations):
            # reads
            state = pickle.loads(eval(input()))
            exchange_energy = pickle.loads(eval(input()))
            anisotropy_energy = pickle.loads(eval(input()))
            magnetic_energy = pickle.loads(eval(input()))
            total_energy = pickle.loads(eval(input()))

            if j >= discard:
                state_arr.append(state)
                exchange_energy_arr.append(exchange_energy)
                anisotropy_energy_arr.append(anisotropy_energy)
                magnetic_energy_arr.append(magnetic_energy)
                total_energy_arr.append(total_energy)

        state_arr = numpy.array(state_arr)

        E_exchange = numpy.mean(exchange_energy_arr)
        E_anisotropy = numpy.mean(anisotropy_energy_arr)
        E_field = numpy.mean(magnetic_energy_arr)
        E_total = numpy.mean(total_energy_arr)

        M_total = numpy.mean(numpy.linalg.norm(numpy.mean(state_arr, axis=1), axis=1))

        if components:
            M_total_x, M_total_y, M_total_z = numpy.mean(
                numpy.mean(state_arr, axis=1), axis=0
            )

        mag_by_types = {}
        mag_x_by_types = {}
        mag_y_by_types = {}
        mag_z_by_types = {}
        if by_types:
            for t in set_types:
                mag_by_types[t] = numpy.mean(
                    numpy.linalg.norm(
                        numpy.mean(state_arr[:, types == t, :], axis=1), axis=1
                    )
                )
                if components:
                    mag = numpy.mean(
                        numpy.mean(state_arr[:, types == t, :], axis=1), axis=0
                    )
                    mag_x_by_types[t], mag_y_by_types[t], mag_z_by_types[t] = mag

        output = f"{temperature[i]} {field[i]} {E_exchange} {E_anisotropy} {E_field} {E_total} {M_total}"
        if components:
            output += f" {M_total_x} {M_total_y} {M_total_z}"

        if by_types:
            for t in set_types:
                output += f" {mag_by_types[t]}"
                if components:
                    output += (
                        f" {mag_x_by_types[t]} {mag_y_by_types[t]} {mag_z_by_types[t]}"
                    )

        print(output)



@main.group("build-samples")
def build_samples():
    pass


@build_samples.command("generic-bcc")
@click.argument("output")
@click.option("--length", default=10)
def generic_bcc(length, output):
    sample = GenericBcc(length)
    sample.temperature = __ask_for_temperature()
    sample.field = __ask_for_field()
    sample.save(output)
