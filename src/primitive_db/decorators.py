
import time
from functools import wraps


def handle_db_errors(func):
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
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()

        result = func(*args, **kwargs)

        end_time = time.monotonic()
        elapsed_time = end_time - start_time

        print(
            f"Функция {func.__name__} "
            f"выполнилась за {elapsed_time:.3f} секунд."
        )

        return result

    return wrapper
