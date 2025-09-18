import pytest
from pyclingo.api import relation, symbol, solve, lit
from pyclingo.core import Number, String, Constraint
from pyclingo.exceptions import Unsat


def test_roundtrip():
    @relation
    class connected:
        this: str
        that: str

    solution = solve([connected('a', symbol('b'))], [connected])
    assert len(solution) == 1
    solution = solution[0]
    assert solution.this == 'a'
    assert solution.that == symbol('b')


@pytest.mark.parametrize('value, expected', [
    (1, Number(1)),
    ('a', String('a'))
])
def test_lit(value, expected):
    actual = lit(value)
    assert type(actual) is type(expected)
    assert actual.value == expected.value


def test_unsat():
    with pytest.raises(Unsat):
        c = symbol('c')
        solve([c, Constraint([c])], [])
