import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from utils.utils import execute_query, check_db, check_todo
from api.auth.router import get_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@router.get('/')
def get_todos():
    query = 'SELECT * FROM todos ORDER BY todo_id'
    try:
        check_db()

        cur = execute_query(query)
        colnames = [desc[0] for desc in cur.description]
        return [dict(zip(colnames, row)) for row in cur.fetchall()]
    except Exception as e:
        print(e)
        raise Exception('Erro ao obter tarefas')

# rota protegida por autenticação
@router.post('/')
def create_todo(todo: dict, token: Annotated[str, Depends(oauth2_scheme)]):
    check_db()

    if 'titulo' not in todo or 'descr' not in todo:
        raise HTTPException(status_code=400, detail="Campos 'titulo' e 'descr' obrigatórios.")
    
    query = f'''INSERT INTO todos (titulo, descr, status)
        VALUES ('{todo['titulo']}', '{todo['descr']}', 'P'
    );'''
    execute_query(query)
    return f'Tarefa {todo["titulo"]} inserida com sucesso'

# rota protegida por autenticação
@router.put('/')
def update_todo(todo: dict, token: Annotated[str, Depends(oauth2_scheme)]):
    check_db()

    if not check_todo(todo):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    query = f'''UPDATE todos
        SET status = 'C'
        WHERE titulo = '{todo['titulo']}';
        '''
    execute_query(query)
    return f'Tarefa {todo["titulo"]} atualizada com sucesso'

# rota protegida por autenticação
@router.delete('/')
def delete_todo(todo: dict, token: Annotated[str, Depends(oauth2_scheme)]):
    check_db()

    if not check_todo(todo):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    query = f'''DELETE FROM todos
        WHERE titulo = '{todo['titulo']}';
        '''
    execute_query(query)
    return f'Tarefa {todo["titulo"]} deletada com sucesso'