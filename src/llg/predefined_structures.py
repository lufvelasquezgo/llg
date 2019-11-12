from itertools import product
from collections import defaultdict
from llg import Sample


class GenericBcc(Sample):
    def __init__(self, length):
        super().__init__()

        self.length = length

        index = {}
        for x, y, z in product(range(self.length), repeat=3):
            index[(x, y, z)] = len(index)
            index[(x + 0.5, y + 0.5, z + 0.5)] = len(index)

        for position, i in index.items():
            site = {"index": i, "position": position}
            self.sites.append(site)

        pairs = []
        for position, i in index.items():
            x, y, z = position
            pairs.append(
                (i, index[((x + 0.5) % length, (y + 0.5) % length, (z + 0.5) % length)])
            )
            pairs.append(
                (i, index[((x + 0.5) % length, (y + 0.5) % length, (z - 0.5) % length)])
            )
            pairs.append(
                (i, index[((x + 0.5) % length, (y - 0.5) % length, (z + 0.5) % length)])
            )
            pairs.append(
                (i, index[((x + 0.5) % length, (y - 0.5) % length, (z - 0.5) % length)])
            )
            pairs.append(
                (i, index[((x - 0.5) % length, (y + 0.5) % length, (z + 0.5) % length)])
            )
            pairs.append(
                (i, index[((x - 0.5) % length, (y + 0.5) % length, (z - 0.5) % length)])
            )
            pairs.append(
                (i, index[((x - 0.5) % length, (y - 0.5) % length, (z + 0.5) % length)])
            )
            pairs.append(
                (i, index[((x - 0.5) % length, (y - 0.5) % length, (z - 0.5) % length)])
            )

        for i, j in pairs:
            self.neighbors.append({"source": i, "target": j})
