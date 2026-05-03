class AutomatoFuncao:
    def __init__(self, parser_context):
        self.ctx = parser_context

    def analisar(self):
        # q0 -> q1 [label="or/and"]
        token_logico = self.ctx.token_atual
        if token_logico.valor not in ['and', 'or']:
            raise Exception(f"Esperado operador lógico ('and'/'or'). Obtido: {token_logico.valor}")
        
        logico = self.ctx.consumir('KEYWORD').valor
        self.ctx.consumir('PONTUACAO', '(') # q1 -> q2
        
        # q2 -> q3 -> q4 -> q5 -> q6 -> q7 -> q8
        alias_esq = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.ts.validar_alias_existente(alias_esq) # Validação!
        
        self.ctx.consumir('PONTUACAO', '.')
        col_esq = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.consumir('PONTUACAO', '.')
        relacional = self.ctx.consumir('RELACIONAL').valor
        self.ctx.consumir('PONTUACAO', '.')
        
        # q8: Decisão entre ir para q11 (valor) ou q9 (alias)
        alvo = self.ctx.consumir().valor # Pode ser numero ou string
        
        condicao = {
            'logico': logico,
            'esq_alias': alias_esq,
            'esq_col': col_esq,
            'relacional': relacional
        }

        if self.ctx.token_atual and self.ctx.token_atual.valor == '.':
            # q8 -> q9 -> q10 -> q11 (É um Alias.Coluna)
            self.ctx.consumir('PONTUACAO', '.')
            col_dir = self.ctx.consumir('IDENTIFICADOR').valor
            self.ctx.ts.validar_alias_existente(alvo) # alvo era o alias
            
            condicao['dir_tipo'] = 'coluna'
            condicao['dir_alias'] = alvo
            condicao['dir_col'] = col_dir
        else:
            # q8 -> q11 (É um valor estático)
            condicao['dir_tipo'] = 'valor'
            condicao['dir_val'] = alvo

        # q11 -> q12 [label=")"]
        self.ctx.consumir('PONTUACAO', ')')
        return condicao # Retorna o dicionário para o Join!