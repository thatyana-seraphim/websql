# app/services/answer_key.py

ANSWER_KEY_SQL = {
    1: "SELECT a.nome AS a_nome, a.telefone AS a_telefone\nFROM aluno a\nWHERE a.cidade = 'São Carlos - SP';",
    2: "SELECT p.nome AS p_nome, p.areapesquisa AS p_areapesquisa\nFROM professor p\nORDER BY p.nome DESC;",
    3: "SELECT a.nome AS a_nome, c.nome AS c_nome\nFROM aluno a\nINNER JOIN curso c ON (a.id_curso = c.id);",
    4: "SELECT a.nome AS a_nome, a.cidade AS a_cidade\nFROM aluno a\nINNER JOIN curso c ON (a.id_curso = c.id)\nWHERE c.nome = 'Ciência da Computação';",
    5: "SELECT c.nome AS c_nome, COUNT(a.id) AS count_a_id\nFROM curso c\nINNER JOIN aluno a ON (a.id_curso = c.id)\nGROUP BY c.nome;"
}

def validate_exercise(exercise_num: int, generated_sql: str) -> bool:
    expected = ANSWER_KEY_SQL.get(exercise_num)
    if not expected:
        return False
        
    return generated_sql.strip().replace('\n', ' ') == expected.strip().replace('\n', ' ')

def exercise_exists(exercise_num: int) -> bool:
    """Verifies if the exercise number is registered in the answer key."""
    return exercise_num in ANSWER_KEY_SQL