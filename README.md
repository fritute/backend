# API de Filmes

API REST desenvolvida com **FastAPI** e **MySQL** para gerenciamento de filmes, categorias e atores.

---

## Tecnologias

- **Python 3.12**
- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **PyMySQL** — driver MySQL
- **MySQL 8.0** — banco de dados
- **Docker / Docker Compose** — containerização

---

## Configuração do ambiente

Copie o arquivo de exemplo de variáveis de ambiente:

```bash
cp .env.example .env
```

O `.env` vem pré-configurado com `localhost` para uso **sem Docker**. Ao rodar **com Docker**, a variável é sobrescrita automaticamente pelo `docker-compose.yml`, sem necessidade de edição manual.

---

## Como executar

### Sem Docker

**Pré-requisitos:** Python 3.12+ e MySQL 8.0+ rodando localmente.

#### 1. Configurar o banco de dados local

O script de criação do banco está em `app/database/script.sql`. Execute-o no seu MySQL:

```bash
mysql -u root -p < app/database/script.sql
```

Ou abra o arquivo `app/database/script.sql` diretamente no seu cliente MySQL (MySQL Workbench, DBeaver, etc.) e execute.

O script cria o banco `filmes_brasil` e todas as tabelas necessárias.

#### 2. Configurar a conexão

No arquivo `.env`, verifique se a `DATABASE_URL` aponta para o seu MySQL local com as credenciais corretas:

```env
DATABASE_URL=mysql+pymysql://root:SUA_SENHA@localhost:3306/filmes_brasil
```

#### 3. Subir a aplicação

```bash
# Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

# Instalar dependências
pip install -r requirements.txt

# Iniciar a aplicação
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

---

### Com Docker

**Pré-requisito:** Docker Desktop ou Rancher Desktop em execução.

```bash
# Subir todos os containers (API + banco de dados)
docker-compose up --build -d
```

O comando acima irá:
- Criar o banco MySQL 8.0 no container `filmes_db`
- Buildar e iniciar a API no container `filmes_api`
- Aguardar o banco ficar saudável antes de iniciar a API

A API estará disponível em: `http://localhost:8000`

> **Rancher Desktop:** use `http://127.0.0.1:8000` caso `localhost` não responda.

```bash
# Parar os containers
docker-compose down

# Parar e remover os dados do banco
docker-compose down -v
```

> Os dados são persistidos no volume Docker `mysql_data` enquanto ele existir.

---

## Documentação interativa

A documentação só fica disponível quando `DEBUG=true` está definido no `.env`:

| Interface | URL |
|-----------|-----|
| Swagger UI | http://localhost:8000/docs |
| Redoc | http://localhost:8000/redoc |

> Em produção, mantenha `DEBUG=false` para ocultar a documentação e o schema OpenAPI.

---

## Segurança

### Variáveis de ambiente

O arquivo `.env` **nunca deve ser commitado no Git**. Ele já está listado no `.gitignore`.

Para configurar o projeto após clonar:

```bash
cp .env.example .env
# Edite o .env com suas credenciais reais
```

As variáveis disponíveis são:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `DATABASE_URL` | URL de conexão com o banco | `mysql+pymysql://root:SENHA@localhost:3306/filmes_brasil` |
| `DEBUG` | Habilita `/docs` e `/redoc` | `true` / `false` |
| `ALLOWED_ORIGINS` | Origens permitidas pelo CORS | `http://localhost:3000,http://meusite.com` |

### CORS

A API aceita requisições apenas das origens definidas em `ALLOWED_ORIGINS`. Para desenvolvimento local, o valor padrão é `http://localhost:3000`. Para múltiplas origens, separe por vírgula:

```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Imagem Docker

O `.dockerignore` impede que arquivos sensíveis (`.env`, `venv/`, `.git/`) sejam copiados para dentro da imagem Docker.

---

## Ordem recomendada para cadastro

Como há relacionamentos entre as entidades, respeite a seguinte ordem:

```
1. Criar Categoria  →  POST /categorias/
2. Criar Filme      →  POST /filmes/        (usa categoria_id)
3. Criar Ator       →  POST /atores/        (usa filme_id)
```


## Endpoints

### Filmes — `/filmes`

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/filmes/` | Lista todos os filmes |
| `GET` | `/filmes/{id}` | Retorna um filme pelo ID |
| `POST` | `/filmes/` | Cadastra um novo filme |
| `PATCH` | `/filmes/{id}` | Atualiza parcialmente um filme |
| `DELETE` | `/filmes/{id}` | Remove um filme |

**Corpo — POST / PATCH:**
```json
{
  "titulo": "Cidade de Deus",
  "diretor": "Fernando Meirelles",
  "ano_lancamento": 2002,
  "nota": 9.5,
  "categoria_id": 1
}
```

**Resposta — 200 / 201:**
```json
{
  "id": 1,
  "titulo": "Cidade de Deus",
  "diretor": "Fernando Meirelles",
  "ano_lancamento": 2002,
  "nota": 9.5,
  "categoria_id": 1,
  "categoria": { "id": 1, "nome": "Drama" },
  "atores": []
}
```

---

### Categorias — `/categorias`

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/categorias/` | Lista todas as categorias |
| `GET` | `/categorias/{id}` | Retorna uma categoria pelo ID |
| `POST` | `/categorias/` | Cadastra uma nova categoria |
| `PATCH` | `/categorias/{id}` | Atualiza uma categoria |
| `DELETE` | `/categorias/{id}` | Remove uma categoria |

**Corpo — POST / PATCH:**
```json
{
  "nome": "Drama"
}
```

**Resposta — 200 / 201:**
```json
{
  "id": 1,
  "nome": "Drama"
}
```

---

### Atores — `/atores`

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/atores/` | Lista todos os atores |
| `GET` | `/atores/{id}` | Retorna um ator pelo ID |
| `POST` | `/atores/` | Cadastra um novo ator |
| `PATCH` | `/atores/{id}` | Atualiza um ator |
| `DELETE` | `/atores/{id}` | Remove um ator |

**Corpo — POST / PATCH:**
```json
{
  "nome": "Alexandre Rodrigues",
  "nacionalidade": "Brasileira",
  "idade": 40,
  "filme_id": 1
}
```

**Resposta — 200 / 201:**
```json
{
  "id": 1,
  "nome": "Alexandre Rodrigues",
  "nacionalidade": "Brasileira",
  "idade": 40,
  "filme_id": 1
}
```

---

## Códigos de resposta

| Código | Significado |
|--------|-------------|
| `200 OK` | Requisição bem-sucedida |
| `201 Created` | Recurso criado com sucesso |
| `204 No Content` | Recurso removido com sucesso |
| `400 Bad Request` | Dados inválidos (ex: `filme_id` inexistente ao criar ator) |
| `404 Not Found` | Recurso não encontrado |
| `422 Unprocessable Entity` | Erro de validação nos campos enviados |
| `500 Internal Server Error` | Erro interno do servidor |

---


