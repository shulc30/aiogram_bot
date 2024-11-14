import os
import sys

BOOK_PATH = 'book/Bredberi_Marsianskie-hroniki.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}

# Функция возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple:
    punctuation_marks = {',', '.', '!', ':', ';', '?'}

    # Сохраняем оригенальный текст ввиде списка слов
    txt_split = text.split()
    # Получаем обрезанный текст по максимальному размеру
    new_txt = text[start:start + PAGE_SIZE]
    # Сплитуем обрезанный текст
    new_txt_split = new_txt.split()

    # Проверяем что последний элимент new_txt_split есть в txt_split
    if new_txt_split[-1] not in txt_split:
        # Если его нет значит обрезаем текст или многоточие
        # Вычисляем разницу между длинной обрезанного текста и длинной последнего слова
        difference = len(new_txt) - len(new_txt_split[-1])
        # Создаем new_txt до этой разницы
        new_txt = new_txt[:difference]

    # Ищем последний знак припенания в новом тексте и обрезаем по нему
    last_punctuation_index = max(new_txt.rfind(p) for p in punctuation_marks)
    if last_punctuation_index != -1:
        new_txt = new_txt[:last_punctuation_index + 1]

    return new_txt, len(new_txt)
    

# Функция формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read() # Считываем полный текст книги
    
    start = 0
    page_number = 1

    while start < len(text):
        # Получаем текст страницы и её размер с помощью _get_part_text
        page_text, page_length = _get_part_text(text, start, PAGE_SIZE)

        # Убираем лишние символы в начале текста страницы
        page_text = page_text.lstrip()

        # Записываем страницу в словарь с номером страницы в качестве ключа
        book[page_number] = page_text

        # Переходим к следующей страницы
        start += page_length
        page_number += 1
    

# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
