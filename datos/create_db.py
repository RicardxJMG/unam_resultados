#%%
from pathlib import Path
import pandas as pd
import sqlite3 as sql 


DB_DIR = Path(__file__).parent / 'processed'
DB_FILE = 'unam_resultados_2025.db'
DB_PATH = DB_DIR / DB_FILE

EXCEL_FILE = DB_DIR / 'data_clean.xlsx'
SHEET_NAMES = [ 'areas_info',
                'facultades_info',
                'carreras_info',
                'carreras_descripcion',
                'resultados_2025',
                'oferta_2024_2025']

SQL_SCHEMA_FILE = Path(__file__).parent / 'queries'/ 'create_db.sql'


def create_database(db_path: Path, schema_path: Path) -> sql.Connection:
    with schema_path.open('r') as f: 
        query_script = f.read()
    
    conn = sql.connect(db_path)
    cursor = conn.execute("PRAGMA foreign_keys = ON;")
    cursor.executescript(query_script)
    conn.commit()
    return conn

def excel_to_db(conn: sql.Connection, excel_path: Path, sheets: list) -> None: 
    id_columns = {
        'id_carrera': 3,
        'id_facultad': 4,
        'id_aspirante': 6
    }
    
    dfs = pd.read_excel(io=excel_path, sheet_name=sheets)
    
    for sheet, df in dfs.items():
        for col in df.columns:
            if col in id_columns:
                df[col] = df[col].astype(str).str.zfill(id_columns[col])
        
        df.to_sql(name=sheet,con=conn,if_exists='append',index=False,
                  dtype={col: 'TEXT' for col in id_columns if col in df.columns})
        
        print(f'Datos insertados en la tabla {sheet}')
        
def main() -> None:
    try: 
        DB_DIR.mkdir(parents=True, exist_ok=True)
        
        conn = create_database(db_path=DB_PATH, schema_path=SQL_SCHEMA_FILE)
        print('-> Base de datos creada correctamente\n')
        excel_to_db(conn=conn, excel_path=EXCEL_FILE, sheets=SHEET_NAMES)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if 'conn' in locals():
            conn.close()
            print('\nConexión cerrada')

if __name__ == '__main__':
    main()
    
    