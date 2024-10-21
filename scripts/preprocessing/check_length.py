import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def main():
    counter = 0
    for file_number in list(range(3, 51)) + list(range(471, 501)):
        ocr_file_path = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed', f'{file_number}_ocr.json')
        man_file_path = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed',
                                     f'{file_number}_man.json')

        with open(ocr_file_path, 'r', encoding='utf-8') as ocr_file:
            ocr_data = json.load(ocr_file)
        with open(man_file_path, 'r', encoding='utf-8') as man_file:
            man_data = json.load(man_file)

        if len(ocr_data)!= len(man_data):
            print(f'File {file_number} has different number of lines')
            print(f'OCR: {len(ocr_data)}')
            print(f'MAN: {len(man_data)}')
            print()
    
    print(counter)



if __name__ == "__main__":
    main()