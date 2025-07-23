import auth_utils
import models
import schemas
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from routers import autores, categorias, editoras, livros, usuarios

origins = [
    'http://localhost:8000',
    'http://localhost:5173'
    # Adicione outros domínios conforme necessidade.
]

app = FastAPI(title='API REST Livraria', description='API para gerenciar os registros da nossa Livraria.', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Incluir os roteadores
app.include_router(autores.router)
app.include_router(categorias.router)
app.include_router(editoras.router)
app.include_router(livros.router)
app.include_router(usuarios.router)


@app.get('/')
def hello_world():
    return {'Hello': 'World!'}


@app.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == form_data.username).first()
    if not usuario or not auth_utils.verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciais inválidas!')

    token = auth_utils.criar_token_acesso(data={'sub': usuario.email})
    user_out = schemas.UsuarioOut(id=usuario.id, nome=usuario.nome, email=usuario.email)

    return {'access_token': token, 'token_type': 'bearer', 'user': user_out}
