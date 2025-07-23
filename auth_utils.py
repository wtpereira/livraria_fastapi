import os

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Usuario

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)


def criar_token_acesso(data: dict, expires_delta: timedelta | None = None):
    to_enconde = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30))))
    to_enconde.update({'exp': expire})
    return jwt.encode(to_enconde, os.environ.get('SECRET_KEY', 'uma-senha-muito-forte'), algorithm=os.environ.get('ALGORITHM', 'HS256'))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def obter_usuario_logado(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Não Autorizado', headers={'WWW-Authenticate': 'Bearer'})
    try:
        print('token: ', token)
        payload = jwt.decode(token, os.environ.get('SECRET_KEY', 'uma-senha-muito-forte'), algorithms=[os.environ.get('ALGORITHM', 'HS256')])
        print('paylod: ', payload)
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        
    except JWTError as ex:
        print(ex)
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.email == username).first()
    if not usuario:
        raise credentials_exception

    return usuario

