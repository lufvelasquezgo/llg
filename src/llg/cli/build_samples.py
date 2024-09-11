import click
from click import Group

from llg.cli.prompts import Prompts
from llg.core.predefined_samples_builders.simple_cubic_system import SimpleCubicSystem
from llg.core.predefined_structures import GenericBcc, GenericFcc


@click.group("build-samples", help="Build simple samples for simulations")
def build_samples() -> Group:
    pass


@build_samples.command("simple-cubic", help="Build a simple cubic sample")
@click.argument("output")
def generic_sc(output: str):
    length = Prompts.ask_for_length()
    temperature = Prompts.ask_for_temperature()
    magnetic_field_intensity = Prompts.ask_for_magnetic_field_intensity()
    energy_unit = Prompts.ask_for_energy_unit()
    damping = Prompts.ask_for_damping()
    gyromagnetic = Prompts.ask_for_gyromagnetic()
    delta_time = Prompts.ask_for_delta_time()
    jex = Prompts.ask_for_jex()
    mu = Prompts.ask_for_mu()
    magnetic_field_axis = Prompts.ask_for_magnetic_field_axis()
    anisotropy_axis = Prompts.ask_for_anisotropy_axis()
    anisotropy_constant = Prompts.ask_for_anisotropy_constant()
    num_iterations = Prompts.ask_for_num_iterations()

    sample = SimpleCubicSystem(
        length,
        temperature,
        magnetic_field_intensity,
        energy_unit,
        damping,
        gyromagnetic,
        delta_time,
        jex,
        mu,
        magnetic_field_axis,
        anisotropy_axis,
        anisotropy_constant,
        num_iterations,
    )
    sample.save(output)


@build_samples.command("body-centered-cubic")
@click.argument("output")
@click.option("--length", default=10, help="It represents the size of the sytem")
def generic_bcc(length, output):
    sample = GenericBcc(length)
    sample.temperature = Prompts.ask_for_temperature()
    sample.field = Prompts.ask_for_magnetic_field_axis()
    sample.save(output)


@build_samples.command("face-centered-cubic")
@click.argument("output")
@click.option("--length", default=10, help="It represents the size of the sytem")
def generic_fcc(length, output):
    sample = GenericFcc(length)
    sample.temperature = Prompts.ask_for_temperature()
    sample.field = Prompts.ask_for_magnetic_field_intensity()
    sample.save(output)
