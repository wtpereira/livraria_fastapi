import auth_utils
import models
import schemas

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, get_db

from models import Usuario


router = APIRouter(prefix='/autores')
models.Base.metadata.create_all(bind=engine)


@router.get('/', response_model=list[schemas.Autor], summary='Listar todos os autores', description='Endpoint para trazer a listagem de todos os autores cadastrados no sistema.')
def listar_autores(db: Session = Depends(get_db)):
    return db.query(models.Autor).all()



def get_user_by_email(db: Session, email: str):
    """ Get user by email"""
    return db.query(models.Autor).filter(models.Autor.email == email).first()

@router.post('/', response_model=schemas.Autor, status_code=201)
def adicionar_autores(novo_autor: schemas.AutorCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    autor_db = get_user_by_email(db, email=novo_autor.email)
    if autor_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='E-mail já cadastrado!')

    autor = models.Autor(nome=novo_autor.nome, email=novo_autor.email, telefone=novo_autor.telefone, bio=novo_autor.bio)
    db.add(autor)
    db.commit()
    db.refresh(autor)

    return autor


@router.get('/{autor_id}', response_model=schemas.Autor)
def mostrar_autor_por_id(autor_id: int, db: Session = Depends(get_db)):
    autor = db.query(models.Autor).get(autor_id)
    if autor:
        return autor

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Autor não encontrado.')


@router.patch('/{autor_id}', response_model=schemas.Autor)
def editar_autor(autor_id: int, autor_atualizado: schemas.AutorBase, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    autor = db.query(models.Autor).get(autor_id)
    if not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Autor não encontrado.')

    autor.nome = autor_atualizado.nome
    autor.telefone = autor_atualizado.telefone
    autor.bio = autor_atualizado.bio
    db.commit()
    db.refresh(autor)

    return autor


@router.delete('/{autor_id}', status_code=204)
def remover_autor(autor_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    autor = db.query(models.Autor).get(autor_id)
    if not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Autor não encontrado.')

    db.delete(autor)
    db.commit()
    return

