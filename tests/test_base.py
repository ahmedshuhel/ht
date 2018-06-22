from h.models.base import Base


def test_equality():
    o1 = Base()
    o2 = Base()
    assert o1 != o2
    o1.id = o2.id
    assert o1 == o2


def test_not_equal():
    o1 = Base()
    o2 = Base()
    o1.id = o2.id
    assert not o1 != o2
