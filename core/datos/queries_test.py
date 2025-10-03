#%%
from pathlib import Path
import pandas as pd
import sqlite3 as sql 
from create_db import DB_PATH
#%%

QUERIES_PATH  = Path(__file__).parent / 'queries'

def init_connection() -> sql.Connection|None:
    conn = None
    try:
        conn = sql.connect(DB_PATH)
    except sql.Error as e: 
        print('Ocurrió un error al iniciar conexión')        
    finally: 
        return conn

def df_query(query_path: Path, conn: sql.Connection) -> pd.DataFrame:
    with open(query_path, 'r') as f: query = f.read()
    return pd.read_sql(query, con = conn)

if __name__ == '__main__': 
    conn = init_connection()
    try: 
        df = df_query(query_path = QUERIES_PATH / 'q6.sql', conn= conn)    
        print(df.head())
        # df = pd.read_sql("SELECT * FROM oferta_2024_2025", con = conn)        
    except Exception as e:
        conn.close()
        print(f'Error: {e}')    
        
        
    conn.close()