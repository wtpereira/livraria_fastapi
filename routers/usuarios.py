import auth_utils
import models
import os
import schemas

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Usuario


router = APIRouter(prefix='/usuarios')
models.Base.metadata.create_all(bind=engine)


@router.post('/', response_model=schemas.UsuarioOut, status_code=201, summary='Cadastrar Usuários', description='Endpoint para cadastrar novos usuários.')
def criar_usuario(novo_usuario: schemas.UsuarioCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    senha_hash = auth_utils.gerar_hash_senha(novo_usuario.senha)
    novo_usuario = models.Usuario(nome=novo_usuario.nome, email=novo_usuario.email, senha_hash=senha_hash)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

