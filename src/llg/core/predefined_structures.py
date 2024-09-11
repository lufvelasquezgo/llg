from itertools import product

from llg.core.sample import Sample


class GenericBcc(Sample):
    def __init__(self, length):
        """
        The constructor for GenericBcc class.It looks periodic boundary conditions.
        """
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


class GenericFcc(Sample):
    def __init__(self, length):
        """
        The constructor for GenericFcc class. It looks periodic boundary conditions.
        """
        super().__init__()

        self.length = length

        index = {}

        for x, y, z in product(range(self.length), repeat=3):
            index[(x, y, z)] = len(index)
            index[(x + 0.5, y + 0.5, z)] = len(index)
            index[(x + 0.5, y, z + 0.5)] = len(index)
            index[(x, y + 0.5, z + 0.5)] = len(index)

        for position, i in index.items():
            site = {"index": i, "position": position}
            self.sites.append(site)

        pairs = []
        for position, i in index.items():
            x, y, z = position
            pairs.append((i, index[((x + 0.5) % length, (y + 0.5) % length, z)]))
            pairs.append((i, index[((x + 0.5) % length, (y - 0.5) % length, z)]))
            pairs.append((i, index[((x - 0.5) % length, (y + 0.5) % length, z)]))
            pairs.append((i, index[((x - 0.5) % length, (y - 0.5) % length, z)]))
            pairs.append((i, index[(x, (y + 0.5) % length, (z + 0.5) % length)]))
            pairs.append((i, index[(x, (y + 0.5) % length, (z - 0.5) % length)]))
            pairs.append((i, index[(x, (y - 0.5) % length, (z + 0.5) % length)]))
            pairs.append((i, index[(x, (y - 0.5) % length, (z - 0.5) % length)]))
            pairs.append((i, index[((x + 0.5) % length, y, (z + 0.5) % length)]))
            pairs.append((i, index[((x + 0.5) % length, y, (z - 0.5) % length)]))
            pairs.append((i, index[((x - 0.5) % length, y, (z + 0.5) % length)]))
            pairs.append((i, index[((x - 0.5) % length, y, (z - 0.5) % length)]))

        for i, j in pairs:
            self.neighbors.append({"source": i, "target": j})
