import auth_utils
import models
import schemas

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db

from models import Usuario

router = APIRouter(prefix='/categorias')
models.Base.metadata.create_all(bind=engine)


@router.get('/', response_model=list[schemas.Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(models.Categoria).all()


@router.post('/', response_model=schemas.Categoria, status_code=201)
def adicionar_categorias(nova_categoria: schemas.CategoriaCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    categoria = models.Categoria(nome=nova_categoria.nome)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    return categoria


@router.get('/{categoria_id}', response_model=schemas.Categoria)
def mostrar_categoria_por_id(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(models.Categoria).get(categoria_id)
    if categoria:
        return categoria

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada.')


@router.patch('/{categoria_id}', response_model=schemas.Categoria)
def editar_categoria(categoria_id: int, categoria_atualizada: schemas.CategoriaBase, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    categoria = db.query(models.Categoria).get(categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada.')

    categoria.nome = categoria_atualizada.nome
    db.commit()
    db.refresh(categoria)

    return categoria


@router.delete('/{categoria_id}', status_code=204)
def remover_categoria(categoria_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    categoria = db.query(models.Categoria).get(categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada.')

    db.delete(categoria)
    db.commit()

    return

