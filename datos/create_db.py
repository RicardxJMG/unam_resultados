#%%
import os 
import pandas as pd
import sqlite3 as sql 
# from sqlalchemy import create_engine

DB_DIR = './processed'
DB_FILE = 'unam_resultados_2025.db'
EXCEL_FILE = os.path.join(DB_DIR, 'data_clean.xlsx')
SHEET_NAMES = [ 'areas_info',
                'facultades_info',
                'carreras_info',
                'resultados_2025',
                'oferta_2024_2025']

SQL_SCHEMA_FILE = './queries/create_db.sql' 

def create_database(db_path:str, schema_path:str) -> sql.Connection:
    with open(schema_path, 'r') as f: query_script = f.read()
    
    conn = sql.connect(db_path)
    cursor = conn.execute("PRAGMA foreign_keys = ON;")
    cursor.executescript(query_script)
    conn.commit()
    return conn

def excel_to_db(conn: sql.Connection, excel_path:str, sheets: list) -> None: 
    dfs = pd.read_excel(io=excel_path, sheet_name=sheets)
    for sheet, df in dfs.items(): 
        df.to_sql(name=sheet, con=conn,if_exists='append',index=False)
        print(f'Datos insertados en la tabla {sheet}')
        
        
def main() -> None:
    os.makedirs(DB_DIR, exist_ok=True)
    db_path = os.path.join(DB_DIR, DB_FILE)    
    
    try: 
        conn = create_database(db_path= db_path, schema_path=SQL_SCHEMA_FILE)
        #testing
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
    
    