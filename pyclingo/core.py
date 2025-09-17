import typing as typ
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


@define(frozen=True)
class Variable:
    name: str = field(validator=validate_variable_name)


BLANK = Variable('_')


@define(frozen=True)
class String:
    value: str = field(validator=instance_of(str))


@define(frozen=True)
class Number:
    value: int = field(validator=instance_of(int))


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
    body: tuple[Atom]  # actually Bool



@define(frozen=True)
class Constraint:
    body: tuple[Atom]  # actually Bool
