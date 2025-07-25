from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Autor(Base):
    __tablename__ = 'autor'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    telefone = Column(String)
    bio = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    livros = relationship("Livro", back_populates='autor')


class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    livros = relationship('Livro', back_populates='categoria')


class Editora(Base):
    __tablename__ = 'editora'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    endereco = Column(String)
    telefone = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    livros = relationship('Livro', back_populates='editora')


class Livro(Base):
    __tablename__ = 'livro'
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    resumo = Column(String)
    ano = Column(Integer)
    paginas = Column(Integer)
    isbn = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Definição das chaves estrangeiras
    autor_id = Column(Integer, ForeignKey("autor.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    editora_id = Column(Integer, ForeignKey("editora.id"), nullable=False)

    # Relacionamentos
    autor = relationship("Autor", back_populates="livros")
    categoria = relationship("Categoria", back_populates="livros")
    editora = relationship("Editora", back_populates="livros")



class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=False, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)

