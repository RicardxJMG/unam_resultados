from pathlib import Path
from typing import Generator, Optional, List
from contextlib import contextmanager
import sqlite3 as sql
import pandas as pd


class DataManager:
    """Clase para gestionar la conexión y consultas a la base de datos."""
    
    def __init__(self, data_path: Path):
        """
        Inicializa el gestor de datos.
        
        Args:
            data_path (Path): Ruta al archivo de la base de datos SQLite
        """
        self.data_path = data_path
        if not self.data_path.exists():
            raise FileNotFoundError(f"No se encontró la base de datos en: {data_path}")
        
    @contextmanager
    def database_connection(self) -> Generator[sql.Connection, None, None]:
        """Gestiona la conexión a la base de datos de forma segura."""
        conn: Optional[sql.Connection] = None
        try: 
            conn = sql.connect(self.data_path)
            conn.row_factory = sql.Row  # Permite acceder a columnas por nombre
            yield conn
        except sql.Error as e:
            print(f'Error al conectarse a la base de datos\n Error: {e}') 
            raise            
        finally:
            if conn is not None: 
                conn.close()
                
    def get_query(self, query: str) -> pd.DataFrame:
        """Ejecuta una consulta SQL y retorna los resultados como DataFrame."""
        with self.database_connection() as conn: 
            return pd.read_sql(sql=query, con=conn)
        
    def load_queries(self, queries_path: Path, n: int = 1) -> List[pd.DataFrame]:
        """
        Carga y ejecuta múltiples consultas SQL desde archivos llamados q{n}.sql
        
        Args:
            queries_path (Path): Ruta al directorio con los archivos SQL
            n (int): Número de consultas a cargar
            
        Returns:
            List[pd.DataFrame]: Lista con los resultados de cada consulta
        """
        dfs: List[pd.DataFrame] = []
        for i in range(n):
            query_file = queries_path / f'q{i+1}.sql'
            if not query_file.exists():
                raise FileNotFoundError(f"No se encontró el archivo: {query_file}")
            query = query_file.read_text(encoding='utf-8')
            dfs.append(self.get_query(query))  # Corregido: Llamada al método con el argumento
            
        return dfs