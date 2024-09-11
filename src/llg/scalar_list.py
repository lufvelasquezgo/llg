from collections.abc import Iterable
from typing import Union

import numpy

from llg.core.types import RangeDict, Scalar


class ScalarList(list):
    def __init__(self, value: Union[Scalar, RangeDict, Iterable[Scalar]]):
        if isinstance(value, dict):
            start = value["start"]
            final = value["final"]
            step = value["step"]
            step = numpy.sign(final - start) * abs(step)
            super().__init__(numpy.arange(start, final + step, step))
        elif isinstance(value, Iterable):
            super().__init__(value)
        elif isinstance(value, (int, float)):
            super().__init__([value])
        else:
            raise Exception(
                f"ScalarIter does not support this type of value: {type(value)}"
            )
