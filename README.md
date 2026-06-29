# WebSQL: Compilador de URL para SQL

## 1. Visão Geral do Projeto (O "O Quê")

### Apresentação
O **WebSQL** é um motor de compilação customizado integrado a uma API Web desenvolvida com FastAPI e SQLModel (SQLite). O objetivo principal da ferramenta é atuar como uma plataforma educacional e interpretador de uma DSL (*Domain Specific Language*) baseada em caminhos de URL. Ele traduz requisições HTTP em consultas estruturadas ANSI SQL de forma determinística, executando-as em um banco de dados relacional e auditando o progresso de aprendizado dos usuários.

Este projeto foi desenhado para expor conceitos arquiteturais através de uma interface simplificada, unindo a teoria de construção de compiladores com a prática de desenvolvimento de APIs modernas.

### Stack Tecnológico Principal
* **Python 3.12:** Linguagem base do motor de compilação léxica e sintática.
* **FastAPI:** Framework assíncrono para o roteamento e exposição da interface REST.
* **SQLModel / SQLAlchemy:** Mapeamento objeto-relacional (ORM) e execução segura das queries dinâmicas.
* **SQLite:** Banco de dados relacional embarcado para persistência de dados acadêmicos e auditoria de tentativas.

---

## 2. Fundamentação Teórica (O "Por Quê")

### Base Conceitual
A ferramenta baseia-se fortemente nos princípios da **Álgebra Relacional** e na sintaxe consolidada do **SQL** (*Structured Query Language*). Em vez de utilizar uma interface tradicional de banco de dados ou um ORM convencional exposto diretamente ao cliente, o WebSQL propõe uma sintaxe contínua e formatada encapsulada na própria requisição HTTP.

### Operações Suportadas
O motor do compilador valida, processa e traduz os seguintes conceitos fundamentais de bancos de dados relacionais:

* **Projeção (`select`):** Definição de colunas específicas e aplicação de funções de agregação (como `COUNT`, `SUM`, `AVG`), espelhando o comportamento lógico da instrução `SELECT`.
* **Origem (Path da Rota):** Identificação das tabelas principais e inferência de seus respectivos aliases lógicos a partir do caminho base da requisição (representando a cláusula `FROM`).
* **Junção (`expand`):** Resolução de relacionamentos estruturais entre múltiplas tabelas via expansão explícita de chaves estrangeiras, implementando a lógica matemática do `INNER JOIN`.
* **Seleção (`where`):** Aplicação de filtros condicionais horizontais sobre os registros utilizando operadores lógicos e relacionais customizados (como `eq` para `=`, `gt` para `>`, `like`, etc.), correspondendo à cláusula `WHERE`.
* **Agrupamento (`groupby` & `having`):** Operações avançadas baseadas em partições de dados e filtros aplicados diretamente sobre resultados agregados, emulando `GROUP BY` e `HAVING`.
* **Ordenação (`orderby`):** Controle da apresentação dos dados de forma ascendente (`asc`) ou descendente (`desc`), refletindo o comportamento do `ORDER BY`.

## 3. Arquitetura do Compilador (O "Como")

O WebSQL foi projetado seguindo a arquitetura clássica de um compilador de passagem única (*single-pass compiler*). O fluxo é dividido em quatro camadas com responsabilidades isoladas, garantindo que a URL seja validada e traduzida com segurança antes de interagir com o banco de dados.

### Pipeline de Processamento

Saída de código
File README-v2.md written successfully.

```text
    URL do Usuário 
         │
         ▼
 ┌───────────────┐
 │    Scanner    │  🔹 Análise Léxica: Tokeniza a URL bruta.
 └───────┬───────┘
         │ (Lista de Tokens)
         ▼
 ┌───────────────┐
 │    Parser     │  🔹 Análise Sintática/Semântica: Valida a gramática via 
 └───────┬───────┘     autômatos e constrói a Tabela de Símbolos.
         │ (Tabela de Símbolos)
         ▼
 ┌───────────────┐
 │   Tradutor    │  🔹 Geração de Código: Traduz os símbolos em ANSI SQL
 └───────┬───────┘     padronizado com aliases anti-colisão.
         │ (String SQL Gerada)
         ▼
 ┌───────────────┐
 │ Engine / Audit│  🔹 Execução e Auditoria: Executa a query, valida contra o
 └───────────────┘     gabarito de exercícios e retorna o JSON.