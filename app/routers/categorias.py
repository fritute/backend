from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.filme import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.services import filme_service

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/", response_model=List[CategoriaResponse], summary="Lista todas as categorias")
def get_categorias(db: Session = Depends(get_db)):
    return filme_service.listar_categorias(db)


@router.get("/{id}", response_model=CategoriaResponse, summary="Retorna uma categoria pelo ID")
def get_categoria(id: int, db: Session = Depends(get_db)):
    categoria = filme_service.buscar_categoria_por_id(db, id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com id {id} não encontrada.",
        )
    return categoria


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED, summary="Cadastra uma nova categoria")
def post_categoria(dados: CategoriaCreate, db: Session = Depends(get_db)):
    return filme_service.criar_categoria(db, dados)


@router.patch("/{id}", response_model=CategoriaResponse, summary="Atualiza uma categoria")
def patch_categoria(id: int, dados: CategoriaUpdate, db: Session = Depends(get_db)):
    categoria = filme_service.atualizar_categoria(db, id, dados)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com id {id} não encontrada.",
        )
    return categoria


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove uma categoria")
def delete_categoria(id: int, db: Session = Depends(get_db)):
    removido = filme_service.deletar_categoria(db, id)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com id {id} não encontrada.",
        )
