from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.filme import FilmeCreate, FilmeUpdate, FilmeResponse
from app.services import filme_service

router = APIRouter(prefix="/filmes", tags=["Filmes"])


@router.get("/", response_model=List[FilmeResponse], summary="Lista todos os filmes")
def get_filmes(db: Session = Depends(get_db)):
    return filme_service.listar_filmes(db)


@router.get("/{id}", response_model=FilmeResponse, summary="Retorna um filme pelo ID")
def get_filme(id: int, db: Session = Depends(get_db)):
    filme = filme_service.buscar_filme_por_id(db, id)
    if not filme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filme com id {id} não encontrado.",
        )
    return filme


@router.post("/", response_model=FilmeResponse, status_code=status.HTTP_201_CREATED, summary="Cadastra um novo filme")
def post_filme(dados: FilmeCreate, db: Session = Depends(get_db)):
    return filme_service.criar_filme(db, dados)


@router.patch("/{id}", response_model=FilmeResponse, summary="Atualiza dados de um filme")
def patch_filme(id: int, dados: FilmeUpdate, db: Session = Depends(get_db)):
    filme = filme_service.atualizar_filme(db, id, dados)
    if not filme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filme com id {id} não encontrado.",
        )
    return filme


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove um filme")
def delete_filme(id: int, db: Session = Depends(get_db)):
    removido = filme_service.deletar_filme(db, id)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filme com id {id} não encontrado.",
        )
