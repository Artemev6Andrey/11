#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import jsonschema


def add(students):
    # Запросить данные о студенте.
    name = input("Фамилия и инициалы? ")
    group = input("Номер группы? ")
    progress = [
        int(input("Оценка за 1 семестр")),
        int(input("Оценка за 2 семестр")),
        int(input("Оценка за 3 семестр")),
        int(input("Оценка за 4 семестр")),
        int(input("Оценка за 5 семестр"))
    ]
    # Создать словарь.
    student = {
        'name': name,
        'group': group,
        'mark': progress
    }
    # Добавить словарь в список.
    students.append(student)
    if len(students) > 1:
        students.sort(key=lambda item: item.get('group')[::-1])
    return students


def list(students):
    # Заголовок таблицы.
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 15
    )
    print(line)
    print(
        '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
            "№",
            "Ф.И.О.",
            "Группа",
            "Успеваемость"
        )
    )
    print(line)

    # Вывести данные о всех студентах.
    for idx, student in enumerate(students, 1):
        ma = student.get('mark', '')
        print(
            '| {:^4} | {:<30} | {:<20} | {}.{}.{}.{}.{:<7} |'.format(
                idx,
                student.get('name', ''),
                student.get('group', ''),
                ma[0],
                ma[1],
                ma[2],
                ma[3],
                ma[4]
            )
        )
        print(line)


def select(students):
    # Инициализировать счетчик.
    count = 0
    # Проверить сведения студентов из списка.
    for student in students:
        mark = student.get('mark', '')
        if sum(mark) / max(len(mark), 1) >= 4.0:
            print(
                '{:>4} {}'.format('*', student.get('name', '')),
                '{:>1} {}'.format('группа №', student.get('group', ''))
            )
            count += 1
    if count == 0:
        print("Студенты с баллом 4.0 и выше не найдены.")


def help_1():
    print("Список команд:\n")
    print("add - добавить студента;")
    print("list - вывести список студентов;")
    print("select - запросить студентов с баллом выше 4.0;")
    print("save - сохранить список студентов;")
    print("load - загрузить список студентов;")
    print("exit - завершить работу с программой.")


def save_students(file_name, students):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    schema = {
        "type": "array",
        "items": [
            {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "group": {
                        "type": "string"
                    },
                    "mark": {
                        "type": "array",
                        "items": [
                            {
                                "type": "integer"
                            },
                            {
                                "type": "integer"
                            },
                            {
                                "type": "integer"
                            },
                            {
                                "type": "integer"
                            },
                            {
                                "type": "integer"
                            }
                        ]
                    }
                },
                "required": [
                    "name",
                    "group",
                    "mark"
                ]
            }
        ]
    }
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
        validator = jsonschema.Draft7Validator(schema)
        try:
            if not validator.validate(loadfile):
                print("Валидация прошла успешно")
        except jsonschema.exceptions.ValidationError:
            print("Ошибка валидации", file=sys.stderr)
            exit()
    return loadfile


def main():
    # Список студентов.
    students = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break
        elif command == 'add':
            students = add(students)
        elif command == 'list':
            list(students)
        elif command.startswith('select'):
            select(students)
        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            save_students(file_name, students)
        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]
            # Сохранить данные в файл с заданным именем.
            students = load_students(file_name)
        elif command == 'help':
            help_1()
        else:
            print("неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()