
from primitive_db.utils import load_table_data


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


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    return metadata


def list_tables(metadata):
    if not metadata:
        print("Таблиц пока нет.")
        return

    for table_name in metadata:
        print(f"- {table_name}")


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
            try:
                value = int(value)
            except ValueError:
                print(f'Ошибка: Столбец "{name}" должен быть int.')
                return None

        elif column_type == "bool":
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            else:
                print(f'Ошибка: Столбец "{name}" должен быть bool.')
                return None

        new_record[name] = value

    table_data.append(new_record)
    return table_data
