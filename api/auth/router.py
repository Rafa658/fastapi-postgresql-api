from fastapi import APIRouter, HTTPException
import jwt
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from utils.utils import execute_query, check_db_user, authenticate_user, create_jwt_token
from core.auth.config import config

router = APIRouter()
params = config()

@router.post('/')
def create_user(user: dict):
    check_db_user()

    if 'username' not in user or 'password' not in user:
        raise HTTPException(status_code=400, detail="Campos 'username' e 'password' obrigatórios.")
    
    query = f'''INSERT INTO users (username, password)
        VALUES ('{user['username']}', '{user['password']}'
    );'''
    execute_query(query)
    return f'Usuário {user["username"]} inserido com sucesso'

@router.post('/token')
def login_for_access_token(user: dict):
    user = authenticate_user(user)
    if user is None:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = create_jwt_token({"sub": user['username']})
    return {'access_token': token, 'token_type': 'bearer'}

@router.get('/protected')
def get_user(data: dict):
    try:
        payload = jwt.decode(data["token"], params['secret_key'], algorithms=[params['algorithm']])
        return payload
        # return f'Bem vindo, {payload["sub"]}'
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado, favor fazer login novamente.")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido, favor fazer login novamente.")