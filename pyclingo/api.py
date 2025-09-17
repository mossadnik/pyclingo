import typing as typ
import attrs
import clingo
from .core import Relation, Number, String, Identifier, Variable, Rule, BLANK
from .generate import generate
from .deserialize import deserialize_solution
from .exceptions import Unsat


def relation(cls):
    return attrs.make_class(
        name=cls.__name__,
        bases=(Relation,),
        attrs={a: attrs.field(type=t, default=BLANK) for a, t in cls.__annotations__.items()}
    )


def lit(value: typ.Union[str, int]):
    if isinstance(value, int):
        return Number(value)
    elif isinstance(value, str):
        return String(value)
    else:
        raise ValueError('Literals must be int or str')


def symbol(name: str):
    return Identifier(name)


def var(name: str):
    return Variable(name)


def rule(head, *body):
    return Rule(head, body)


def solve(program: list, relations: list[type]) -> list:
    ctl = clingo.Control()
    ctl.add("base", [], generate(program))
    ctl.ground([("base", [])], context=None)

    with ctl.solve(yield_=True) as handle:
        model = handle.model()
        if not model:
            raise Unsat('Not satisfiable.')
        solution = model.symbols(atoms=True)
        return deserialize_solution(solution, relations)
