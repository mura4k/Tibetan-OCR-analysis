import os
import json
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    source_directory = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed')
    destination_directory = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed')

    os.makedirs(destination_directory, exist_ok=True)

    # regex pattern to match and remove the initial four numbers
    pattern = re.compile(r'^\d+ \d+ \d+ \d+ ')

    for filename in os.listdir(source_directory):
        if filename.endswith('_ocr.txt'):
            # extract the number from the filename
            number = int(filename.split('_')[0])

            with open(os.path.join(source_directory, filename), 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # process each line, numbering them starting from 1
            numbered_lines = {}
            for i, line in enumerate(lines, start=1):
                if 2 <= number <= 50:
                    # remove the leading numbers for files numbered 2 to 50
                    cleaned_line = pattern.sub('', line.strip())
                elif 471 <= number <= 500:
                    # keep the line as is for files numbered 471 to 500
                    cleaned_line = line.strip()
                else:
                    # skip files that do not match the criteria
                    continue

                numbered_lines[i] = cleaned_line
            os.remove(os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed', filename))

            # output JSON file
            json_filename = f"{number}_ocr.json"

            # write the numbered lines to the JSON file
            with open(os.path.join(destination_directory, json_filename), 'w', encoding='utf-8') as f:
                json.dump(numbered_lines, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
