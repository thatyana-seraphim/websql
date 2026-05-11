from lexico.lexicoAutomato import Scanner
from sintatico.parser_principal import ParserPrincipal
from gerador.tradutorAutomato import TradutorSQL

entrada = "/Produtos:p?expand=ProdutosFornecedores:pf,on(p.prod_id.eq.' tag')&expand=Fornecedor:f,on(pf.fornecedor_id.eq.f.fornecedor_id)" + "&select=p.nome,f.nome" + "&where=p.preco.lt.1,and(p.estoque.lt.10)" + "&groupby=f.user"
# entrada = "/Aluno:a?select=a.cidade,avg.a.idade,avg.a.renda&groupby=a.cidade&having=avg.a.idade.gt.18,and(avg.a.renda.lte.1,500)"
# entrada = "/Aluno:a,Curso:c?select=a.nome,c.sigla&where=a.idade.eq.125,and(c.sigla.eq.a.sigla_curso)&orderby=a.nome.asc"
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

print("🚀3. SQL FINAL GERADO:")
print(f"\n{sql_final}")