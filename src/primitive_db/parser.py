
"""Разбор команд базы данных."""

import shlex


def split_command(command):
    """Разбивает команду на части."""
    lexer = shlex.shlex(command, posix=True, punctuation_chars="=")
    lexer.whitespace_split = True
    lexer.commenters = ""
    return list(lexer)


def parse_values(text):
    """Разбирает значения для insert."""
    text = text.strip()

    if not text.startswith("(") or not text.endswith(")"):
        raise ValueError("Значения должны быть в скобках")

    lexer = shlex.shlex(text[1:-1], posix=True)
    lexer.whitespace = ","
    lexer.whitespace_split = True
    lexer.commenters = ""

    return [value.strip() for value in lexer]


def parse_condition(parts, columns):
    """Разбирает условие вида age = 20."""
    if isinstance(parts, str):
        parts = split_command(parts)

    if len(parts) != 3 or parts[1] != "=":
        raise ValueError("Неверное условие")

    name, _, value = parts
    column_type = None

    for column in columns:
        column_name, data_type = column.split(":")

        if column_name == name:
            column_type = data_type
            break

    if column_type is None:
        raise ValueError(f'Столбец "{name}" не существует')

    if not value.strip():
        raise ValueError(f'Значение столбца "{name}" не может быть пустым')

    if column_type == "int":
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f'Столбец "{name}" должен быть int') from None

    elif column_type == "bool":
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        else:
            raise ValueError(f'Столбец "{name}" должен быть bool')

    return {name: value}
