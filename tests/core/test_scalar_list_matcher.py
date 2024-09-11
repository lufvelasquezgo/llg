from llg.scalar_list import ScalarList
from llg.scalar_list_matcher import ScalarListMatcher


def test_scalar_list_matcher():
    # given
    scalar_list_1 = ScalarList([1, 2, 3])
    scalar_list_2 = ScalarList([4, 5, 6, 7])
    scalar_list_3 = ScalarList([8, 9])

    # when
    scalar_list_matcher = ScalarListMatcher(scalar_list_1, scalar_list_2, scalar_list_3)

    # then
    assert len(scalar_list_matcher) == 4
    assert list(scalar_list_matcher) == [(1, 4, 8), (2, 5, 9), (3, 6, 8), (1, 7, 9)]


def test_scalar_list_matcher_already_matched():
    # given
    scalar_list_1 = ScalarList([1])
    scalar_list_2 = ScalarList([4])
    scalar_list_3 = ScalarList([8])

    # when
    scalar_list_matcher = ScalarListMatcher(scalar_list_1, scalar_list_2, scalar_list_3)

    # then
    assert len(scalar_list_matcher) == 1
    assert list(scalar_list_matcher) == [(1, 4, 8)]


def test_scalar_list_matcher_with_empty_list():
    # given
    scalar_list_1 = ScalarList([])
    scalar_list_2 = ScalarList([4, 5, 6, 7])
    scalar_list_3 = ScalarList([8, 9])

    # when
    try:
        ScalarListMatcher(scalar_list_1, scalar_list_2, scalar_list_3)
    except ValueError as error:
        # then
        assert str(error) == "All ScalarLists must have at least one element"
    else:
        assert False, "Exception not raised"
