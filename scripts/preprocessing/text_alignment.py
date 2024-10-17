from difflib import SequenceMatcher
from typing import List, Dict, Tuple
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
counter = 0

def string_tokenizer(text: str) -> List[str]:
    text = text.replace('  ', ' ')
    result = []
    shad = '/'
    igo = '@'
    prev = ''

    for char in text:
        if char == ' ':
            if prev:
                result.append(prev)
            prev = ''
        elif char in {shad, igo}:
            if prev and prev[-1] == char:
                prev += char
            else:
                if prev:
                    result.append(prev)
                prev = char
        else:
            if prev and prev[-1] in {shad, igo}:
                result.append(prev)
                prev = char
            else:
                prev += char

    if prev:
        result.append(prev)

    return result


def tokenize_files(ocr_data: Dict, man_data: Dict) -> Tuple[Dict, Dict]:
    if len(ocr_data) == len(man_data) - 1:
        new_ocr_data = {"1": ""}
        for key in sorted(ocr_data.keys(), key=int):
            new_ocr_data[str(int(key) + 1)] = ocr_data[key]
        ocr_data = new_ocr_data

    for string_num in ocr_data.keys():
        ocr_data[string_num] = string_tokenizer(ocr_data[string_num])
    for string_num in man_data.keys():
        man_data[string_num] = string_tokenizer(man_data[string_num])

    return ocr_data, man_data


def level_word_count(auto_text, manual_text, file_number, string_number):
    min_length = min(len(auto_text), len(manual_text))

    # If the length of the shorter text is 0 (first line in OCR is not recognised, end leveling)
    if min_length == 0:
        return

    i = 0
    while i < min_length:
        seq_base = SequenceMatcher(a=auto_text[i], b=manual_text[i]).ratio()

        seq_ocr_cat = SequenceMatcher(a=auto_text[i] + (auto_text[i + 1] if i + 1 < len(auto_text) else ''),
                                      b=manual_text[i]).ratio()

        seq_man_cat = SequenceMatcher(a=auto_text[i],
                                      b=manual_text[i] + (
                                          manual_text[i + 1] if i + 1 < len(manual_text) else '')).ratio()

        if seq_ocr_cat > seq_base and seq_ocr_cat > seq_man_cat:
            auto_text[i] = auto_text[i] + ' ' + auto_text[i + 1]
            del auto_text[i + 1]

        elif seq_man_cat > seq_base and seq_man_cat > seq_ocr_cat:
            manual_text[i] = manual_text[i] + ' ' + manual_text[i + 1]
            del manual_text[i + 1]

        else:
            i += 1  # Only move forward if no concatenation occurred
        min_length = min(len(auto_text), len(manual_text))

    # Post-process to handle one-off length differences
    if len(auto_text) == len(manual_text) - 1:
        manual_text[-2] += ' ' + manual_text[-1]
        manual_text.pop()
    elif len(manual_text) == len(auto_text) - 1:
        auto_text[-2] += ' ' + auto_text[-1]
        auto_text.pop()

    if len(auto_text) != len(manual_text) and len(auto_text) != 0:
        print()
        global counter
        counter += 1
        print(f"Файл номер {file_number}, строка {string_number}, требует ручной разметки")
        print(len(auto_text))
        print(auto_text)
        print(len(manual_text))
        print(manual_text)
        print()


def main():
    for file_number in list(range(2, 51)) + list(range(471, 501)):
        ocr_file_path = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed', f'{file_number}_ocr.json')
        man_file_path = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed',
                                     f'{file_number}_man.json')

        with open(ocr_file_path, 'r', encoding='utf-8') as ocr_file:
            ocr_data = json.load(ocr_file)
        with open(man_file_path, 'r', encoding='utf-8') as man_file:
            man_data = json.load(man_file)

        
        ocr_data, man_data = tokenize_files(ocr_data, man_data)
        for string_num in ocr_data.keys():
            level_word_count(ocr_data[string_num], man_data[string_num], file_number, string_num)

        with open(ocr_file_path, 'w', encoding='utf-8') as file:
            json.dump(ocr_data, file, ensure_ascii=False, indent=4)
        with open(man_file_path, 'w', encoding='utf-8') as file:
            json.dump(man_data, file, ensure_ascii=False, indent=4)
    
    print(counter)



if __name__ == "__main__":
    main()
