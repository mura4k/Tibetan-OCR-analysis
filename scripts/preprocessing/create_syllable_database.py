import pandas as pd
import sqlite3
import os


def parse_excel(file_path, db_path):
    try:
        df = pd.read_excel(file_path)
        df = df[df.columns.drop(list(df.filter(regex='Unnamed:')))]
        df['SymbolCount'] = df['Unicode'].apply(lambda x: len(str(x).split('&#')) - 1)

        conn = sqlite3.connect(db_path)
        df.to_sql('tibetan_syllables', conn, index=False, if_exists='replace', method='multi', chunksize=1000)
        conn.close()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

excel_file_path = os.path.join(BASE_DIR, 'data', 'freq_dict.xlsx')

db_file_path = os.path.join(BASE_DIR, 'data', 'tibetan_syllables.db')

success = parse_excel(excel_file_path, db_file_path)

if success:
    print("Parsing and database insertion successful!")
else:
    print("Parsing failed. Please check the error message.")
