import os
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts', 'preprocessing')


def run_scripts():
    scripts = [
        'rename_ocr_texts.py',
        'split_manually_recognized_texts.py',
        'to_json_manually_recognized_texts.py',
        'to_json_ocr_texts.py'
    ]

    for script in scripts:
        script_path = os.path.join(SCRIPTS_DIR, script)
        if os.path.isfile(script_path):
            subprocess.run(['python', script_path], check=True)
            print(f'Ran script: {script}')
        else:
            print(f'Script not found: {script}')


if __name__ == "__main__":
    run_scripts()
