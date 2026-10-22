import prompt


def welcome():
    print("Первая попытка запустить проект!")
    print("help - справка")
    print("exit - выход")

    while True:
        command = prompt.string("Введите команду: ")

        if command == "help":
            print("help - справка")
            print("exit - выход")

        elif command == "exit":
            print("Выход из программы")
            break
        else:
            print("Неизвестная команда. Попробуйте снова.")