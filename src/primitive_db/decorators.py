
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
