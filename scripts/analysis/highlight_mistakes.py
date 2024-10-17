from difflib import SequenceMatcher
import os
import json
import re
import sqlite3
from collections import Counter
from typing import Dict, List


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_DIR = os.path.join(BASE_DIR, 'data', 'tibetan_syllables.db')

def search_in_db(search_word: str):
    # Path to SQLite database file
    db_path = DB_DIR

    table_name = 'tibetan_syllables'
    syllable_column = 'Transliteration'
    count_column = 'SymbolCount'

    search_word = search_word

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to check if the word exists in the column
    query = f"SELECT {count_column} FROM {table_name} WHERE {syllable_column} = ?"
    try:
        # Execute the query with the search word
        cursor.execute(query, (search_word,))
        # Fetch one result (since we only need to know if it exists)
        result = cursor.fetchone()
        if result:
            conn.close()
            return result[0]

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    conn.close()
    return -1


def find_mistakes(ocr_data: Dict[int, List], man_data: Dict[int, List], syllable_mistakes) -> List[tuple]:
    all_mistakes = []  # List with tuples containing mistakes

    for key in ocr_data.keys():  # Iterate through every string

        # If the first string is empty, it is str type, so it is converted to empty list
        if isinstance(ocr_data[key], str):
            ocr_data[key] = [ocr_data[key]]
        if isinstance(man_data[key], str):
            man_data[key] = [man_data[key]]

        if not ocr_data[key]:  # Handle not recognised first string
            ocr_data[key] = ["<mistake></mistake>"]
            man_data[key] = ["<error-prone>" + ' '.join(man_data[key]) + "</error-prone>"]

        for i in range(len(man_data[key])):
            seq = SequenceMatcher(a=ocr_data[key][i].replace(' ', ''), b=man_data[key][i].replace(' ', ''))
            if seq.ratio() != 1:
                # pattern = re.compile(r"[a-zA-Z']+")
                # try:
                #     if pattern.match(man_data[key][i])[0] == pattern.match(ocr_data[key][i])[0]:
                #
                #     print()
                # except:
                #     print()
                syllable_number = search_in_db(man_data[key][i])
                if syllable_number != -1:
                    syllable_mistakes[syllable_number] += 1
                all_mistakes.append((ocr_data[key][i], man_data[key][i]))
                ocr_data[key][i] = "<mistake>" + ocr_data[key][i] + "</mistake>"
                man_data[key][i] = "<error-prone>" + man_data[key][i] + "</error-prone>"

        # Join the lists back into a single string for each key
        ocr_data[key] = " ".join(ocr_data[key])
        man_data[key] = " ".join(man_data[key])
    return all_mistakes


def main():
    syllable_mistakes = Counter()
    for file_number in list(range(2, 51)) + list(range(471, 501)):
        ocr_file_path = os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed', f'{file_number}_ocr.json')
        man_file_path = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed',
                                     f'{file_number}_man.json')

        with open(ocr_file_path, 'r', encoding='utf-8') as file:
            ocr_data = json.load(file)

        with open(man_file_path, 'r', encoding='utf-8') as file:
            man_data = json.load(file)

        if os.path.exists(ocr_file_path) and os.path.exists(man_file_path):

            result_dir = os.path.join(BASE_DIR, 'results1', str(file_number))
            os.makedirs(result_dir, exist_ok=True)
            mistakes = find_mistakes(ocr_data, man_data, syllable_mistakes)
            print(mistakes)
            print(ocr_data)
            print(man_data)



            # with open(os.path.join(result_dir, f'{file_number}_ocr.json'), 'w', encoding='utf-8') as ocr_result_file:
            #     json.dump(ocr_data, ocr_result_file, ensure_ascii=False, indent=4)
            #
            # with open(os.path.join(result_dir, f'{file_number}_man.json'), 'w', encoding='utf-8') as man_result_file:
            #     json.dump(man_data, man_result_file, ensure_ascii=False, indent=4)

            print(f'Processed file number {file_number}')
    mistakes_count = syllable_mistakes.total()
    for i in syllable_mistakes.keys():
        syllable_mistakes[i] /= mistakes_count
    print(syllable_mistakes)


if __name__ == "__main__":
    main()
