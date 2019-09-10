"""
Class Benchmark to compute times for several running for a code.
"""

import time as _time
import numpy as _numpy


class Benchmark:
    """
    Benchmark Class
    It is a context manager, which contains a `run` generator for running the
    code inside it and computes the elapsed time and store it in the `_times`
    list.
    """

    def __init__(self, trials):
        self._trials = trials
        self._times = []

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._times = []

    def run(self):
        """
        Generator for running the code inside it and compute the elapsed time.
        The times are stored in the `_times` list.
        """
        for i in range(self._trials):
            start = _time.time()
            yield i
            final = _time.time()
            self._times.append(final - start)

    @property
    def mean(self):
        """
        Property to compute the mean time in case of `_times` is not empty.
        """
        if not self._times:
            return None
        return _numpy.mean(self._times)

    @property
    def std(self):
        """
        Property to compute the std time in case of `_times` is not empty.
        """
        if not self._times:
            return None
        return _numpy.std(self._times)
