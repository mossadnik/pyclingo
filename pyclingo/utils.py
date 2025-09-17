import re


def camel2snake(s):
    def sub(m):
        left, right = m.group()
        return f'{left}_{right.lower()}'

    return re.sub('[a-z][A-Z]', sub, s).lower()


def comma_separated(values):
    return ', '.join(values)
