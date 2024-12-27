import os
import re
import shutil


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def main():
    source_directory = os.path.join(BASE_DIR, 'data', 'pictures')

    pattern = re.compile(r'TCCG-001_(\d+)_crop\.jpg')

    for filename in os.listdir(source_directory):
        match = pattern.match(filename)
        if match:
            number = match.group(1)
            destination_directory = os.path.join(BASE_DIR, 'results1', str(int(number)))
            os.makedirs(destination_directory, exist_ok=True)
            new_filename = f'{int(number)}.jpg'
            old_file = os.path.join(source_directory, filename)
            new_file = os.path.join(destination_directory, new_filename)
            shutil.copy2(old_file, new_file)


if __name__ == '__main__':
    main()