import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def process_first_texts_to_json(file_path):
    texts = {}

    with open(file_path, 'r') as f:
        lines = [line.rstrip().replace("[", "").replace("]", "") for line in f if line != '\n']

    flag = 1
    for idx, line in enumerate(lines):
        # split line into key and value based on the closing brace
        try:
            _, value = line.strip().split('} ', 1)
            texts[idx + 1] = value  # use 1-based indexing (1st string, 2nd string etc.)
        except ValueError:
            if idx == len(lines) - 1:
                break
            else:
                print(f"Need manual help in {file_path} in {idx + 1} line")
                flag = 0

    json_file_path = os.path.splitext(file_path)[0] + '.json'

    # save the dictionary to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(texts, json_file, ensure_ascii=False, indent=4)

    # delete the original text file
    if flag == 1:
        os.remove(file_path)


def process_second_texts_to_json(file_path):
    texts = {}

    with open(file_path, 'r') as f:
        lines = [line.rstrip() for line in f if line != '\n']

    for idx, line in enumerate(lines):
        texts[idx + 1] = line  # use 1-based indexing (1st string, 2nd string etc.)

    json_file_path = os.path.splitext(file_path)[0] + '.json'

    # save the dictionary to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(texts, json_file, ensure_ascii=False, indent=4)

    # delete the original text file
    os.remove(file_path)


def main():
    for i in range(3, 56):
        fp = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed', str(i) + '_man.txt')
        process_first_texts_to_json(fp)
    for i in range(471, 501):
        fp = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed', str(i) + '_man.txt')
        process_second_texts_to_json(fp)


if __name__ == '__main__':
    main()