from sintatico.sub_automatos.automato_funcao import AutomatoFuncao
from sintatico.sub_automatos.automato_valor import AutomatoValor

class AutomatoJoin:
    def __init__(self, parser_context):
        self.ctx = parser_context

    def analisar(self):
        # q0 -> q1 -> q2 -> q3 -> q4 -> q5
        self.ctx.consumir('KEYWORD', 'expand')
        self.ctx.consumir('PONTUACAO', '=')
        tabela = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.consumir('PONTUACAO', ':')
        alias = self.ctx.consumir('IDENTIFICADOR').valor
        
        self.ctx.ts.registrar_nova_tabela(tabela, alias, is_join=True)
        
        # q5 -> q6 -> q7 -> q8 (NOVO: Ponto antes do ON)
        self.ctx.consumir('PONTUACAO', ',')
        self.ctx.consumir('KEYWORD', 'on')
        self.ctx.consumir('PONTUACAO', '(')
        
        # Leitura da Condição Principal (q8 a q17)
        cond_principal = self.ler_condicao_join()
        
        # Loop de q17 a q19
        condicoes_extras = []
        self.fluxo_q17(condicoes_extras)
        
        self.ctx.ts.adicionar_join(tabela, alias, cond_principal, condicoes_extras)

    def ler_condicao_join(self):
        # q8 -> q9 -> q10 -> q11 -> q12 -> q13 -> q14
        alias_esq = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.ts.validar_alias_existente(alias_esq)
        
        self.ctx.consumir('PONTUACAO', '.')
        col_esq = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.consumir('PONTUACAO', '.')
        relacional = self.ctx.consumir('RELACIONAL').valor
        self.ctx.consumir('PONTUACAO', '.')
        
        condicao = {
            'esq_alias': alias_esq, 
            'esq_col': col_esq, 
            'op': relacional
        }

        # Bifurcação a partir de q14 baseada no TIPO do token
        token_alvo = self.ctx.token_atual
        
        if token_alvo.tipo == 'IDENTIFICADOR':
            # q14 -> q15 -> q16 -> q17 (É Alias.Coluna)
            alias_dir = self.ctx.consumir('IDENTIFICADOR').valor
            self.ctx.consumir('PONTUACAO', '.')
            col_dir = self.ctx.consumir('IDENTIFICADOR').valor
            
            # Validação Semântica do Alias
            self.ctx.ts.validar_alias_existente(alias_dir)
            
            condicao['dir_tipo'] = 'coluna'
            condicao['dir_alias'] = alias_dir
            condicao['dir_col'] = col_dir
            
        elif token_alvo.tipo in ['NUMERO', 'STRING']:
            # q14 -> q17 (É um valor estático, ex: -1,5 ou 'ativo')
            # Delega para o AutomatoValor processar e formatar
            valor_estatico = AutomatoValor(self.ctx).analisar()
            
            condicao['dir_tipo'] = 'valor'
            condicao['dir_val'] = valor_estatico
            
        else:
            raise Exception(f"Erro no ON do Join: O alvo da condição deve ser 'alias.coluna', 'numero' ou 'string'. Obtido: {token_alvo.valor}")
            
        return condicao

    def fluxo_q17(self, condicoes_extras):
        token = self.ctx.token_atual
        if token and token.valor == ')':
            # q17 -> q19 [label=")"] FIM DO JOIN
            self.ctx.consumir('PONTUACAO', ')')
            return
            
        elif token and token.valor == ',':
            # q17 -> q18 [label=","]
            self.ctx.consumir('PONTUACAO', ',')
            
            # q18 -> q17 [label="funcao"]
            func_resultado = AutomatoFuncao(self.ctx).analisar()
            condicoes_extras.append(func_resultado)
            
            # Recursão de volta para q17
            self.fluxo_q17(condicoes_extras)
        else:
            raise Exception(f"Erro no ON do Join: Esperado ',' ou ')', mas obteve '{token.valor}'")