# -*- coding: utf-8 -*-

"""Console script for llg."""
import os
import pickle

import click
import numpy
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

import h5py
import moviepy.editor as mpy
from llg import Simulation, StoreHDF
from llg._tools import __ask_for_field, __ask_for_temperature
from llg.plot_states import PlotStates
from llg.predefined_structures import GenericBcc, GenericFcc, GenericSc
from tqdm import tqdm


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
@click.option(
    "--compress",
    default=False,
    is_flag=True,
    show_default=True,
    help="It reduces the overall number of bits and bytes of the file, but it takes much more time",
)
def store_hdf_cli(output, compress):
    simulation_information = pickle.loads(eval(input()))
    num_TH = simulation_information["num_TH"]
    num_iterations = simulation_information["num_iterations"]

    with StoreHDF(output, compress) as hdf5_file:
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
@click.option(
    "--by-types",
    default=False,
    is_flag=True,
    help="It allows to compute avarages by type.",
)
@click.option(
    "--components",
    default=False,
    is_flag=True,
    help="It allows to compute avarages by components.",
)
@click.option(
    "--discard",
    default=0,
    help="It allows to discard some iterations at the time to compute avarages.",
)
def compute_averages(by_types, components, discard):
    simulation_information = pickle.loads(eval(input()))

    if discard > simulation_information["num_iterations"]:
        raise Exception("Discard option should be less than the number of iterations !")

    temperature = simulation_information["temperature"]
    field = simulation_information["field"]
    types = numpy.array(simulation_information["types"])
    set_types = sorted(set(types))

    print(f"#num_TH = {simulation_information['num_TH']}")

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


@build_samples.command("generic-sc")
@click.argument("output")
@click.option("--length", default=10, help="It represents the size of the sytem")
def generic_sc(length, output):
    sample = GenericSc(length)
    sample.temperature = __ask_for_temperature()
    sample.field = __ask_for_field()
    sample.save(output)


@build_samples.command("generic-bcc")
@click.argument("output")
@click.option("--length", default=10, help="It represents the size of the sytem")
def generic_bcc(length, output):
    sample = GenericBcc(length)
    sample.temperature = __ask_for_temperature()
    sample.field = __ask_for_field()
    sample.save(output)


@build_samples.command("generic-fcc")
@click.argument("output")
@click.option("--length", default=10, help="It represents the size of the sytem")
def generic_fcc(length, output):
    sample = GenericFcc(length)
    sample.temperature = __ask_for_temperature()
    sample.field = __ask_for_field()
    sample.save(output)


@main.group("plot")
def plot():
    pass


@plot.command("plot-averages")
@click.argument("output")
def plot_averages(output):
    num_TH = int(input().split()[-1])
    header = input()
    labels = header.replace("#", "").split()

    values = {label: [] for label in labels}

    for _ in range(num_TH):
        line = input().split()
        for column, val in enumerate(line):
            val = float(val)
            values[labels[column]].append(val)

    mag_types = set(
        "_".join(label.split("_")[:2]) for label in labels if label.startswith("M")
    ) - {"M_total"}

    labels_per_page = []
    labels_per_page.append(
        sorted([label for label in labels if label.startswith("E_")])
    )
    labels_per_page.append(
        sorted([label for label in labels if label.startswith("M_total")])
    )

    for t in mag_types:
        labels_per_page.append(
            sorted([label for label in labels if label.startswith(t)])
        )

    markers = ["o", "s", "<", "*"]
    with PdfPages(output) as pdf:
        for page in tqdm(labels_per_page):
            fig = pyplot.figure(figsize=(16, 6))
            ax_temperature = fig.add_subplot(121)
            ax_field = fig.add_subplot(122)
            for i, label in enumerate(page):
                ax_temperature.plot(
                    values["temperature"], values[label], marker=markers[i], label=label
                )
                ax_field.plot(
                    values["field"], values[label], marker=markers[i], label=label
                )
            ax_temperature.set_xlabel("Temperature")
            ax_field.set_xlabel("Field")
            ax_temperature.grid()
            ax_field.grid()
            ax_temperature.legend(loc="best")
            ax_field.legend(loc="best")
            pyplot.tight_layout()
            pyplot.savefig(pdf, format="pdf")
            pyplot.close()


@plot.command("plot-states")
@click.argument("output")
@click.option(
    "--step",
    default="max",
    help="Step separation between plots. If step=max, it will be the amount of iterations.",
)
@click.option("--size", default=500, help="Figure length size in pixels.")
@click.option(
    "--mode",
    default="azimuthal",
    type=click.Choice(["azimuthal", "polar"]),
    help="Color mode",
)
@click.option(
    "--colormap",
    default="hsv",
    help="Color map. Matplotlib supported colormaps: https://matplotlib.org/examples/color/colormaps_reference.html",
)
def plot_states(output, step, size, mode, colormap):
    simulation_information = pickle.loads(eval(input()))
    num_TH = simulation_information["num_TH"]
    num_iterations = simulation_information["num_iterations"]
    positions = simulation_information["positions"]
    temperature = simulation_information["temperature"]
    field = simulation_information["field"]
    initial_state = simulation_information["initial_state"]

    if step == "max":
        step = num_iterations
    else:
        step = int(step)

    if num_iterations % step != 0:
        raise Exception("`step` is not a multiple of `num_iterations`")

    plot_state = PlotStates(positions, output, size, mode, colormap)
    plot_state.plot(initial_state, 0, None, None, save=True)
    click.secho(f"Figure was created the initial state", fg="green")

    for i in range(num_TH):
        T = temperature[i]
        H = field[i]
        for j in range(num_iterations):
            # reads
            state = pickle.loads(eval(input()))
            _ = pickle.loads(eval(input()))
            _ = pickle.loads(eval(input()))
            _ = pickle.loads(eval(input()))
            _ = pickle.loads(eval(input()))
            if (j + 1) % step == 0:
                plot_state.plot(state, j + 1, T, H, save=True)
                click.secho(
                    f"Figure was created for T={T:.2f}, H={H:.2f}, iteration={j + 1}",
                    fg="green",
                )


@plot.command("animate-states")
@click.argument("output")
@click.option(
    "--step",
    default="max",
    help="Step separation between plots. If step=max, it will be the amount of iterations.",
)
@click.option("--size", default=500, help="Figure length size in pixels.")
@click.option(
    "--mode",
    default="azimuthal",
    type=click.Choice(["azimuthal", "polar"]),
    help="Color mode",
    show_default=True,
)
@click.option(
    "--colormap",
    default="hsv",
    help="Color map. Matplotlib supported colormaps: https://matplotlib.org/examples/color/colormaps_reference.html",
)
@click.option("--fps", default=1, help="Frames per second.")
def animate_states(output, step, size, mode, colormap, fps):
    simulation_information = pickle.loads(eval(input()))
    num_TH = simulation_information["num_TH"]
    num_iterations = simulation_information["num_iterations"]
    positions = simulation_information["positions"]
    temperature = simulation_information["temperature"]
    field = simulation_information["field"]
    initial_state = simulation_information["initial_state"]

    if step == "max":
        step = num_iterations
    else:
        step = int(step)

    if num_iterations % step != 0:
        raise Exception("`step` is not a multiple of `num_iterations`")

    def image_generator():
        plot_state = PlotStates(positions, output, size, mode, colormap)
        yield plot_state.plot(initial_state, 0, None, None)

        for i in range(num_TH):
            T = temperature[i]
            H = field[i]
            for j in range(num_iterations):
                # reads
                state = pickle.loads(eval(input()))
                _ = pickle.loads(eval(input()))
                _ = pickle.loads(eval(input()))
                _ = pickle.loads(eval(input()))
                _ = pickle.loads(eval(input()))
                if (j + 1) % step == 0:
                    yield plot_state.plot(state, j + 1, T, H)

    def make_frame(t):
        return next(generator)

    # plus 1 due to the initial state.
    duration = (num_TH * (num_iterations // step) + 1) / fps

    generator = image_generator()
    animation = mpy.VideoClip(make_frame, duration=duration)

    # the generator should be reseted due the in the VideoClip init, the make_frame
    # function is called one time.
    generator = image_generator()

    _, output_extension = os.path.splitext(output)
    if output_extension == ".gif":
        animation.write_gif(output, fps=fps)
    else:
        animation.write_videofile(output, fps=fps)
