from difflib import SequenceMatcher
import os
import json


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def find_mistakes(ocr_data, man_data):
    for key in ocr_data.keys():
        if key in man_data:
            result = []
            if isinstance(ocr_data[key], str):
                ocr_data[key] = [ocr_data[key]]
            if isinstance(man_data[key], str):
                man_data[key] = [man_data[key]]

            if not ocr_data[key]:
                ocr_data[key] = ["<mistake></mistake>"]
                man_data[key] = ["<error-prone>" + ' '.join(man_data[key]) + "</error-prone>"]

            for i in range(len(man_data[key])):
                seq = SequenceMatcher(a=ocr_data[key][i], b=man_data[key][i])
                if seq.ratio() != 1:
                    result.append((ocr_data[key][i], man_data[key][i]))
                    ocr_data[key][i] = "<mistake>" + ocr_data[key][i] + "</mistake>"
                    man_data[key][i] = "<error-prone>" + man_data[key][i] + "</error-prone>"

            # Join the lists back into a single string for each key
            ocr_data[key] = " ".join(ocr_data[key])
            man_data[key] = " ".join(man_data[key])
    return result


def main():
    for file_number in list(range(2, 51)) + list(range(471, 501)):
        ocr_file_path = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed', f'{file_number}_ocr.json')
        man_file_path = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed',
                                     f'{file_number}_man.json')

        with open(ocr_file_path, 'r', encoding='utf-8') as file:
            ocr_data = json.load(file)

        with open(man_file_path, 'r', encoding='utf-8') as file:
            man_data = json.load(file)

        if os.path.exists(ocr_file_path) and os.path.exists(man_file_path):

            result_dir = os.path.join(BASE_DIR, 'results', str(file_number))
            os.makedirs(result_dir, exist_ok=True)
            mistakes = find_mistakes(ocr_data, man_data)

            with open(os.path.join(result_dir, f'{file_number}_ocr.json'), 'w', encoding='utf-8') as ocr_result_file:
                json.dump(ocr_data, ocr_result_file, ensure_ascii=False, indent=4)

            with open(os.path.join(result_dir, f'{file_number}_man.json'), 'w', encoding='utf-8') as man_result_file:
                json.dump(man_data, man_result_file, ensure_ascii=False, indent=4)

            print(f'Processed file number {file_number}')


if __name__ == "__main__":
    main()
