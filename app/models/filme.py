from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)

    filmes = relationship("Filme", back_populates="categoria")


class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    diretor = Column(String(100))
    ano_lancamento = Column(Integer)
    nota = Column(DECIMAL(3, 1))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    categoria = relationship("Categoria", back_populates="filmes")
    atores = relationship("Ator", back_populates="filme")


class Ator(Base):
    __tablename__ = "atores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    nacionalidade = Column(String(50))
    idade = Column(Integer)
    filme_id = Column(Integer, ForeignKey("filmes.id"))

    filme = relationship("Filme", back_populates="atores")
