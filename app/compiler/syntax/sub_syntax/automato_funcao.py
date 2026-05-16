from app.compiler.syntax.sub_syntax.automato_valor import AutomatoValor

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
        condicao = {
            'logico': logico,
            'esq_alias': alias_esq,
            'esq_col': col_esq,
            'relacional': relacional
        }

        # Bifurcação a partir de q8 baseada no TIPO do token
        token_alvo = self.ctx.token_atual
        
        if token_alvo.tipo == 'IDENTIFICADOR':
            # q8 -> q9 -> q10 -> q11 (É um Alias.Coluna)
            alias_dir = self.ctx.consumir('IDENTIFICADOR').valor
            self.ctx.consumir('PONTUACAO', '.')
            col_dir = self.ctx.consumir('IDENTIFICADOR').valor
            
            # Validação Semântica do Alias da direita
            self.ctx.ts.validar_alias_existente(alias_dir)
            
            condicao['dir_tipo'] = 'coluna'
            condicao['dir_alias'] = alias_dir
            condicao['dir_col'] = col_dir
            
        elif token_alvo.tipo in ['NUMERO', 'STRING']:
            # q8 -> q11 (É um valor estático)
            # Delega para o AutomatoValor processar e formatar (ex: '-10,5' ou 'ativo')
            valor_estatico = AutomatoValor(self.ctx).analisar()
            
            condicao['dir_tipo'] = 'valor'
            condicao['dir_val'] = valor_estatico
            
        else:
            raise Exception(f"Erro na Função Lógica: O alvo deve ser 'alias.coluna', 'numero' ou 'string'. Obtido: {token_alvo.valor}")

        # q11 -> q12 [label=")"]
        self.ctx.consumir('PONTUACAO', ')')
        
        return condicao # Retorna o dicionário para o Join!