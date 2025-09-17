import pytest
from clingo.symbol import String
from pyclingo.deserialize import deserialize_symbol


class Test_deserialize_symbol:
    @pytest.mark.parametrize('value',
        ['a', '"a"']
    )
    def test_string(self, value):
        sym = String(value)
        assert deserialize_symbol(sym, {}) == value
