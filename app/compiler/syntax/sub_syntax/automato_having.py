from app.compiler.syntax.sub_syntax.automato_valor import AutomatoValor

class AutomatoHaving:
    def __init__(self, parser_context):
        self.ctx = parser_context

    def analisar(self):
        # q0 -> q1 -> q2
        self.ctx.consumir('KEYWORD', 'having')
        self.ctx.consumir('PONTUACAO', '=')
        
        # A primeira condição não tem operador lógico anterior
        self.fluxo_q2(logico_anterior=None, tem_parenteses=False)

    def fluxo_q2(self, logico_anterior, tem_parenteses):
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
        token_alvo = self.ctx.token_atual
        alvo_dict = {}
        
        if token_alvo.tipo == 'IDENTIFICADOR':
            # É uma coluna! (q10 -> q11 -> q12 -> q13)
            alias_dir = self.ctx.consumir('IDENTIFICADOR').valor
            self.ctx.consumir('PONTUACAO', '.')
            col_dir = self.ctx.consumir('IDENTIFICADOR').valor
            
            # Validação Semântica do Alias não pode faltar aqui!
            self.ctx.ts.validar_alias_existente(alias_dir)
            
            alvo_dict = {'tipo': 'coluna', 'alias': alias_dir, 'coluna': col_dir}
            
        elif token_alvo.tipo in ['NUMERO', 'STRING']:
            # É um valor estático! (q10 -> q13)
            # Delega para o AutomatoValor processar (ex: 10,5 vira 10.5)
            valor_estatico = AutomatoValor(self.ctx).analisar()
            
            alvo_dict = {'tipo': 'valor', 'valor': valor_estatico}
            
        else:
            raise Exception(f"Erro no Having: O alvo deve ser 'alias.coluna', 'numero' ou 'string'. Obtido: {token_alvo.valor}")
        
        if tem_parenteses:
            self.ctx.consumir('PONTUACAO', ')')

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
                self.ctx.consumir('PONTUACAO', '(')
                
                # Recursão repassando o operador lógico
                self.fluxo_q2(logico_anterior=logico, tem_parenteses=True)
            else:
                raise Exception(f"Esperado 'and' ou 'or' no Having. Obtido: {token_logico.valor}")
        else:
            raise Exception(f"Erro no Having: Esperado ',' ou '&', obteve '{token.valor}'")