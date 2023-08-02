import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import psycopg2
from core.database.config import config

def get_db():
    params = config()
    try:
        conn = psycopg2.connect(**params)
        print('Conectado à DB')
        
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    get_db()