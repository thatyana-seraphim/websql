class AutomatoHaving:
    def __init__(self, parser_context):
        self.ctx = parser_context

    def analisar(self):
        # q0 -> q1 -> q2
        self.ctx.consumir('KEYWORD', 'having')
        self.ctx.consumir('PONTUACAO', '=')
        
        # A primeira condição não tem operador lógico anterior
        self.fluxo_q2(logico_anterior=None)

    def fluxo_q2(self, logico_anterior):
        # q2 -> q3 -> q4 -> q5 -> q6 -> q7 -> q8 -> q9 -> q10
        agregacao = self.ctx.consumir('AGREGACAO').valor
        self.ctx.consumir('PONTUACAO', '.')
        alias_esq = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.consumir('PONTUACAO', '.')
        col_esq = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.consumir('PONTUACAO', '.')
        relacional = self.ctx.consumir('RELACIONAL').valor
        self.ctx.consumir('PONTUACAO', '.')

        # q10: Leitura do alvo
        alvo = self.ctx.consumir().valor

        # Bifurcação q10 -> q13 (valor) OU q10 -> q11 -> q12 -> q13 (coluna)
        alvo_dict = {}
        if self.ctx.token_atual and self.ctx.token_atual.valor == '.':
            self.ctx.consumir('PONTUACAO', '.')
            col_dir = self.ctx.consumir('IDENTIFICADOR').valor
            alvo_dict = {'tipo': 'coluna', 'alias': alvo, 'coluna': col_dir}
        else:
            alvo_dict = {'tipo': 'valor', 'valor': alvo}

        # Salva a condição validada na Tabela de Símbolos
        self.ctx.ts.adicionar_having(agregacao, alias_esq, col_esq, relacional, alvo_dict, logico_anterior)

        # Segue para o estado de aceitação/loop
        self.fluxo_q13()

    def fluxo_q13(self):
        token = self.ctx.token_atual
        
        # Se não houver mais tokens ou houver o '&', o autômato encerra
        if not token or token.valor == '&':
            return
            
        # q13 -> q14 [label=","]
        elif token.valor == ',':
            self.ctx.consumir('PONTUACAO', ',')
            
            token_logico = self.ctx.token_atual
            if token_logico and token_logico.valor in ['and', 'or']:
                # q14 -> q2 [label="and / or"]
                logico = self.ctx.consumir('KEYWORD').valor
                self.ctx.consumir('PONTUACAO', '.')
                
                # Recursão repassando o operador lógico
                self.fluxo_q2(logico_anterior=logico)
            else:
                raise Exception(f"Esperado 'and' ou 'or' no Having. Obtido: {token_logico.valor}")
        else:
            raise Exception(f"Erro no Having: Esperado ',' ou '&', obteve '{token.valor}'")