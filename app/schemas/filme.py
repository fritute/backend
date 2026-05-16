from __future__ import annotations
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field


# ─────────────────────────────────────────
# CATEGORIA
# ─────────────────────────────────────────

class CategoriaBase(BaseModel):
    nome: str = Field(..., max_length=50, examples=["Ação"])


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=50)


class CategoriaResponse(CategoriaBase):
    id: int

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────
# ATOR
# ─────────────────────────────────────────

class AtorBase(BaseModel):
    nome: str = Field(..., max_length=100, examples=["Fernanda Montenegro"])
    nacionalidade: Optional[str] = Field(None, max_length=50, examples=["Brasileira"])
    idade: Optional[int] = Field(None, ge=0, examples=[75])


class AtorCreate(AtorBase):
    filme_id: Optional[int] = None


class AtorUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=100)
    nacionalidade: Optional[str] = Field(None, max_length=50)
    idade: Optional[int] = Field(None, ge=0)
    filme_id: Optional[int] = None


class AtorResponse(AtorBase):
    id: int
    filme_id: Optional[int] = None

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────
# FILME
# ─────────────────────────────────────────

class FilmeBase(BaseModel):
    titulo: str = Field(..., max_length=100, examples=["Central do Brasil"])
    diretor: Optional[str] = Field(None, max_length=100, examples=["Walter Salles"])
    ano_lancamento: Optional[int] = Field(None, ge=1888, examples=[1998])
    nota: Optional[Decimal] = Field(None, ge=0, le=10, examples=[9.2])
    categoria_id: Optional[int] = None


class FilmeCreate(FilmeBase):
    pass


class FilmeUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=100)
    diretor: Optional[str] = Field(None, max_length=100)
    ano_lancamento: Optional[int] = Field(None, ge=1888)
    nota: Optional[Decimal] = Field(None, ge=0, le=10)
    categoria_id: Optional[int] = None


class FilmeResponse(FilmeBase):
    id: int
    categoria: Optional[CategoriaResponse] = None
    atores: List[AtorResponse] = []

    model_config = {"from_attributes": True}
