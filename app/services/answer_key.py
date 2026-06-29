# app/services/answer_key.py

ANSWER_KEY_RESULTS = {
    1: [
        {"a_nome": "Edvaldo Carlos Silva", "a_telefone": "(017) 276-9999"},
        {"a_nome": "João Benedito Scapin", "a_telefone": "(017) 273-8974"},
        {"a_nome": "Marcos João Casanova", "a_telefone": "(017) 274-9874"},
        {"a_nome": "Simone Cristina Lima", "a_telefone": "(017) 273-9865"},
        {"a_nome": "José Paulo Figueira", "a_telefone": "(017) 274-9874"}
    ],
    2: [
        {"p_nome": "Ramon Travanti", "p_areapesquisa": "Direito Romano"},
        {"p_nome": "Marcos Salvador", "p_areapesquisa": "Matemática Financeira"},
        {"p_nome": "Gustavo Golveia Netto", "p_areapesquisa": "Sociologia"},
        {"p_nome": "Cintia Falcão", "p_areapesquisa": "Engenharia de Software"},
        {"p_nome": "Abgair Simon Ferreira", "p_areapesquisa": "Banco de Dados"}
    ],
    3: [
        {"a_nome": "Edvaldo Carlos Silva", "c_nome": "Ciência da Computação"},
        {"a_nome": "João Benedito Scapin", "c_nome": "Engenharia Civil"},
        {"a_nome": "Carol Antonia Silveira", "c_nome": "Pedagogia"},
        {"a_nome": "Marcos João Casanova", "c_nome": "Ciência da Computação"},
        {"a_nome": "Simone Cristina Lima", "c_nome": "Direito"},
        {"a_nome": "Aílton Castro", "c_nome": "Engenharia Civil"},
        {"a_nome": "José Paulo Figueira", "c_nome": "Pedagogia"}
    ],
    4: [
        {"a_nome": "Edvaldo Carlos Silva", "a_cidade": "São Carlos - SP"},
        {"a_nome": "Marcos João Casanova", "a_cidade": "São Carlos - SP"}
    ],
    5: [
        {"c_nome": "Ciência da Computação", "a_id": 2},
        {"c_nome": "Direito", "a_id": 1},
        {"c_nome": "Engenharia Civil", "a_id": 2},
        {"c_nome": "Pedagogia", "a_id": 2}
    ]
}

def validate_exercise(exercise_num: int, user_results: list) -> bool:
    """Verifies if the database output matches the expected JSON result."""
    expected = ANSWER_KEY_RESULTS.get(exercise_num)
    
    if expected is None:
        return False
        
    if len(user_results) != len(expected):
        return False

    if exercise_num == 2:
        return user_results == expected

    user_set = [tuple(sorted(d.items())) for d in user_results]
    expected_set = [tuple(sorted(d.items())) for d in expected]

    return sorted(user_set) == sorted(expected_set)

def exercise_exists(exercise_num: int) -> bool:
    """Verifies if the exercise number is registered in the answer key."""
    return exercise_num in ANSWER_KEY_RESULTS