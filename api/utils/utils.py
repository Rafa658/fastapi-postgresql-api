import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from db.database import get_db
from datetime import datetime, timedelta
import jwt

from core.auth.config import config

params = config()

# Função auxiliar para executar consultas no banco de dados
def execute_query(query, args=None):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute(query, args)
    conn.commit()
    return cur

def check_db():
    query_todo = '''CREATE TABLE IF NOT EXISTS todos (
        todo_id SERIAL PRIMARY KEY,
        titulo VARCHAR (20),
        descr VARCHAR (50),
        status VARCHAR (1)
    )'''
    execute_query(query_todo)

def check_db_user():
    query_user = '''CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR (20),
        password VARCHAR (20)
    )'''
    execute_query(query_user)

def check_todo(todo: dict):
    check_query = f'''SELECT * FROM todos WHERE titulo = '{todo['titulo']}';'''
    check_cur = execute_query(check_query)
    if len(check_cur.fetchall()) == 0:
        return False
    
    return True

def authenticate_user(user: dict):
    query = f'''SELECT * FROM users 
        WHERE username = '{user['username']}' 
        AND password = '{user['password']}'
    ;'''
    cur = execute_query(query)

    user_info = cur.fetchone()
    if user_info is None:
        return None
    
    colnames = [desc[0] for desc in cur.description]
    return dict(zip(colnames, user_info))

def create_jwt_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes = int(params['access_token_expire_minutes']))
    data_to_encode = {**data, "exp": expire}
    encoded_jwt = jwt.encode(data_to_encode, params['secret_key'], algorithm = params['algorithm'])
    return encoded_jwt