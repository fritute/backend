from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.filme import Filme, Categoria, Ator
from app.schemas.filme import FilmeCreate, FilmeUpdate, CategoriaCreate, CategoriaUpdate, AtorCreate


# ─────────────────────────────────────────
# FILMES
# ─────────────────────────────────────────

def listar_filmes(db: Session) -> List[Filme]:
    return db.query(Filme).all()


def buscar_filme_por_id(db: Session, filme_id: int) -> Optional[Filme]:
    return db.query(Filme).filter(Filme.id == filme_id).first()


def criar_filme(db: Session, dados: FilmeCreate) -> Filme:
    filme = Filme(**dados.model_dump())
    db.add(filme)
    db.commit()
    db.refresh(filme)
    return filme


def atualizar_filme(db: Session, filme_id: int, dados: FilmeUpdate) -> Optional[Filme]:
    filme = buscar_filme_por_id(db, filme_id)
    if not filme:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(filme, campo, valor)
    db.commit()
    db.refresh(filme)
    return filme


def deletar_filme(db: Session, filme_id: int) -> bool:
    filme = buscar_filme_por_id(db, filme_id)
    if not filme:
        return False
    db.delete(filme)
    db.commit()
    return True


# ─────────────────────────────────────────
# CATEGORIAS
# ─────────────────────────────────────────

def listar_categorias(db: Session) -> List[Categoria]:
    return db.query(Categoria).all()


def criar_categoria(db: Session, dados: CategoriaCreate) -> Categoria:
    categoria = Categoria(**dados.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def buscar_categoria_por_id(db: Session, categoria_id: int) -> Optional[Categoria]:
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()


def atualizar_categoria(db: Session, categoria_id: int, dados: CategoriaUpdate) -> Optional[Categoria]:
    categoria = buscar_categoria_por_id(db, categoria_id)
    if not categoria:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria


def deletar_categoria(db: Session, categoria_id: int) -> bool:
    categoria = buscar_categoria_por_id(db, categoria_id)
    if not categoria:
        return False
    db.delete(categoria)
    db.commit()
    return True


# ─────────────────────────────────────────
# ATORES
# ─────────────────────────────────────────

def listar_atores_do_filme(db: Session, filme_id: int) -> List[Ator]:
    return db.query(Ator).filter(Ator.filme_id == filme_id).all()


def criar_ator(db: Session, dados: AtorCreate) -> Ator:
    ator = Ator(**dados.model_dump())
    db.add(ator)
    db.commit()
    db.refresh(ator)
    return ator
