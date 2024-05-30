from difflib import SequenceMatcher
from typing import List
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def glue_words_with_igo(text_list: List[str]) -> List[str]:
    result = []
    i = 0
    while i < len(text_list):
        if text_list[i].endswith('/'):
            if i + 1 < len(text_list):
                text_list[i] = text_list[i][:-1] + text_list[i + 1]
                i += 1
            result.append(text_list[i])
        elif text_list[i].startswith('/'):
            if result:
                result[-1] += text_list[i]
            else:
                result.append(text_list[i])
        else:
            result.append(text_list[i])
        i += 1
    return result


def level_word_count(auto_text, manual_text):
    for i in range(max(len(auto_text), len(manual_text))):
        try:
            seq1 = SequenceMatcher(a=auto_text[i], b=manual_text[i]).ratio()
            seq2 = SequenceMatcher(a=auto_text[i] + auto_text[i + 1], b=manual_text[i]).ratio()
            seq3 = SequenceMatcher(a=auto_text[i], b=manual_text[i] + manual_text[i + 1]).ratio()
            if seq2 > seq1 and seq2 > seq3:
                auto_text[i] = auto_text[i] + ' ' + auto_text[i + 1]
                for j in range(i+1, len(auto_text) - 1):
                    auto_text[j] = auto_text[j + 1]
                auto_text.pop()
            if seq3 > seq2 and seq3 > seq1:
                manual_text[i] = manual_text[i] + manual_text[i + 1]
                for j in range(i+1, len(manual_text) - 1):
                    manual_text[j] = manual_text[j + 1]
                manual_text.pop()
        except IndexError:
            break


def process_and_save_json(ocr_file_path: str, man_file_path: str) -> (int, int):
    with open(ocr_file_path, 'r', encoding='utf-8') as file:
        ocr_data = json.load(file)

    with open(man_file_path, 'r', encoding='utf-8') as file:
        man_data = json.load(file)

    len_ocr = 0
    len_man = 0

    for key in ocr_data.keys():
        if key in man_data:
            ocr_text = glue_words_with_igo(ocr_data[key].split())
            man_text = glue_words_with_igo(man_data[key].split())

            level_word_count(ocr_text, man_text)

            ocr_data[key] = ocr_text
            man_data[key] = man_text

            len_ocr += len(ocr_text)
            len_man += len(man_text)

    with open(ocr_file_path, 'w', encoding='utf-8') as file:
        json.dump(ocr_data, file, ensure_ascii=False, indent=4)

    with open(man_file_path, 'w', encoding='utf-8') as file:
        json.dump(man_data, file, ensure_ascii=False, indent=4)

    return len_ocr, len_man


def main():
    for file_number in range(472, 501):
        ocr_file_path = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed', f'{file_number}_ocr.json')
        man_file_path = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed', f'{file_number}_man.json')

        len_ocr, len_man = process_and_save_json(ocr_file_path, man_file_path)

        print(f'File number {file_number}')
        print(f'Length of OCR Text: {len_ocr}')
        print(f'Total Length of Manual Text: {len_man}')
        print()


if __name__ == "__main__":
    main()
