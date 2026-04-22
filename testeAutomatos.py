from lexico.lexicoAutomato import Scanner
from sintatico.sintaticoAutomato import ParserPrincipal
from gerador.tradutorAutomato import TradutorSQL

entrada = "URLTableusuarios"

print(f"URL: {entrada}\n")

# 1. Léxico
scanner = Scanner()
tokens = scanner.tokenizar(entrada)
print("1. TOKENS GERADOS:")
print(tokens, "\n")

# 2 e 3. Sintático e Semântico (Tabela de Símbolos)
parser = ParserPrincipal(tokens)
tabela_simbolos = parser.analisar()
print("2. TABELA DE SÍMBOLOS PREENCHIDA:")
print(tabela_simbolos, "\n")

# 4. Gerador
tradutor = TradutorSQL(tabela_simbolos)
sql_final = tradutor.gerar()

print("3. SQL FINAL GERADO:")
print(f"🚀 {sql_final}")