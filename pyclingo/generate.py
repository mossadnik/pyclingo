import typing as typ
import json
import attrs
from . import utils as ut
from .core import Identifier, Variable, Number, String, Relation, Rule, Constraint, Choice, BinaryOperator, BinaryOperatorType


_binop_repr = {
    BinaryOperatorType.equal: '=',
    BinaryOperatorType.not_equal: '!='
}


def generate_statement(obj):
    if isinstance(obj, (Identifier, Variable)):
        return obj.name
    elif isinstance(obj, str):
        return json.dumps(obj)
    elif isinstance(obj, int):
        return str(obj)
    elif isinstance(obj, Number):
        return str(obj.value)
    elif isinstance(obj, String):
        return json.dumps(obj.value)
    elif isinstance(obj, Relation):
        name = obj.function_name()
        args = map(generate_statement, attrs.astuple(obj, recurse=False))
        return f'{name}({ut.comma_separated(args)})'
    elif isinstance(obj, BinaryOperator):
        left, right = map(generate_statement, [obj.left, obj.right])
        return f'{left} {_binop_repr[obj.op]} {right}'
    elif isinstance(obj, Rule):
        head = generate_statement(obj.head)
        body = map(generate_statement, obj.body)
        return f'{head} :- {ut.comma_separated(body)}'
    elif isinstance(obj, Constraint):
        body = map(generate_statement, obj.body)
        return f':- {ut.comma_separated(body)}'
    elif isinstance(obj, Choice):
        head = generate_statement(obj.head)
        body = map(generate_statement, obj.body)
        return f'{obj.lower} {{ {head}: {ut.comma_separated(body)} }} {obj.upper}'
    else:
        raise ValueError(f'Cannot generate statement from {obj}')


def generate(program: typ.Sequence) -> str:
    return '\n'.join(f'{generate_statement(statement)}.' for statement in program)
