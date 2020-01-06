import click


def __ask_for_temperature():
    """It is a function which asks for valid input according to the ``confirm()`` function. It asks for confirmation (yes/no) about if the user want to insert some values for temperature.
    """
    click.secho(
        "Your sample file will not contain a valid value for temperature.", fg="yellow"
    )
    if click.confirm("Do you want to insert some values ?", default=True):
        option = click.prompt(
            "Select an option to the temperature",
            type=click.Choice(["value", "list", "dict", "file"]),
            default="value",
        )
        if option == "value":
            values = float(click.prompt("Insert the temperature value"))
        elif option == "list":
            values = click.prompt("Insert the temperature values separated with spaces")
            values = list(map(float, values.rstrip().rsplit(" ")))
        elif option == "dict":
            values = click.prompt(
                "Insert 'start final step' values separated with spaces"
            )
            values = list(map(float, values.rstrip().rsplit(" ")))
            values = {"start": values[0], "final": values[1], "step": values[2]}
        elif option == "file":
            file_name = click.prompt("Insert the file with the temperatures")
            with open(file_name) as file:
                values = list(map(float, file.read().split()))

        return values
    return None


def __ask_for_field():
    """It is a function which asks for valid input according to the ``confirm()`` function. It asks for confirmation (yes/no) about if the user want to insert some values for field.
    """
    click.secho(
        "Your sample file will not contain a valid value for field.", fg="yellow"
    )
    if click.confirm("Do you want to insert some values ?", default=True):
        option = click.prompt(
            "Select an option to the field",
            type=click.Choice(["value", "list", "dict", "file"]),
            default="value",
        )
        if option == "value":
            values = float(click.prompt("Insert the field value"))
        elif option == "list":
            values = click.prompt("Insert the field values separated with spaces")
            values = list(map(float, values.rstrip().rsplit(" ")))
        elif option == "dict":
            values = click.prompt(
                "Insert 'start final step' values separated with spaces"
            )
            values = list(map(float, values.rstrip().rsplit(" ")))
            values = {"start": values[0], "final": values[1], "step": values[2]}
        elif option == "file":
            file_name = click.prompt("Insert the file with the fields")
            with open(file_name) as file:
                values = list(map(float, file.read().split()))

        return values
    return None
