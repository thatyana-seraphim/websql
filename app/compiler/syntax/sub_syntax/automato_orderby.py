class AutomatoOrderby:
    def __init__(self, parser_context):
        self.ctx = parser_context

    def analisar(self):
        # q0 -> q1 -> q2
        self.ctx.consumir('KEYWORD', 'orderby')
        self.ctx.consumir('PONTUACAO', '=')
        
        # q2 -> q3 -> q4 -> q5 -> q6
        alias = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.consumir('PONTUACAO', '.')
        coluna = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.consumir('PONTUACAO', '.')
        
        # q6 -> q7 (Valida asc ou desc)
        token_direcao = self.ctx.token_atual
        if token_direcao and token_direcao.valor in ['asc', 'desc']:
            direcao = self.ctx.consumir('KEYWORD').valor
        else:
            raise Exception(f"Erro Sintático: Esperado 'asc' ou 'desc' no OrderBy. Obtido: '{token_direcao.valor}'")
            
        # Validação semântica e gravação na memória
        self.ctx.ts.adicionar_orderby(alias, coluna, direcao)
        
        # q7 é estado de aceitação final. Retorna para o ParserPrincipal.
        return