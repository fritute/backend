import uvicorn
from fastapi import FastAPI
from app.database.database import engine, Base
from app.routers import filmes, categorias, atores

# Cria as tabelas no banco caso ainda não existam
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Filmes",
    description="CRUD de filmes com FastAPI e MySQL",
    version="1.0.0",
)

app.include_router(filmes.router)
app.include_router(categorias.router)
app.include_router(atores.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "API de Filmes rodando!"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8080, reload=True)
