-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS discord_auditoria;
USE discord_auditoria;

-- Tabela de usuários (armazenar ID e nome únicos)
CREATE TABLE IF NOT EXISTS usuarios (
    id BIGINT PRIMARY KEY,
    nome VARCHAR(100)
);

-- Tabela de logs
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id BIGINT,
    tipo VARCHAR(50),
    data_hora DATETIME NOT NULL,
    mensagem TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);