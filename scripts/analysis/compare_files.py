import re
import sqlite3
from difflib import SequenceMatcher


def find_mistakes(auto_text, manual_text):
    result = []
    for i in range(len(auto_text)):
        seq = SequenceMatcher(a=auto_text[i], b=manual_text[i])
        if seq.ratio() != 1:
            result.append((auto_text[i], manual_text[i]))
    return result


def load_syllables():
    conn = sqlite3.connect('tibetan_syllables.db')
    c = conn.cursor()
    c.execute("SELECT Transliteration FROM tibetan_syllables")
    syllables = [str(row[0]) for row in c.fetchall()]
    conn.close()
    return syllables


def split_into_syllables(text, syllables):
    pattern = "|".join(syllables)
    return re.findall(pattern, text)


def main():
    # syllables = load_syllables()
    # print(syllables)
    for file_number in range(471, 478):
        with open('OCR_texts/TCCG-001_0' + str(file_number) + '_crop.txt', 'r', encoding='utf-8') as file:
            auto_text = file.read()

        with open('manual_recognition_texts/0' + str(file_number) + '.txt', 'r', encoding='utf-8') as file:
            manual_text = file.read()

        auto_text = glue_words_with_igo(auto_text.split())

        manual_text = glue_words_with_igo(manual_text.split())

        # 478 +-, 483, 489, 492, 497, 499, 496-499 не работают нормально, посмотреть, что не так
        level_word_count(manual_text, auto_text)

        print(file_number)
        print(auto_text)
        print(len(auto_text))

        print(manual_text)
        print(len(manual_text))
        mistakes = find_mistakes(auto_text, manual_text)
        print(mistakes)

        print()


if __name__ == "__main__":
    main()
