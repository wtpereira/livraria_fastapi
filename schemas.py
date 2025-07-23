from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Schemas do Autor
class AutorBase(BaseModel):
    nome: str = Field(..., min_length=3)
    fone: str = Field(..., min_length=3)
    biografia: Optional[str] = Field(None, min_length=3)


class AutorCreate(AutorBase):
    email: EmailStr


class Autor(AutorCreate):
    id: int

    # Ele permite que a leitura da varíavel seja feita dessas duas formas:
    # autor['nome']
    # autor.nome
    class Config:
        orm_mode = True

# Schemas da Categoria
class CategoriaBase(BaseModel):
    nome: str = Field(..., min_length=3)


class CategoriaCreate(CategoriaBase):
    pass


class Categoria(CategoriaBase):
    id: int

    class Config:
        orm_mode = True


# Schemas da Editora
class EditoraBase(BaseModel):
    nome: str = Field(..., min_length=3)
    fone: str = Field(..., min_length=3)
    endereco: str = Field(min_length=3)


class EditoraCreate(EditoraBase):
    pass

class Editora(EditoraBase):
    id: int

    class Config:
        orm_mode = True


# Schemas do Livro
class LivroBase(BaseModel):
    titulo: str = Field(..., min_length=3)
    resumo: Optional[str] = Field(None, min_length=3)
    ano: Optional[int] = Field(None)
    paginas: int
    isbn: Optional[str] = Field(None, min_length=3)


class LivroCreate(LivroBase):
    autor_id: int
    categoria_id: int
    editora_id: int


class Livro(LivroBase):
    id: int
    autor: Autor
    categoria: Categoria
    editora: Editora

    class Config:
        orm_mode = True


# Schema do Usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str = Field(..., min_length=8)


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        orm_mode = True
