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
    del metadata[table_name]
    return metadata