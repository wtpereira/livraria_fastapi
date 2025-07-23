import auth_utils
import models
import schemas

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, get_db

from models import Usuario


router = APIRouter(prefix='/livros')
models.Base.metadata.create_all(bind=engine)


@router.get('/', response_model=list[schemas.Livro])
def listar_livros(db: Session = Depends(get_db)):
    return db.query(models.Livro).all()


@router.post('/', response_model=schemas.Livro, status_code=201)
def adicionar_livro(novo_livro: schemas.LivroCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    autor = db.query(models.Autor).get(novo_livro.autor_id)
    if not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Autor não encontrado.')

    categoria = db.query(models.Categoria).get(novo_livro.categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada.')

    editora = db.query(models.Editora).get(novo_livro.editora_id)
    if not editora:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Editora não encontrada.')

    livro = models.Livro(
        titulo=novo_livro.titulo,
        paginas=novo_livro.paginas,
        ano=novo_livro.ano,
        resumo=novo_livro.resumo,
        isbn=novo_livro.isbn,
        autor_id=novo_livro.autor_id,
        categoria_id=novo_livro.categoria_id,
        editora_id=novo_livro.editora_id
    )
    db.add(livro)
    db.commit()
    db.refresh(livro)

    return livro


@router.get('/{livro_id}', response_model=schemas.Livro)
def mostrar_livro_por_id(livro_id: int, db: Session = Depends(get_db)):
    livro = db.query(models.Livro).get(livro_id)
    if livro:
        return livro

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Livro não encontrado.')


@router.patch('/{livro_id}', response_model=schemas.Livro)
def editar_livro(livro_id: int, livro_atualizado: schemas.LivroCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    livro = db.query(models.Livro).get(livro_id)
    if not livro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Livro não encontrado.')

    autor = db.query(models.Autor).get(livro_atualizado.autor_id)
    if not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Autor não encontrado.')

    categoria = db.query(models.Categoria).get(livro_atualizado.categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada.')

    editora = db.query(models.Editora).get(livro_atualizado.editora_id)
    if not editora:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Editora não encontrada.')

    livro.titulo = livro_atualizado.titulo
    livro.resumo = livro_atualizado.resumo
    livro.ano = livro_atualizado.ano
    livro.paginas = livro_atualizado.paginas
    livro.isbn = livro_atualizado.isbn
    livro.autor_id = livro_atualizado.autor_id
    livro.categoria_id = livro_atualizado.categoria_id
    livro.editora_id = livro_atualizado.editora_id

    db.commit()
    db.refresh(livro)

    return livro


@router.delete('/{livro_id}', status_code=204)
def remover_livro(livro_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(auth_utils.obter_usuario_logado)):
    livro = db.query(models.Livro).get(livro_id)
    if not livro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Livro não encontrado.')

    db.delete(livro)
    db.commit()

    return

