create database filmes_brasil;
USE filmes_brasil;

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

-- =========================
-- TABELA DE FILMES
-- =========================
CREATE TABLE filmes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    diretor VARCHAR(100),
    ano_lancamento INT,
    nota DECIMAL(3,1),
    categoria_id INT,

    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- =========================
-- TABELA DE ATORES
-- =========================
CREATE TABLE atores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    nacionalidade VARCHAR(50),
    idade INT,
    filme_id INT,

    FOREIGN KEY (filme_id) REFERENCES filmes(id)
);

