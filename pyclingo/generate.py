import json
import attrs
from . import utils as ut
from .core import Identifier, Variable, Number, String, Relation, Rule, Constraint, Choice


def generate(obj):
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
        args = map(generate, attrs.astuple(obj, recurse=False))
        return f'{name}({ut.comma_separated(args)})'
    elif isinstance(obj, Rule):
        head = generate(obj.head)
        body = map(generate, obj.body)
        return f'{head} :- {ut.comma_separated(body)}'
    elif isinstance(obj, Constraint):
        body = map(generate, obj.body)
        return f':- {ut.comma_separated(body)}'
    elif isinstance(obj, Choice):
        head = generate(obj.head)
        body = map(generate, obj.body)
        return f'{obj.lower} {{ {head}: {ut.comma_separated(body)} }} {obj.upper}'
    elif isinstance(obj, (list, tuple)):
        return '\n'.join(f'{generate(statement)}.' for statement in obj)
