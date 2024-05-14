import pandas as pd
import sqlite3


def parse_excel(file_path, db_path="tibetan_syllables.db"):
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


excel_file_path = "freq_dict.xlsx"

success = parse_excel(excel_file_path)
if success:
    print("Parsing and database insertion successful!")
else:
    print("Parsing failed. Please check the error message.")
