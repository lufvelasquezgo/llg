from typing import Type

import click
from click import Group

from llg.cli.prompts import Prompts
from llg.core.generic_system_builders.body_centered_cubic_system import (
    BodyCenteredCubicSystem,
)
from llg.core.generic_system_builders.face_centered_cubic_system import (
    FaceCenteredCubicSystem,
)
from llg.core.generic_system_builders.generic_system import GenericSystem
from llg.core.generic_system_builders.simple_cubic_system import SimpleCubicSystem


@click.group("build-samples", help="Build simple generic systems to simulate")
def build_generic_system() -> Group:
    pass


@build_generic_system.command("simple-cubic", help="Build a simple cubic sample")
@click.argument("output")
def generic_simple_cubic(output: str):
    system = _build_generic_system(SimpleCubicSystem)
    system.save(output)


@build_generic_system.command("body-centered-cubic")
@click.argument("output")
def generic_body_centered_cubic(output):
    system = _build_generic_system(BodyCenteredCubicSystem)
    system.save(output)


@build_generic_system.command("face-centered-cubic")
@click.argument("output")
def generic_face_centered_cubic(output):
    system = _build_generic_system(FaceCenteredCubicSystem)
    system.save(output)


def _build_generic_system(generic_system_class: Type[GenericSystem]) -> GenericSystem:
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

    return generic_system_class(
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
