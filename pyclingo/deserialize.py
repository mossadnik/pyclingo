import typing as typ
import json
from clingo.symbol import SymbolType
from pyclingo.core import Relation, Identifier



def deserialize_symbol(symbol, function_cls: dict[str, type]) -> typ.Union[Relation, Identifier, str, int]:
    if symbol.type is SymbolType.Function:
        if symbol.name in function_cls:
            cls = function_cls[symbol.name]
            return cls(*[deserialize_symbol(a, function_cls) for a in symbol.arguments])
        elif not symbol.arguments:
            return Identifier(symbol.name)
        else:
            raise ValueError(f'No relation provided for function: {symbol.name}')
    elif symbol.type is SymbolType.String:
        value = symbol.string.replace('"', '\\"')
        try:
            return json.loads(f'"{value}"')
        except json.JSONDecodeError:
            raise ValueError(f'Failed to decode string constant: {symbol.string}')
    elif symbol.type is SymbolType.Number:
        return symbol.number
    else:
        raise ValueError(f'Cannot deserialize symbol {symbol}')


def deserialize_solution(solution: list, relations: list[type]) -> list:
    if not isinstance(relations, (list, tuple)):
        relations = [relations]
    function_cls = {rel.function_name(): rel for rel in relations}
    res = []
    for sol in solution:
        if sol.name not in function_cls:
            # TODO this skips top-level identifiers
            continue
        res.append(deserialize_symbol(sol, function_cls))
    return res
