from pyclingo.api import relation, var, symbol, solve


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
