
import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def welcome():
    metadata = load_metadata("db_meta.json")

    print("Первая попытка запустить проект!")
    print("create_table - создать таблицу")
    print("list_tables - список таблиц")
    print("drop_table - удалить таблицу")
    print("insert into <таблица> values (...) - добавить запись")
    print("select from <таблица> - показать записи")
    print("select from <таблица> where <столбец> = <значение> - поиск")
    print("update <таблица> set <столбец> = <значение> where ... - изменение")
    print("delete from <таблица> where <столбец> = <значение> - удаление")
    print("info <таблица> - информация о таблице")
    print("help - справка")
    print("exit - выход")

    while True:
        command = prompt.string("Введите команду: ")

        if command == "help":
            print("create_table - создать таблицу")
            print("list_tables - список таблиц")
            print("drop_table - удалить таблицу")
            print("insert into <таблица> values (...) - добавить запись")
            print("select from <таблица> - показать записи")
            print("select from <таблица> where <столбец> = <значение> - поиск")
            print("update <таблица> set <столбец> = <значение> where ... - изменение")
            print("delete from <таблица> where <столбец> = <значение> - удаление")
            print("info <таблица> - информация о таблице")
            print("help - справка")
            print("exit - выход")

        elif command.startswith("create_table "):
            parts = command.split()

            if len(parts) < 3:
                print("Укажите имя таблицы и столбцы")
            else:
                create_table(metadata, parts[1], parts[2:])
                save_metadata("db_meta.json", metadata)

        elif command == "drop_table" or command.startswith("drop_table "):
            parts = command.split()

            if len(parts) != 2:
                print("Укажите имя таблицы")
            else:
                table_name = parts[1]

                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                else:
                    result = drop_table(metadata, table_name)

                    if result is not None:
                        save_metadata("db_meta.json", metadata)
                        print(f'Таблица "{table_name}" удалена.')

        elif command == "list_tables":
            list_tables(metadata)

        elif command.startswith("insert into "):
            parts = command.split(" values ", 1)

            if len(parts) != 2:
                print("Ошибка: Укажите значения.")
            else:
                table_name = parts[0].replace("insert into ", "").strip()
                values_text = parts[1].strip()

                if not (
                    values_text.startswith("(") and values_text.endswith(")")
                ):
                    print("Ошибка: Значения должны быть в скобках.")
                else:
                    values_text = values_text[1:-1]
                    values = values_text.split(",")

                    for i in range(len(values)):
                        values[i] = values[i].strip().strip('"').strip("'")

                    table_data = insert(metadata, table_name, values)

                    if table_data is not None:
                        save_table_data(table_name, table_data)
                        print(f'Запись добавлена в таблицу "{table_name}".')

        elif command.startswith("select from "):
            try:
                parts = shlex.split(command)
            except ValueError:
                print("Ошибка: Проверьте кавычки.")
                continue

            if len(parts) != 3 and len(parts) != 7:
                print("Пример: select from users where age = 20")
                continue

            table_name = parts[2]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            where_clause = None

            if len(parts) == 7:
                if parts[3] != "where" or parts[5] != "=":
                    print("Ошибка: Неверное условие where.")
                    continue

                column_name = parts[4]
                value = parts[6]
                column_type = None

                for column in metadata[table_name]:
                    name, data_type = column.split(":")

                    if name == column_name:
                        column_type = data_type
                        break

                if column_type is None:
                    print(f'Ошибка: Столбец "{column_name}" не существует.')
                    continue

                if column_type == "int":
                    try:
                        value = int(value)
                    except ValueError:
                        print("Ошибка: Ожидалось целое число.")
                        continue

                elif column_type == "bool":
                    if value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False
                    else:
                        print("Ошибка: Ожидалось true или false.")
                        continue

                where_clause = {column_name: value}

            table_data = load_table_data(table_name)
            result = select(table_data, where_clause)

            table = PrettyTable()
            column_names = []

            for column in metadata[table_name]:
                column_names.append(column.split(":")[0])

            table.field_names = column_names

            for row in result:
                values = []

                for name in column_names:
                    values.append(row[name])

                table.add_row(values)

            print(table)

        elif command.startswith("update "):
            try:
                parts = shlex.split(command)
            except ValueError:
                print("Ошибка: Проверьте кавычки.")
                continue

            if (
                len(parts) != 10
                or parts[2] != "set"
                or parts[4] != "="
                or parts[6] != "where"
                or parts[8] != "="
            ):
                print('Пример: update users set age = 21 where name = "Anna"')
                continue

            table_name = parts[1]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            set_column = parts[3]
            set_value = parts[5]

            where_column = parts[7]
            where_value = parts[9]

            if set_column == "ID":
                print("Ошибка: Нельзя изменять ID.")
                continue

            set_type = None
            where_type = None

            for column in metadata[table_name]:
                name, data_type = column.split(":")

                if name == set_column:
                    set_type = data_type

                if name == where_column:
                    where_type = data_type

            if set_type is None:
                print(f'Ошибка: Столбец "{set_column}" не существует.')
                continue

            if where_type is None:
                print(f'Ошибка: Столбец "{where_column}" не существует.')
                continue

            try:
                if set_type == "int":
                    set_value = int(set_value)

                elif set_type == "bool":
                    if set_value.lower() == "true":
                        set_value = True
                    elif set_value.lower() == "false":
                        set_value = False
                    else:
                        raise ValueError

                if where_type == "int":
                    where_value = int(where_value)

                elif where_type == "bool":
                    if where_value.lower() == "true":
                        where_value = True
                    elif where_value.lower() == "false":
                        where_value = False
                    else:
                        raise ValueError

            except ValueError:
                print("Ошибка: Некорректный тип значения.")
                continue

            table_data = load_table_data(table_name)

            where_clause = {where_column: where_value}
            set_clause = {set_column: set_value}

            found = select(table_data, where_clause)

            if not found:
                print("Записи не найдены.")
                continue

            updated_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, updated_data)

            print(f"Обновлено записей: {len(found)}.")

        elif command.startswith("delete from "):
            try:
                parts = shlex.split(command)
            except ValueError:
                print("Ошибка: Проверьте кавычки.")
                continue

            if (
                len(parts) != 7
                or parts[1] != "from"
                or parts[3] != "where"
                or parts[5] != "="
            ):
                print('Пример: delete from users where name = "Anna"')
                continue

            table_name = parts[2]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            column_name = parts[4]
            value = parts[6]
            column_type = None

            for column in metadata[table_name]:
                name, data_type = column.split(":")

                if name == column_name:
                    column_type = data_type
                    break

            if column_type is None:
                print(f'Ошибка: Столбец "{column_name}" не существует.')
                continue

            if column_type == "int":
                try:
                    value = int(value)
                except ValueError:
                    print("Ошибка: Ожидалось целое число.")
                    continue

            elif column_type == "bool":
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                else:
                    print("Ошибка: Ожидалось true или false.")
                    continue

            where_clause = {column_name: value}
            table_data = load_table_data(table_name)

            found = select(table_data, where_clause)

            if not found:
                print("Записи не найдены.")
                continue

            new_data = delete(table_data, where_clause)

            if new_data is not None:
                save_table_data(table_name, new_data)
                print(f"Удалено записей: {len(found)}.")

        elif command == "info" or command.startswith("info "):
            parts = command.split()

            if len(parts) != 2:
                print("Пример: info users")
                continue

            table_name = parts[1]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            columns = metadata[table_name]
            table_data = load_table_data(table_name)

            print(f"Таблица: {table_name}")
            print(f"Столбцы: {', '.join(columns)}")
            print(f"Количество записей: {len(table_data)}")

        elif command == "exit":
            print("Выход из программы")
            break

        else:
            print("Неизвестная команда. Попробуйте снова.")
