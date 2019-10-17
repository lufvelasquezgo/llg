import click


@click.command()
@click.argument("sample_file", type=click.Path(exists=True))
def read_sample(sample_file):
    pass
