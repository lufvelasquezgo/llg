import numpy
import click
import yaml
from itertools import product
from collections import defaultdict


@click.command()
@click.option("-length", default=7)
def main(length):
    sites = list()
    types = dict()
    mub = 5.788e-2
    jex = 44.01
    mus = 2.22 * mub
    field_dir = [0, 0, 1]
    for x, y, z in product(range(length), repeat=3):
        sites.append((x, y, z))
        sites.append((x + 0.5, y + 0.5, z + 0.5))

    num_sites = len(sites)

    initial_state = numpy.random.normal(size=(num_sites, 3))
    initial_state /= numpy.linalg.norm(initial_state, axis=1)[:, numpy.newaxis]

    nhbs_dict = defaultdict(list)
    for site in sites:
        x, y, z = site
        types[site] = "Fe"
        nhbs_dict[site].append(sites.index(
            ((x + 0.5) % length, (y + 0.5) % length, (z + 0.5) % length)))
        nhbs_dict[site].append(sites.index(
            ((x + 0.5) % length, (y + 0.5) % length, (z - 0.5) % length)))
        nhbs_dict[site].append(sites.index(
            ((x + 0.5) % length, (y - 0.5) % length, (z + 0.5) % length)))
        nhbs_dict[site].append(sites.index(
            ((x + 0.5) % length, (y - 0.5) % length, (z - 0.5) % length)))
        nhbs_dict[site].append(sites.index(
            ((x - 0.5) % length, (y + 0.5) % length, (z + 0.5) % length)))
        nhbs_dict[site].append(sites.index(
            ((x - 0.5) % length, (y + 0.5) % length, (z - 0.5) % length)))
        nhbs_dict[site].append(sites.index(
            ((x - 0.5) % length, (y - 0.5) % length, (z + 0.5) % length)))
        nhbs_dict[site].append(sites.index(
            ((x - 0.5) % length, (y - 0.5) % length, (z - 0.5) % length)))

    neighbors = list()
    num_neighbors = list()
    for nhbs in nhbs_dict.values():
        neighbors += nhbs
        num_neighbors.append(len(nhbs))

    num_interactions = sum(num_neighbors)
    num_types = len(set(types.values()))

    outname = "sample.dat"
    with open(outname, "w") as outfile:
        outfile.write(f"{num_sites} {num_interactions} {num_types}\n")
        for t in set(types.values()):
            outfile.write(f"{t}\n")

        for i, site in enumerate(sites):
            outfile.write(
                "{} {} {} {} {} {} {} {} {} {} {} {}\n".format(i, *site, mus, *field_dir, types[site], *initial_state[i]))

        for i, site in enumerate(sites):
            for nhb in nhbs_dict[site]:
                outfile.write("{} {} {}\n".format(i, nhb, jex))

    parameters = {
        "sample": outname,
        "num_iterations": 1000,
    }

    with open("parameters.yml", "w") as outfile:
        yaml.dump(parameters, outfile, default_flow_style=False)


if __name__ == "__main__":
    main()
