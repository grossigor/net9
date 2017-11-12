import requests
import chardet
import os


def get_file_text(filename):
    with open(filename, 'rb') as f:
        data = f.read()
        result = chardet.detect(data)
        text = data.decode(result['encoding'])
        return text


def save_result_file(filename, result):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(result)


def translate_it(filename, result_filename, source_lang, result_lang="ru"):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param filename: <str> absolute path to file for translation
    :param result_filename: <str> absolute path to file for write translation result
    :param source_lang: <str> source language code
    :param result_lang: <str> translation language code
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    text = get_file_text(filename)
    lang = source_lang + '-' + result_lang

    params = {
        'key': key,
        'lang': lang,
        'text': text,
    }
    response = requests.get(url, params=params).json()
    result = ' '.join(response.get('text', []))
    save_result_file(result_filename, result)


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(current_dir)
    txt_files = list(filter(lambda x: x.endswith('.txt'), files))
    for file in txt_files:
        file_lang = os.path.splitext(file)[0]
        file_path = os.path.join(current_dir, file)
        file_result = os.path.join(current_dir, file_lang + '-ru.txt')
        translate_it(file_path, file_result, file_lang.lower())
