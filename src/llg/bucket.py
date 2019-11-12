from collections.abc import Iterable
from numbers import Real
import numpy


class Bucket:
    def __init__(self, structure):
        if isinstance(structure, dict):
            start = structure["start"]
            final = structure["final"]
            step = structure["step"]
            step = numpy.sign(final - start) * abs(step)
            self.values = numpy.arange(start, final + step, step)
        elif isinstance(structure, Iterable):
            self.values = structure
        elif isinstance(structure, Real):
            self.values = [structure]
        else:
            raise Exception("No supported format.")

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    @staticmethod
    def match_sizes(bucket_1, bucket_2):
        if len(bucket_1) == len(bucket_2):
            return bucket_1, bucket_2

        if len(bucket_1) < len(bucket_2):
            while len(bucket_1) < len(bucket_2):
                bucket_1 = Bucket(bucket_1.values * 2)
            return Bucket(bucket_1.values[: len(bucket_2)]), bucket_2

        if len(bucket_2) < len(bucket_1):
            while len(bucket_2) < len(bucket_1):
                bucket_2 = Bucket(bucket_2.values * 2)
            return bucket_1, Bucket(bucket_2.values[: len(bucket_1)])
