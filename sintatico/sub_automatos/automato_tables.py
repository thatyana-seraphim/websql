class AutomatoTables:
    def __init__(self, parser_context):
        # Recebe o ParserPrincipal para ter acesso à lista de tokens e à Tabela de Símbolos
        self.ctx = parser_context
        self.tabela_temporaria = None

    def analisar(self):
        # start -> q0 [label="/"]
        self.ctx.consumir('PONTUACAO', '/')
        self.fluxo_q0()

    def fluxo_q0(self):
        # q0 -> q1 [label="'table_name'"]
        token_tabela = self.ctx.consumir('IDENTIFICADOR')
        self.tabela_temporaria = token_tabela.valor
        self.fluxo_q1()

    def fluxo_q1(self):
        # q1 -> q2 [label=":"]
        self.ctx.consumir('PONTUACAO', ':')
        self.fluxo_q2()

    def fluxo_q2(self):
        # q2 -> q3 [label="'alias'"]
        token_alias = self.ctx.consumir('IDENTIFICADOR')
        
        # Salva na nossa Tabela de Símbolos!
        self.ctx.ts.adicionar_tabela(self.tabela_temporaria, token_alias.valor)
        self.fluxo_q3()

    def fluxo_q3(self):
        token_atual = self.ctx.token_atual
        
        if token_atual.valor == ',':
            # q3 -> q0 [label="','"] (Loop para mais tabelas)
            self.ctx.consumir('PONTUACAO', ',')
            self.fluxo_q0()
            
        elif token_atual.valor == '?':
            # q3 -> q4 [label="'?'"] (Estado Final do Sub-automato)
            self.ctx.consumir('PONTUACAO', '?')
            # O estado q4 encerra o sub-autômato e devolve o controle ao ParserPrincipal
            print("✅ Sub-autômato 'Tables' concluído com sucesso!")
            return
        else:
            raise Exception(f"Erro em q3: Esperado ',' ou '?', obtido '{token_atual.valor}'")