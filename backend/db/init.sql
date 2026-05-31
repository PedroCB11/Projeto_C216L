DROP TABLE IF EXISTS professores;

CREATE TABLE professores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    sala_de_atendimento VARCHAR(50) NOT NULL
);

INSERT INTO professores (nome, email, sala_de_atendimento) VALUES 
('Aluno 1', 'aluno_1@example.com', 'Curso 1'),
('Aluno 2', 'aluno_2@example.com', 'Curso 2');
