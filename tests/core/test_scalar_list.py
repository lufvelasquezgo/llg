from llg.scalar_list import ScalarList


def test_scalar_list_from_int():
    # given
    value = 10

    # when
    scalar_iter = ScalarList(value)

    # then
    assert len(scalar_iter) == 1
    assert scalar_iter[0] == 10


def test_scalar_list_from_float():
    # given
    value = 69.69

    # when
    scalar_iter = ScalarList(value)

    # then
    assert len(scalar_iter) == 1
    assert scalar_iter[0] == 69.69


def test_scalar_list_from_range_dict():
    # given
    value = {"start": 0, "final": 10, "step": 2}

    # when
    scalar_iter = ScalarList(value)

    # then
    assert len(scalar_iter) == 6
    assert scalar_iter == [0, 2, 4, 6, 8, 10]


def test_scalar_list_from_range_dict_negative_step():
    # given
    value = {"start": 10, "final": 0, "step": -2}

    # when
    scalar_iter = ScalarList(value)

    # then
    assert len(scalar_iter) == 6
    assert scalar_iter == [10, 8, 6, 4, 2, 0]


def test_scalar_list_from_range_dict_float_step():
    # given
    value = {"start": 0, "final": 10, "step": 2.5}

    # when
    scalar_iter = ScalarList(value)

    # then
    assert len(scalar_iter) == 5
    assert scalar_iter == [0, 2.5, 5, 7.5, 10]


def test_scalar_list_from_list():
    # given
    value = [1, 2, 3]

    # when
    scalar_iter = ScalarList(value)

    # then
    assert len(scalar_iter) == 3
    assert scalar_iter == [1, 2, 3]


def test_scalar_list_from_empty_list():
    # given
    value = []

    # when
    scalar_iter = ScalarList(value)

    # then
    assert len(scalar_iter) == 0
    assert scalar_iter == []
