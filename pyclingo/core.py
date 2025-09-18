import typing as typ
from enum import Enum, auto
from attrs import define, field
from attrs.validators import instance_of
from . import utils as ut


def validate_identifier_name(instance, attribute, value):
    if not value.islower():
        raise ValueError(f'Symbol not lower case: {value}')
    if not value.isidentifier():
        raise ValueError(f'Not a valid identifier: {value}')


def validate_variable_name(instance, attribute, value):
    if value == '_':
        return
    if not value[0].isupper():
        raise ValueError('Variable name must start with upper case letter')
    if not value.isidentifier():
        raise ValueError('Variable name must be a valid identifier')



class Atom:
    def when(self, *body) -> 'Rule':
        return Rule(self, body)


@define(frozen=True)
class Identifier(Atom):
    name: str = field(validator=validate_identifier_name)


@define(frozen=True, eq=False)
class Expression:
    def __eq__(self, other: 'Expression') -> 'BinaryOperator':
        return BinaryOperator(BinaryOperatorType.equal, self, other)

    def __ne__(self, other: 'Expression') -> 'BinaryOperator':
        return BinaryOperator(BinaryOperatorType.not_equal, self, other)


@define(frozen=True, eq=False)
class Variable(Expression):
    name: str = field(validator=validate_variable_name)


BLANK = Variable('_')


@define(frozen=True, eq=False)
class String(Expression):
    value: str = field(validator=instance_of(str))


@define(frozen=True, eq=False)
class Number(Expression):
    value: int = field(validator=instance_of(int))



class BinaryOperatorType(Enum):
    equal = auto()
    not_equal = auto()


@define(frozen=True)
class BinaryOperator(Expression):
    op: BinaryOperatorType
    left: Expression
    right: Expression


@define(frozen=True)
class Relation(Atom):
    @classmethod
    def function_name(cls):
        return ut.camel2snake(cls.__name__)


@define(frozen=True)
class Choice:
    head: Atom
    body: tuple[Atom]
    lower: int = field(default=1)
    upper: int = field(default=1)


@define(frozen=True)
class Rule:
    head: typ.Union[Atom, Choice]
    body: tuple[typ.Union[Atom, Expression]]


@define(frozen=True)
class Constraint:
    body: typ.Sequence[typ.Union[Atom, Expression]]
