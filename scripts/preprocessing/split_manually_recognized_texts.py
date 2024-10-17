import re
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def main():
    # Path to transliterated pages 2-55
    input_file_1 = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'raw', 'transliteration 001_055.txt')
    with open(input_file_1, "r") as f:
        text = f.read()
    text = re.split(r"\nPage \d\d\d\d\n", text)

    # Save each page's text to a separate file
    for i in range(2, 56):
        filename = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed', f"{i}_man.txt")
        with open(filename, "w") as f:
            f.write(text[i - 2])

    # Path to transliterated pages 471-500
    input_file_2 = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'raw', 'transliteration TCCG-001_471_500.txt')
    with open(input_file_2, "r") as f:
        text = f.read()
    text = re.split(r'\nPage \d\d\d\d\n', text)

    # Save each page's text to a separate file
    for i in range(471, 501):
        filename = os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed', f"{i}_man.txt")
        with open(filename, "w") as f:
            f.write(text[i - 471])


if __name__ == '__main__':
    main()
