
"""Команды и основной цикл базы данных."""

import prompt
from prettytable import PrettyTable

from primitive_db.constants import META_FILE
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.parser import parse_condition, parse_values, split_command
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Показывает доступные команды."""
    print("\n***Работа с базой данных***")
    print("create_table <таблица> <столбец:тип> ... - создать таблицу")
    print("list_tables - список таблиц")
    print("drop_table <таблица> - удалить таблицу")
    print("insert into <таблица> values (...) - добавить запись")
    print("select from <таблица> [where столбец = значение] - показать записи")
    print("update <таблица> set столбец = значение where ... - изменить запись")
    print("delete from <таблица> where столбец = значение - удалить запись")
    print("info <таблица> - информация о таблице")
    print("help - справка")
    print("exit - выход")


def print_rows(columns, rows):
    """Выводит найденные записи в таблице."""
    names = [column.split(":")[0] for column in columns]
    table = PrettyTable()
    table.field_names = names

    for row in rows:
        table.add_row([row[name] for name in names])

    print(table)


def create_command(parts, metadata):
    """Обрабатывает создание таблицы."""
    if len(parts) < 3:
        print("Укажите имя таблицы и столбцы.")
        return

    table_name = parts[1]
    existed = table_name in metadata
    create_table(metadata, table_name, parts[2:])

    if not existed and table_name in metadata:
        save_metadata(META_FILE, metadata)


def drop_command(parts, metadata):
    """Обрабатывает удаление таблицы."""
    if len(parts) != 2:
        print("Укажите имя таблицы.")
        return

    table_name = parts[1]

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    result = drop_table(metadata, table_name)

    if result is not None:
        save_metadata(META_FILE, metadata)
        print(f'Таблица "{table_name}" успешно удалена.')


def insert_command(command, metadata):
    """Обрабатывает добавление записи."""
    command_start, separator, values_text = command.partition(" values ")
    parts = split_command(command_start)

    if not separator or len(parts) != 3:
        print('Пример: insert into users values ("Anna", 20, true)')
        return

    table_name = parts[2]
    values = parse_values(values_text)
    table_data = insert(metadata, table_name, values)

    if table_data is None:
        return

    save_table_data(table_name, table_data)
    record_id = table_data[-1]["ID"]

    print(f'Запись с ID={record_id} успешно добавлена в таблицу "{table_name}".')


def select_command(parts, metadata):
    """Обрабатывает поиск записей."""
    if len(parts) not in (3, 7) or parts[1] != "from":
        print("Пример: select from users where age = 20")
        return

    table_name = parts[2]

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    where_clause = None

    if len(parts) == 7:
        if parts[3] != "where":
            raise ValueError("Ожидалось where")

        where_clause = parse_condition(parts[4:7], metadata[table_name])

    table_data = load_table_data(table_name)
    rows = select(table_data, where_clause)

    if rows is None:
        return

    print_rows(metadata[table_name], rows)


def update_command(parts, metadata):
    """Обрабатывает изменение записей."""
    if len(parts) != 10 or parts[2] != "set" or parts[6] != "where":
        print('Пример: update users set age = 21 where name = "Anna"')
        return

    table_name = parts[1]

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = metadata[table_name]
    set_clause = parse_condition(parts[3:6], columns)
    where_clause = parse_condition(parts[7:10], columns)

    if "ID" in set_clause:
        print("Ошибка: Нельзя изменять ID.")
        return

    table_data = load_table_data(table_name)
    found = select(table_data, where_clause)

    if found is None:
        return

    if not found:
        print("Записи не найдены.")
        return

    updated = update(table_data, set_clause, where_clause)

    if updated is None:
        return

    save_table_data(table_name, updated)

    if len(found) == 1:
        print(
            f'Запись с ID={found[0]["ID"]} в таблице '
            f'"{table_name}" успешно обновлена.'
        )
    else:
        print(f"Обновлено записей: {len(found)}.")


def delete_command(parts, metadata):
    """Обрабатывает удаление записей."""
    if len(parts) != 7 or parts[1] != "from" or parts[3] != "where":
        print('Пример: delete from users where name = "Anna"')
        return

    table_name = parts[2]

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    where_clause = parse_condition(parts[4:7], metadata[table_name])
    table_data = load_table_data(table_name)
    found = select(table_data, where_clause)

    if found is None:
        return

    if not found:
        print("Записи не найдены.")
        return

    new_data = delete(table_data, where_clause)

    if new_data is None:
        return

    save_table_data(table_name, new_data)

    if len(found) == 1:
        print(
            f'Запись с ID={found[0]["ID"]} успешно удалена '
            f'из таблицы "{table_name}".'
        )
    else:
        print(f"Удалено записей: {len(found)}.")


def info_command(parts, metadata):
    """Показывает информацию о таблице."""
    if len(parts) != 2:
        print("Пример: info users")
        return

    table_name = parts[1]

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    columns = metadata[table_name]
    table_data = load_table_data(table_name)

    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(columns)}")
    print(f"Количество записей: {len(table_data)}")


def run():
    """Запускает командный цикл базы данных."""
    print_help()

    while True:
        metadata = load_metadata(META_FILE)
        command = prompt.string("Введите команду: ").strip()

        try:
            parts = split_command(command)

            if not parts:
                continue

            action = parts[0]

            if action == "help":
                print_help()
            elif action == "exit":
                print("Выход из программы")
                break
            elif action == "create_table":
                create_command(parts, metadata)
            elif action == "list_tables":
                list_tables(metadata)
            elif action == "drop_table":
                drop_command(parts, metadata)
            elif action == "insert" and len(parts) > 1 and parts[1] == "into":
                insert_command(command, metadata)
            elif action == "select":
                select_command(parts, metadata)
            elif action == "update":
                update_command(parts, metadata)
            elif action == "delete":
                delete_command(parts, metadata)
            elif action == "info":
                info_command(parts, metadata)
            else:
                print(f"Функции {action} нет. Попробуйте снова.")

        except ValueError as error:
            print(f"Некорректное значение: {error}. Попробуйте снова.")
