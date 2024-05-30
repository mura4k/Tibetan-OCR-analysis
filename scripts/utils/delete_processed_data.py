import os
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def delete_processed_files():
    directories = [
        os.path.join(BASE_DIR, 'data', 'ocr_texts', 'processed'),
        os.path.join(BASE_DIR, 'data', 'manually_recognised_texts', 'processed')
    ]

    for directory in directories:
        files = glob.glob(os.path.join(directory, '*'))
        for file in files:
            os.remove(file)
            print(f'Deleted: {file}')


if __name__ == "__main__":
    delete_processed_files()
