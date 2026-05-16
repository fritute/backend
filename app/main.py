import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, Base
from app.routers import filmes, categorias, atores

# Cria as tabelas no banco caso ainda não existam
Base.metadata.create_all(bind=engine)

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(
    title="API de Filmes",
    description="CRUD de filmes com FastAPI e MySQL",
    version="1.0.0",
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
    openapi_url="/openapi.json" if DEBUG else None,
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(filmes.router)
app.include_router(categorias.router)
app.include_router(atores.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "API de Filmes rodando!"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8080, reload=True)
