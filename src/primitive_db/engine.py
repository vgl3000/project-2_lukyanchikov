
import prompt

from primitive_db.core import create_table, drop_table, insert, list_tables
from primitive_db.utils import load_metadata, save_metadata, save_table_data


def welcome():
    metadata = load_metadata("db_meta.json")

    print("Первая попытка запустить проект!")
    print("create_table - создать таблицу")
    print("list_tables - список таблиц")
    print("drop_table - удалить таблицу")
    print("insert into <таблица> values (...) - добавить запись")
    print("help - справка")
    print("exit - выход")

    while True:
        command = prompt.string("Введите команду: ")

        if command == "help":
            print("create_table - создать таблицу")
            print("list_tables - список таблиц")
            print("drop_table - удалить таблицу")
            print("insert into <таблица> values (...) - добавить запись")
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
                drop_table(metadata, parts[1])
                save_metadata("db_meta.json", metadata)

        elif command == "list_tables":
            list_tables(metadata)

        elif command.startswith("insert into "):
            parts = command.split(" values ", 1)

            if len(parts) != 2:
                print("Ошибка: Укажите значения.")
            else:
                table_name = parts[0].replace("insert into ", "").strip()
                values_text = parts[1].strip()

                if not values_text.startswith("(") or not values_text.endswith(")"):
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

        elif command == "exit":
            print("Выход из программы")
            break

        else:
            print("Неизвестная команда. Попробуйте снова.")
