
"""Декораторы и кэширование."""

import time
from functools import wraps


def handle_db_errors(func):
    """Обрабатывает основные ошибки базы данных."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except KeyError as error:
            print(f"Ошибка: Таблица или столбец {error} не найден.")

        except ValueError as error:
            print(f"Ошибка валидации: {error}")

        except FileNotFoundError:
            print("Ошибка: Файл данных не найден.")

    return wrapper


def confirm_action(action_name):
    """Запрашивает подтверждение действия."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )

            if answer.strip().lower() != "y":
                print("Действие отменено.")
                return None

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    """Показывает время выполнения функции."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()

        result = func(*args, **kwargs)

        elapsed_time = time.monotonic() - start_time

        print(
            f"Функция {func.__name__} "
            f"выполнилась за {elapsed_time:.3f} секунд."
        )

        return result

    return wrapper


def create_cacher():
    """Создаёт кэш для результатов запросов."""
    cache = {}

    def cache_result(key, value_func):
        """Возвращает результат из кэша или вычисляет его."""
        if key in cache:
            return cache[key]

        result = value_func()
        cache[key] = result

        return result

    return cache_result
