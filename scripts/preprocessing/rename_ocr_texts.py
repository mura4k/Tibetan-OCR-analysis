import re
import os
import shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def main():
    source_directory = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'raw')
    destination_directory = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed')

    pattern = re.compile(r'TCCG-001_(\d+)_crop\.txt')

    os.makedirs(destination_directory, exist_ok=True)

    for filename in os.listdir(source_directory):
        match = pattern.match(filename)
        if match:
            number = match.group(1)
            new_filename = f'{int(number)}_ocr.txt'
            old_file = os.path.join(source_directory, filename)
            new_file = os.path.join(destination_directory, new_filename)
            shutil.copy2(old_file, new_file)


if __name__ == '__main__':
    main()
