#%%
import matplotlib.pyplot as plt 
import seaborn as sns 
# import plotly
import pandas as pd 
from pathlib import Path
import sqlite3 as sql 
import numpy as np

#%%
DATA_PATH = Path(__file__).parent / "datos" / "processed" / "unam_resultados.db"

def connect_database(data_path: str = DATA_PATH) -> sql.Connection|None: 
    con = None
    try: 
        con = sql.connect(DATA_PATH)
    except:
        print("Error al conectarse a la base de datos")
    finally:
        return None


if __name__ == '__main__':
    pass 


