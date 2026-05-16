from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.filme import AtorCreate, AtorUpdate, AtorResponse
from app.services import filme_service

router = APIRouter(prefix="/atores", tags=["Atores"])


@router.get("/", response_model=List[AtorResponse], summary="Lista todos os atores")
def get_atores(db: Session = Depends(get_db)):
    return filme_service.listar_atores(db)


@router.get("/{id}", response_model=AtorResponse, summary="Retorna um ator pelo ID")
def get_ator(id: int, db: Session = Depends(get_db)):
    ator = filme_service.buscar_ator_por_id(db, id)
    if not ator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ator com id {id} não encontrado.",
        )
    return ator


@router.post("/", response_model=AtorResponse, status_code=status.HTTP_201_CREATED, summary="Cadastra um novo ator")
def post_ator(dados: AtorCreate, db: Session = Depends(get_db)):
    return filme_service.criar_ator(db, dados)


@router.patch("/{id}", response_model=AtorResponse, summary="Atualiza um ator")
def patch_ator(id: int, dados: AtorUpdate, db: Session = Depends(get_db)):
    ator = filme_service.atualizar_ator(db, id, dados)
    if not ator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ator com id {id} não encontrado.",
        )
    return ator


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove um ator")
def delete_ator(id: int, db: Session = Depends(get_db)):
    removido = filme_service.deletar_ator(db, id)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ator com id {id} não encontrado.",
        )
