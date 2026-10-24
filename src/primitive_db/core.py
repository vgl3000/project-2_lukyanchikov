
import json

from primitive_db.decorators import (
    confirm_action,
    create_cacher,
    handle_db_errors,
    log_time,
)
from primitive_db.utils import delete_table_data, load_table_data

select_cache = create_cacher()


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    for column in columns:
        parts = column.split(":")

        if len(parts) != 2:
            print(f"Некорректный столбец: {column}")
            return metadata

        column_type = parts[1]

        if column_type not in ["int", "str", "bool"]:
            print(f"Некорректный тип данных: {column_type}")
            return metadata

    metadata[table_name] = ["ID:int"] + columns
    return metadata


@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    delete_table_data(table_name)

    del metadata[table_name]
    return metadata


def list_tables(metadata):
    if not metadata:
        print("Таблиц пока нет.")
        return

    for table_name in metadata:
        print(f"- {table_name}")


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    columns = metadata[table_name][1:]

    if len(values) != len(columns):
        print("Ошибка: Неверное количество значений.")
        return None

    table_data = load_table_data(table_name)

    new_id = 1

    for row in table_data:
        if row["ID"] >= new_id:
            new_id = row["ID"] + 1

    new_record = {"ID": new_id}

    for i in range(len(columns)):
        name, column_type = columns[i].split(":")
        value = values[i]

        if column_type == "int":
            value = int(value)

        elif column_type == "bool":
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            else:
                raise ValueError(f'Столбец "{name}" должен быть bool.')

        new_record[name] = value

    table_data.append(new_record)
    return table_data


@log_time
def select(table_data, where_clause=None):
    key = json.dumps(
        {"data": table_data, "where": where_clause},
        sort_keys=True,
        ensure_ascii=False,
    )

    def find_records():
        result = []

        for row in table_data:
            matches = True

            if where_clause is not None:
                for column, value in where_clause.items():
                    if row.get(column) != value:
                        matches = False
                        break

            if matches:
                result.append(row.copy())

        return result

    cached_rows = select_cache(key, find_records)

    return [row.copy() for row in cached_rows]


def update(table_data, set_clause, where_clause):
    for row in table_data:
        matches = True

        for column, value in where_clause.items():
            if row.get(column) != value:
                matches = False
                break

        if matches:
            for column, value in set_clause.items():
                row[column] = value

    return table_data


@confirm_action("удаление записей")
def delete(table_data, where_clause):
    result = []

    for row in table_data:
        matches = True

        for column, value in where_clause.items():
            if row.get(column) != value:
                matches = False
                break

        if not matches:
            result.append(row)

    return result
