def get_file_text(filename):
    import chardet
    with open(filename, 'rb') as f:
        data = f.read()
        result = chardet.detect(data)
        text = data.decode(result['encoding'])
        return text


def convert_text_to_list(text):
    word_list = text.strip().lower().split(' ')
    return word_list


def get_words_count(word_list):
    words_count = {}
    for word in word_list:
        if len(word) >= 6:
            if word in words_count:
                words_count[word] += 1
            else:
                words_count[word] = 1
    words_count = sorted(words_count.items(), key=lambda item: item[1], reverse=True)
    return words_count


def get_top10(words_count):
    top10 = {}
    for word_count in words_count:
        word, count = word_count
        if count not in top10:
            top10[count] = word
        else:
            top10[count] += ', ' + word
        if len(top10) == 10:
            break
    return top10


def print_top10(filename, top10):
    print('Наиболее упоминаемые слова в файле {}:'.format(filename))
    for count, word in top10.items():
        print('Слово {} упомянуто {} раз'.format(word, count))


def main():
    filename = input('Введите имя файла для подсчёта')
    text = get_file_text(filename)
    word_list = convert_text_to_list(text)
    words_count = get_words_count(word_list)
    print(words_count)
    top_list = get_top10(words_count)
    print_top10(filename, top_list)


main()
