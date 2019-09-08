import time
import numpy


class Benchmark:
    def __init__(self, trials):
        self._trials = trials
        self._times = []

    def run(self):
        for _ in range(self._trials):
            start = time.time()
            yield _
            final = time.time()
            self._times.append(final - start)

    @property
    def mean(self):
        return numpy.mean(self._times)

    @property
    def std(self):
        return numpy.std(self._times)
