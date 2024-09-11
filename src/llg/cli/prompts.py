from typing import Iterable, Tuple, Union

import click
from click import IntRange

from llg.core.constants import EnergyUnit
from llg.core.types import RangeDict


class Prompts:
    @staticmethod
    def ask_for_length() -> int:
        return click.prompt(
            "Insert the size of the system",
            type=IntRange(min=1),
            default=10,
        )

    @staticmethod
    def ask_for_temperature() -> Union[float, RangeDict, Iterable[float]]:
        option = click.prompt(
            "Select an option to the temperature",
            type=click.Choice(["value", "list", "dict", "file"]),
            default="value",
        )
        if option == "value":
            return float(click.prompt("Insert the temperature value"))
        elif option == "list":
            values = click.prompt("Insert the temperature values separated with spaces")
            return list(map(float, values.rstrip().rsplit(" ")))
        elif option == "dict":
            values = click.prompt(
                "Insert 'start final step' values separated with spaces"
            )
            values = list(map(float, values.rstrip().rsplit(" ")))
            start, final, step = values
            return {"start": start, "final": final, "step": step}
        elif option == "file":
            file_name = click.prompt(
                "Insert the file path with the temperatures. "
                "It should be a plain text with a value per line"
            )
            with open(file_name) as file:
                return list(map(float, file.read().split()))
        else:
            raise ValueError("Invalid option")

    @staticmethod
    def ask_for_magnetic_field_intensity() -> Union[float, RangeDict, Iterable[float]]:
        option = click.prompt(
            "Select an option to the field",
            type=click.Choice(["value", "list", "dict", "file"]),
            default="value",
        )
        if option == "value":
            return float(click.prompt("Insert the field value"))
        elif option == "list":
            values = click.prompt("Insert the field values separated with spaces")
            return list(map(float, values.rstrip().rsplit(" ")))
        elif option == "dict":
            values = click.prompt(
                "Insert 'start final step' values separated with spaces"
            )
            values = list(map(float, values.rstrip().rsplit(" ")))
            start, final, step = values
            return {"start": start, "final": final, "step": step}
        elif option == "file":
            file_name = click.prompt(
                "Insert the file with the fields. "
                "It should be a plain text with a value per line."
            )
            with open(file_name) as file:
                return list(map(float, file.read().split()))
        else:
            raise ValueError("Invalid option")

    @staticmethod
    def ask_for_energy_unit() -> EnergyUnit:
        value = click.prompt(
            "Insert the energy unit",
            type=click.Choice(["joule", "mev", "adim"]),
            default="adim",
        )
        return EnergyUnit(value)

    @staticmethod
    def ask_for_damping() -> float:
        return click.prompt("Insert the damping constant", type=float, default=0.01)

    @staticmethod
    def ask_for_gyromagnetic() -> float:
        return click.prompt("Insert the gyromagnetic constant", type=float, default=1.0)

    @staticmethod
    def ask_for_delta_time() -> float:
        return click.prompt("Insert the time step", type=float, default=0.01)

    @staticmethod
    def ask_for_jex() -> float:
        return click.prompt("Insert the exchange interaction", type=float, default=1.0)

    @staticmethod
    def ask_for_mu() -> float:
        return click.prompt("Insert the spin norms", type=float, default=1.0)

    @staticmethod
    def ask_for_magnetic_field_axis() -> Tuple[float, float, float]:
        axis = None
        while axis is None:
            values = click.prompt(
                "Insert the magnetic field axis separated with spaces"
            )
            rx, ry, rz = values.rstrip().rsplit(" ")
            axis = (float(rx), float(ry), float(rz))
            if len(axis) != 3:
                axis = None
                click.secho("Error: The magnetic field axis must have 3 components")

        return axis

    @staticmethod
    def ask_for_anisotropy_axis() -> Tuple[float, float, float]:
        axis = None
        while axis is None:
            values = click.prompt("Insert the anisotropy axis separated with spaces")
            rx, ry, rz = values.rstrip().rsplit(" ")
            axis = (float(rx), float(ry), float(rz))
            if len(axis) != 3:
                axis = None
                click.secho("Error: The anisotropy axis must have 3 components")

        return axis

    @staticmethod
    def ask_for_anisotropy_constant() -> float:
        return click.prompt("Insert the anisotropy constant", type=float, default=1.0)

    @staticmethod
    def ask_for_num_iterations() -> int:
        return click.prompt("Insert the number of iterations", type=int, default=1000)
