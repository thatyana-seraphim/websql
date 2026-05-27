from app.compiler.lexical.lexicoAutomato import Scanner
from app.compiler.syntax.parser_principal import ParserPrincipal
from app.compiler.generator.tradutorAutomato import TradutorSQL

class CompilerService:
    @staticmethod
    def compile_url_to_sql(raw_input: str) -> dict:
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

        # Returns the processed data
        return {
            "sql": generated_sql,
            "recognized_tables": [t['nome'] for t in symbol_table.tabelas_principais]
        }