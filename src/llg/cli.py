# -*- coding: utf-8 -*-

"""Console script for llg."""
import click
from llg import Simulation
import sys
import pickle


@click.command()
@click.argument("file", type=click.Path(exists=True))
def main(file, args=None):
    """Console script for llg."""
    simulation = Simulation.from_file(file)
    print(pickle.dumps(simulation.system.information))
    print(pickle.dumps(simulation.num_iterations))
    print(pickle.dumps(simulation.initial_state))
    for state in simulation.run():
        print(pickle.dumps(state))

    # click.echo("Replace this message by putting your code into "
    #            "llg.cli.main")
    # click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    main()
