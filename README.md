
# Примитивная база данных

Учебный проект на Python. Программа работает через терминал и позволяет создавать таблицы и работать с записями.

Данные сохраняются в JSON-файлах.

## Установка и запуск

Для установки зависимостей:

```bash
uv sync
```

Для запуска программы:

```bash
uv run project
```

## Управление таблицами

Создать таблицу:

```text
create_table users name:str age:int active:bool
```

Посмотреть список таблиц:

```text
list_tables
```

Удалить таблицу:

```text
drop_table users
```

Поддерживаются типы int, str и bool. Столбец ID создается автоматически.

## CRUD-операции

Добавить запись:

```text
insert into users values ("Anna", 20, true)
```

Посмотреть все записи:

```text
select from users
```

Найти запись:

```text
select from users where age = 20
```

Изменить запись:

```text
update users set age = 21 where name = "Anna"
```

Удалить запись:

```text
delete from users where name = "Anna"
```

Посмотреть информацию о таблице:

```text
info users
```

Команда help показывает справку, exit завершает программу.

## Хранение данных

Информация о таблицах находится в db_meta.json.

Записи хранятся в папке data/ в отдельных JSON-файлах.

## Проверка кода

```bash
uv run ruff check .
```

## Демонстрация работы

Ссылка на запись asciinema будет добавлена после завершения проекта.
