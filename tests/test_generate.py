import pytest
from pyclingo.generate import generate_statement
from pyclingo.api import var, lit


class Test_generate_statement:
    @pytest.mark.parametrize('expr, expected', [
        [var('A') == lit(1), 'A = 1'],
        [var('A') != lit(1), 'A != 1'],
        [var('A') == var('B'), 'A = B'],
    ])
    def test_binary_operator(self, expr, expected):
        actual = generate_statement(expr)
        assert actual == expected
