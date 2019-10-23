import numpy
import click
import json
from itertools import product
from collections import defaultdict


@click.command()
@click.option("-length", default=15)
def main(length):
    sites = list()
    types = dict()
    mub = 5.788e-2
    jex = 44.01
    mus = 2.22 * mub
    field_dir = [0.0, 0.0, 1.0]
    kv = 0.0
    kv_axis = [0.0, 0.0, 1.0]
    for x, y, z in product(range(length), repeat=3):
        sites.append((x, y, z))
        sites.append((x + 0.5, y + 0.5, z + 0.5))

    nhbs_dict = defaultdict(list)
    for site in sites:
        x, y, z = site
        types[site] = "Fe"
        nhbs_dict[site].append(
            sites.index(((x + 0.5) % length, (y + 0.5) % length, (z + 0.5) % length))
        )
        nhbs_dict[site].append(
            sites.index(((x + 0.5) % length, (y + 0.5) % length, (z - 0.5) % length))
        )
        nhbs_dict[site].append(
            sites.index(((x + 0.5) % length, (y - 0.5) % length, (z + 0.5) % length))
        )
        nhbs_dict[site].append(
            sites.index(((x + 0.5) % length, (y - 0.5) % length, (z - 0.5) % length))
        )
        nhbs_dict[site].append(
            sites.index(((x - 0.5) % length, (y + 0.5) % length, (z + 0.5) % length))
        )
        nhbs_dict[site].append(
            sites.index(((x - 0.5) % length, (y + 0.5) % length, (z - 0.5) % length))
        )
        nhbs_dict[site].append(
            sites.index(((x - 0.5) % length, (y - 0.5) % length, (z + 0.5) % length))
        )
        nhbs_dict[site].append(
            sites.index(((x - 0.5) % length, (y - 0.5) % length, (z - 0.5) % length))
        )

    neighbors = list()
    num_neighbors = list()
    for nhbs in nhbs_dict.values():
        neighbors += nhbs
        num_neighbors.append(len(nhbs))

    sample = {
        "geometry": {"sites": [], "neighbors": []},
        "parameters": {
            "units": "mev",
            "damping": 1.0,
            "gyromagnetic": 1.76e11,
            "deltat": 1e-15,
        },
        "temperature": [0.0] * 2,
        "field": [10.0] * 2,
        "seed": 696969,
        "initial_state": [],
        "num_iterations": 1000,
    }

    for i, site in enumerate(sites):
        sample["geometry"]["sites"].append(
            {
                "index": i,
                "position": list(site),
                "type": types[site],
                "mu": mus,
                "anisotropy_constant": kv,
                "anisotopy_axis": kv_axis,
                "field_axis": field_dir,
            }
        )

    for i, site in enumerate(sites):
        for nhb in nhbs_dict[site]:
            sample["geometry"]["neighbors"].append(
                {"source": i, "target": nhb, "jex": jex}
            )

    for i, site in enumerate(sites):
        sample["initial_state"].append([1, 0, 0])

    with open("sample.json", "w") as outfile:
        json.dump(sample, outfile, sort_keys=False, indent=2)


if __name__ == "__main__":
    main()
