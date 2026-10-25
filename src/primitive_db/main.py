#!/usr/bin/env python3
"""Точка входа в программу."""

from primitive_db.engine import run


def main():
    """Запускает базу данных."""
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из программы")


if __name__ == "__main__":
    main()
