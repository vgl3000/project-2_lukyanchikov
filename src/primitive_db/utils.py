
"""Загрузка и сохранение данных базы."""

import json
import os

from primitive_db.constants import DATA_DIR


def save_metadata(filepath, data):
    """Сохраняет информацию о таблицах."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_metadata(filepath):
    """Загружает информацию о таблицах."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def get_table_path(table_name):
    """Возвращает путь к файлу таблицы."""
    return os.path.join(DATA_DIR, f"{table_name}.json")


def load_table_data(table_name):
    """Загружает записи таблицы."""
    filepath = get_table_path(table_name)

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет записи таблицы."""
    os.makedirs(DATA_DIR, exist_ok=True)

    filepath = get_table_path(table_name)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def delete_table_data(table_name):
    """Удаляет файл таблицы."""
    filepath = get_table_path(table_name)

    if os.path.isfile(filepath):
        os.remove(filepath)
