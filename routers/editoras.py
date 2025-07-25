import auth_utils
import models
import schemas

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db

from models import Usuario


router = APIRouter(prefix='/editoras')
models.Base.metadata.create_all(bind=engine)


@router.get('/', response_model=list[schemas.Editora])
def listar_editoras(db: Session = Depends(get_db)):
    return db.query(models.Editora).all()


@router.post('/', response_model=schemas.Editora, status_code=201)
def adicionar_editoras(nova_editora: schemas.EditoraCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    editora = models.Editora(nome=nova_editora.nome, telefone=nova_editora.telefone, endereco=nova_editora.endereco)
    db.add(editora)
    db.commit()
    db.refresh(editora)

    return editora


@router.get('/{editora_id}', response_model=schemas.Editora)
def mostrar_editora_por_id(editora_id: int, db: Session = Depends(get_db)):
    editora = db.query(models.Editora).get(editora_id)
    if editora:
        return editora

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Editora não encontrada.')


@router.patch('/{editora_id}', response_model=schemas.Editora)
def editar_editora(editora_id: int, editora_atualizada: schemas.EditoraBase, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    editora = db.query(models.Editora).get(editora_id)
    if not editora:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Editora não encontrada.')

    editora.nome = editora_atualizada.nome
    editora.telefone = editora_atualizada.telefone
    editora.endereco = editora_atualizada.endereco
    db.commit()
    db.refresh(editora)

    return editora


@router.delete('/{editora_id}', status_code=204)
def remover_editora(editora_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    editora = db.query(models.Editora).get(editora_id)
    if not editora:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Editora não encontrada.')

    db.delete(editora)
    db.commit()
    return

