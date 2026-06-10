-- ==========================================
-- INSERÇÃO DE DADOS (SEED)
-- ==========================================

INSERT INTO CURSO (id, Nome, TotalCreditos) VALUES (2142, 'Engenharia Civil', 1500);
INSERT INTO CURSO (id, Nome, TotalCreditos) VALUES (2143, 'Ciência da Computação', 2000);
INSERT INTO CURSO (id, Nome, TotalCreditos) VALUES (2144, 'Direito', 1750);
INSERT INTO CURSO (id, Nome, TotalCreditos) VALUES (2145, 'Pedagogia', 1500);
INSERT INTO CURSO (id, Nome, TotalCreditos) VALUES (2146, 'Odontologia', 1600);

INSERT INTO PROFESSOR (id, Nome, Admissao, AreaPesquisa) VALUES (45675, 'Abgair Simon Ferreira', '1992-04-10', 'Banco de Dados'); 
INSERT INTO PROFESSOR (id, Nome, Admissao, AreaPesquisa) VALUES (45690, 'Ramon Travanti', '1993-05-20', 'Direito Romano'); 
INSERT INTO PROFESSOR (id, Nome, Admissao, AreaPesquisa) VALUES (45691, 'Gustavo Golveia Netto', '1993-04-05', 'Sociologia'); 
INSERT INTO PROFESSOR (id, Nome, Admissao, AreaPesquisa) VALUES (45692, 'Marcos Salvador', '1993-03-31', 'Matemática Financeira'); 
INSERT INTO PROFESSOR (id, Nome, Admissao, AreaPesquisa) VALUES (45693, 'Cintia Falcão', '1993-02-15', 'Engenharia de Software'); 

INSERT INTO ALUNO (id, Nome, Endereco, Cidade, Telefone, id_curso) VALUES (111, 'Edvaldo Carlos Silva', 'Av.São Carlos, 186', 'São Carlos - SP', '(017) 276-9999', 2143);
INSERT INTO ALUNO (id, Nome, Endereco, Cidade, Telefone, id_curso) VALUES (112, 'João Benedito Scapin', 'R.José Bonifácio, 70', 'São Carlos - SP', '(017) 273-8974', 2142);
INSERT INTO ALUNO (id, Nome, Endereco, Cidade, Telefone, id_curso) VALUES (113, 'Carol Antonia Silveira', 'R.Luiz Camões, 120', 'Ibaté - SP', '(017) 278-8568', 2145);
INSERT INTO ALUNO (id, Nome, Endereco, Cidade, Telefone, id_curso) VALUES (114, 'Marcos João Casanova', 'Av. São Carlos, 176', 'São Carlos - SP', '(017) 274-9874', 2143);
INSERT INTO ALUNO (id, Nome, Endereco, Cidade, Telefone, id_curso) VALUES (115, 'Simone Cristina Lima', 'R.Raul Junior, 180', 'São Carlos - SP', '(017) 273-9865', 2144);
INSERT INTO ALUNO (id, Nome, Endereco, Cidade, Telefone, id_curso) VALUES (116, 'Aílton Castro', 'R.Antonio Carlos, 120', 'Ibaté - SP', '(017) 278-8568', 2142);
INSERT INTO ALUNO (id, Nome, Endereco, Cidade, Telefone, id_curso) VALUES (117, 'José Paulo Figueira', 'R. XV Novembro, 871', 'São Carlos - SP', '(017) 274-9874', 2145);

INSERT INTO DISCIPLINA (id, Nome, QuantCreditos) VALUES (1, 'Banco de Dados', 30);
INSERT INTO DISCIPLINA (id, Nome, QuantCreditos) VALUES (2, 'Estrutura de Dados', 30);
INSERT INTO DISCIPLINA (id, Nome, QuantCreditos) VALUES (3, 'Direito Penal', 25);
INSERT INTO DISCIPLINA (id, Nome, QuantCreditos) VALUES (4, 'Cálculo Numérico', 30);
INSERT INTO DISCIPLINA (id, Nome, QuantCreditos) VALUES (5, 'Psicologia Infantil', 25);
INSERT INTO DISCIPLINA (id, Nome, QuantCreditos) VALUES (6, 'Direito Tributário', 33);
INSERT INTO DISCIPLINA (id, Nome, QuantCreditos) VALUES (7, 'Engenharia Software', 27);

INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (111, 1, 45675, '01/1998', 8.5);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (111, 2, 45675, '01/1998', 6.0);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (111, 2, 45675, '02/1998', 7.0);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (115, 3, 45690, '01/1998', 4.5);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (115, 3, 45690, '02/1998', 7.5);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (111, 4, 45692, '01/1998', 8.0);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (112, 4, 45692, '01/1998', 7.0);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (113, 5, 45691, '01/1998', 7.5);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (115, 6, 45690, '01/1998', 9.0);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (111, 7, 45693, '01/1998', 10.0);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (112, 7, 45693, '01/1998', 5.5);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (112, 7, 45693, '02/1998', 10.0);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (114, 1, 45675, '01/1998', 7.0);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (114, 2, 45675, '01/1998', 8.0);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (114, 4, 45692, '01/1998', 6.5);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (114, 4, 45692, '02/1998', 8.5);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (116, 4, 45692, '01/1998', 3.5);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (116, 4, 45692, '02/1998', 9.5);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (114, 7, 45693, '01/1998', 9.5);
INSERT INTO AULA (id_aluno, id_disp, id_prof, Semestre, Nota) VALUES (116, 7, 45693, '01/1998', 8.5);

INSERT INTO DISCIPLINACURSO (id_disp, id_curso) VALUES (1, 2143);
INSERT INTO DISCIPLINACURSO (id_disp, id_curso) VALUES (2, 2143);
INSERT INTO DISCIPLINACURSO (id_disp, id_curso) VALUES (3, 2144);
INSERT INTO DISCIPLINACURSO (id_disp, id_curso) VALUES (4, 2143);
INSERT INTO DISCIPLINACURSO (id_disp, id_curso) VALUES (4, 2142);
INSERT INTO DISCIPLINACURSO (id_disp, id_curso) VALUES (5, 2145);
INSERT INTO DISCIPLINACURSO (id_disp, id_curso) VALUES (6, 2144);
INSERT INTO DISCIPLINACURSO (id_disp, id_curso) VALUES (7, 2143);
INSERT INTO DISCIPLINACURSO (id_disp, id_curso) VALUES (7, 2142);