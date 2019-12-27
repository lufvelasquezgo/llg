from collections.abc import Iterable
from numbers import Real
import numpy


class Bucket:
    """
    This is a class to match the sizes of two attributes. For this case, the 
    attributes are the ``temperature`` and the ``field``.

    Attributes:
        bucket_1 (float/list): It gets the temperature information 
        of the ``simulation_file``.
        bucket_2 (float/list): It gets the field information of the 
        ``simulation_file``.
    """

    def __init__(self, structure):
        """
        The constructor for Bucket class.

        Parameters:
            structure ():
        """
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
            raise Exception("[Bucket for temperature and field] No supported format.")

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    @staticmethod
    def match_sizes(bucket_1, bucket_2):
        """
        It is a function decorator, it is an instance for read the attributes and 
        match it sizes. 

        Parameters:
            bucket_1 (float/list):
            bucket_2 (float/list):

        Returns: 
            bucket_1: Object that has the same size of bucket_2.
            bucket_2: Object that has the same size of bucket_1.
        """
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
