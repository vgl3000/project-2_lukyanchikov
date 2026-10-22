import prompt

from primitive_db.core import create_table, list_tables


def welcome():
    metadata = {}

    print("Первая попытка запустить проект!")
    print("create_table - создать таблицу")
    print("list_tables - список таблиц")
    print("help - справка")
    print("exit - выход")

    while True:
        command = prompt.string("Введите команду: ")

        if command == "help":
            print("create_table - создать таблицу")
            print("list_tables - список таблиц")
            print("help - справка")
            print("exit - выход")

        elif command.startswith("create_table "):
            parts = command.split()

            if len(parts) < 3:
                print("Укажите имя таблицы и столбцы")
            else:
                create_table(metadata, parts[1], parts[2:])

        elif command == "list_tables":
            list_tables(metadata)

        elif command == "exit":
            print("Выход из программы")
            break

        else:
            print("Неизвестная команда. Попробуйте снова.")