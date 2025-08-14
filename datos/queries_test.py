#%%
import pandas as pd
import sqlite3 as sql 
from create_db import DB_PATH
#%%

def init_connection() -> sql.Connection|None:
    conn = None
    try:
        conn = sql.connect(DB_PATH)
    except sql.Error as e: 
        print('Ocurrió un error al iniciar conexión')        
    finally: 
        return conn


if __name__ == '__main__': 
    
    conn  = init_connection()
    with open('./queries/q1.sql', 'r') as f: query = f.read()
    print(pd.read_sql(query, con = conn))
    conn.close()