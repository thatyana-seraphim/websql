class AutomatoGroupby:
    def __init__(self, parser_context):
        self.ctx = parser_context

    def analisar(self):
        # q0 -> q1 -> q2
        self.ctx.consumir('KEYWORD', 'groupby')
        self.ctx.consumir('PONTUACAO', '=')
        
        # Inicia a leitura da coluna (q2)
        self.fluxo_q2()

    def fluxo_q2(self):
        # q2 -> q3 [label="alias"]
        alias = self.ctx.consumir('IDENTIFICADOR').valor
        
        # q3 -> q4 [label="."]
        self.ctx.consumir('PONTUACAO', '.')
        
        # q4 -> q5 [label="coluna"]
        coluna = self.ctx.consumir('IDENTIFICADOR').valor
        
        # Validação semântica e salvamento na memória
        self.ctx.ts.adicionar_groupby(alias, coluna)
        
        # Vai para o estado final
        self.fluxo_q5()

    def fluxo_q5(self):
        # Estado de aceitação q5 (peripheries=2)
        # Como o diagrama não possui transição de loop (ex: vírgula),
        # nós simplesmente encerramos e devolvemos o controle ao ParserPrincipal.
        return