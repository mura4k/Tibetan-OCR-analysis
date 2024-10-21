from typing import List, Dict, Tuple
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

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
    # in case first string is not recognised in OCR file, add empty string to the beginning
    if len(ocr_data) == len(man_data) - 1:
        new_ocr_data = {"1": ""}
        for key in sorted(ocr_data.keys(), key=int):
            new_ocr_data[str(int(key) + 1)] = ocr_data[key]
        ocr_data = new_ocr_data

    # tokenize strings in ocr and man files
    for string_num in ocr_data.keys():
        ocr_data[string_num] = string_tokenizer(ocr_data[string_num])
    for string_num in man_data.keys():
        man_data[string_num] = string_tokenizer(man_data[string_num])

    return ocr_data, man_data

def main():
    for file_number in list(range(3, 51)) + list(range(471, 501)):
        ocr_file_path = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed', f'{file_number}_ocr.json')
        man_file_path = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed',
                                        f'{file_number}_man.json')

        with open(ocr_file_path, 'r', encoding='utf-8') as ocr_file:
            ocr_data = json.load(ocr_file)
        with open(man_file_path, 'r', encoding='utf-8') as man_file:
            man_data = json.load(man_file)
    
        ocr_data, man_data = tokenize_files(ocr_data, man_data)

        with open(ocr_file_path, 'w', encoding='utf-8') as file:
            json.dump(ocr_data, file, ensure_ascii=False, indent=4)
        with open(man_file_path, 'w', encoding='utf-8') as file:
            json.dump(man_data, file, ensure_ascii=False, indent=4)

