from app.services.answer_key import validate_exercise, exercise_exists
from app.compiler.lexical.lexicoAutomato import Scanner
from app.compiler.syntax.parser_principal import ParserPrincipal
from app.compiler.generator.tradutorAutomato import TradutorSQL
from app.database.models import UsuarioTentativa
from sqlmodel import Session, text, select

class CompilerService:
    @staticmethod
    def compile_url_and_execute(
        raw_input: str,
        session: Session,
        user_name: str = None,
        user_email: str = None,
        exercise_num: int = None
    ) -> dict:
        
        if exercise_num is not None:
            if not exercise_exists(exercise_num):
                raise Exception(f"Exercise Error: O exercício número {exercise_num} não existe no sistema.")
            
        is_correct = False
        generated_sql = ""
        symbol_table = None
        compilation_error = None

        try:
            # 1. Lexical Analysis
            scanner = Scanner()
            tokens = scanner.tokenize(raw_input)
            
            if not tokens:
                raise Exception("Lexical Error: No valid tokens found in the URL.")

            # 2. Syntax and Semantic Analysis
            parser = ParserPrincipal(tokens)
            symbol_table = parser.analisar()

            # 3. Code Generation
            translator = TradutorSQL(symbol_table)
            generated_sql = translator.gerar()
                
            if exercise_num is not None:
                is_correct = validate_exercise(exercise_num, generated_sql)
        except Exception as e:
            compilation_error = e
            is_correct=False
  
        if user_email and exercise_num is not None:
            # Busca se já existe um registro para este email e exercício
            statement = select(UsuarioTentativa).where(
                UsuarioTentativa.email == user_email,
                UsuarioTentativa.num_exercicio == exercise_num
            )
            registro = session.exec(statement).first()

            if registro:
                # Se existe, soma +1
                if registro.acertos == 0:
                    registro.tentativas += 1
                    if is_correct: registro.acertos += 1
            else:
                # Se não existe, cria o primeiro registro
                registro = UsuarioTentativa(
                    nome=user_name or "Anônimo",
                    email=user_email,
                    num_exercicio=exercise_num,
                    tentativas=1,
                    acertos=1 if is_correct else 0
                )
            
            session.add(registro)
            session.commit() # Salva no banco!

        if compilation_error:
            raise compilation_error

        # 4. Execute SQL
        statement_sql = text(generated_sql)
        db_result = session.exec(statement_sql)
        formatted_results = [dict(row) for row in db_result.mappings().all()]

        # Returns the processed data
        return {
            "sql": generated_sql,
            "recognized_tables": [t['nome'] for t in symbol_table.tabelas_principais],
            "result": formatted_results,
            "is_correct": is_correct
        }