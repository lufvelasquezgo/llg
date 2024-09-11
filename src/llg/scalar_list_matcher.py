from typing import Iterable, Iterator, Tuple

from llg.core.types import Scalar
from llg.scalar_list import ScalarList


class ScalarListMatcher(Iterable[Tuple[Scalar, Scalar]]):
    def __init__(self, *scalar_lists: ScalarList):
        self._validate_min_size(scalar_lists)
        self.size = max(len(scalar_list) for scalar_list in scalar_lists)
        self.scalar_lists = [
            self._complete_size(scalar_list, self.size) for scalar_list in scalar_lists
        ]

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[Tuple[Scalar, Scalar]]:
        return zip(*self.scalar_lists)

    @staticmethod
    def _complete_size(scalar_iter: ScalarList, size: int) -> ScalarList:
        while len(scalar_iter) < size:
            scalar_iter = ScalarList(list(scalar_iter) * 2)
        return ScalarList(list(scalar_iter)[:size])

    @staticmethod
    def _validate_min_size(scalar_lists: Tuple[ScalarList, ...]) -> None:
        for scalar_list in scalar_lists:
            if len(scalar_list) < 1:
                raise ValueError("All ScalarLists must have at least one element")
