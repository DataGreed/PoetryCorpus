# -*- coding: utf-8 -*-
# Автор: Гусев Илья
# Описание: Генерация, загрузка и сохранение разметок по текстам.

import os
from poetry.apps.corpus.scripts.settings import MARKUPS_DUMP_RAW_PATH

from rupo.files.writer import Writer, FileTypeEnum
from rupo.api import get_improved_markup


def get_paths(path: str, ext: str):
    """
    Получение всех файлов заданного типа по заданному пути.

    :param path: путь к файлу/папке.
    :param ext: требуемое расширение.
    """
    if os.path.isfile(path):
        if ext == os.path.splitext(path)[1]:
            yield path
    else:
        for root, folders, files in os.walk(path):
            for file in files:
                if ext == os.path.splitext(file)[1]:
                    yield os.path.join(root, file)
            for folder in folders:
                return get_paths(folder, ext)


def run():
    raw_writer = Writer(FileTypeEnum.RAW, MARKUPS_DUMP_RAW_PATH)
    raw_writer.open()
    i = 0
    path = "/media/data/stihi_ru_clean"
    paths = get_paths(path, "")
    for filename in paths:
        with open(filename, "r", encoding="utf-8") as file:
            text = ""
            is_text = False
            try:
                for file_line in file:
                    if "<div" in file_line:
                        is_text = True
                    elif "</div>" in file_line:
                        is_text = False
                        clean_text = ""
                        skip = False
                        lines = text.split("\n")
                        for line in lines:
                            if line == "":
                                continue
                            for ch in line:
                                if "a" < ch < "z" or "A" < ch < "Z" or ch == "Ј":
                                    skip = True
                                    break
                            clean_text += line.strip() + "\n"
                        if not skip:
                            print(clean_text.split("\n")[:2])
                            markup, result = get_improved_markup(clean_text)
                            raw_writer.write_markup(markup)
                        else:
                            print("Skipped")
                        i += 1
                        print(i)
                        text = ""
                    elif is_text:
                        text += file_line.strip() + "\n"
            except Exception as e:
                pass
    raw_writer.close()
run()