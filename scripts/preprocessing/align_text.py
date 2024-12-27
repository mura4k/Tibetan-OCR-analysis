from difflib import SequenceMatcher
from typing import List
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
counter = 0


from difflib import SequenceMatcher

def level_string(auto_text, manual_text, file_number, string_number):
    # Ensure both are lists of tokens (e.g., words or symbols)
    if isinstance(auto_text, str):
        auto_text = auto_text.split()
    if isinstance(manual_text, str):
        manual_text = manual_text.split()

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

        # If "/" is present in auto_text but not in manual_text, insert "" in manual_text and increment index
        if auto_text[i] == '/' and manual_text[i] != '/':
            manual_text.insert(i, "")
            i += 1  # Move to the next token to avoid infinite loop
            min_length = min(len(auto_text), len(manual_text))  # Update min_length after insertion

        # If "/" is present in manual_text but not in auto_text, insert "" in auto_text and increment index
        elif manual_text[i] == '/' and auto_text[i] != '/':
            auto_text.insert(i, "")
            i += 1  # Move to the next token to avoid infinite loop
            min_length = min(len(auto_text), len(manual_text))  # Update min_length after insertion

        # Avoid concatenating words with '/' or '@' tokens
        elif seq_ocr_cat > seq_base and seq_ocr_cat > seq_man_cat and auto_text[i + 1] not in {'/', '@'}:
            auto_text[i] = auto_text[i] + ' ' + auto_text[i + 1]
            del auto_text[i + 1]

        elif seq_man_cat > seq_base and seq_man_cat > seq_ocr_cat and manual_text[i + 1] not in {'/', '@'}:
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
    # Post-process to handle 2 shads missing
    elif len(auto_text) == len(manual_text) - 2 and (manual_text[-1] == "/" and manual_text[-2] == "/"):
        auto_text.append("")
        auto_text.append("")
    elif len(manual_text) == len(auto_text) - 2 and (auto_text[-1] == "/" and auto_text[-2] == "/"):
        manual_text.append("")
        manual_text.append("")

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
    for file_number in list(range(3, 51)) + list(range(471, 501)):
        ocr_file_path = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed', f'{file_number}_ocr.json')
        man_file_path = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed',
                                     f'{file_number}_man.json')

        with open(ocr_file_path, 'r', encoding='utf-8') as ocr_file:
            ocr_data = json.load(ocr_file)
        with open(man_file_path, 'r', encoding='utf-8') as man_file:
            man_data = json.load(man_file)

        for string_num in ocr_data.keys():
            level_string(ocr_data[string_num], man_data[string_num], file_number, string_num)

        with open(ocr_file_path, 'w', encoding='utf-8') as file:
            json.dump(ocr_data, file, ensure_ascii=False, indent=4)
        with open(man_file_path, 'w', encoding='utf-8') as file:
            json.dump(man_data, file, ensure_ascii=False, indent=4)
    
    print(counter)



if __name__ == "__main__":
    main()