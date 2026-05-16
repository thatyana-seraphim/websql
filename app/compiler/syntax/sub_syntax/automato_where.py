from app.compiler.syntax.sub_syntax.automato_funcao import AutomatoFuncao
from app.compiler.syntax.sub_syntax.automato_valor import AutomatoValor

class AutomatoWhere:
    def __init__(self, parser_context):
        self.ctx = parser_context

    def analisar(self):
        # q0 -> q1 -> q2
        self.ctx.consumir('KEYWORD', 'where')
        self.ctx.consumir('PONTUACAO', '=')

        # Lê a primeira condição obrigatória (q2 a q10)
        cond_principal = self.ler_condicao_principal()

        # Prepara a lista e inicia o loop (q10 -> q11 -> q10)
        condicoes_extras = []
        self.fluxo_q10(condicoes_extras)

        # Salva na Tabela de Símbolos
        self.ctx.ts.adicionar_where(cond_principal, condicoes_extras)

    def ler_condicao_principal(self):
        # q2 -> q3 -> q4 -> q5 -> q6 -> q7
        alias_esq = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.ts.validar_alias_existente(alias_esq)
        
        self.ctx.consumir('PONTUACAO', '.')
        col_esq = self.ctx.consumir('IDENTIFICADOR').valor
        self.ctx.consumir('PONTUACAO', '.')
        relacional = self.ctx.consumir('RELACIONAL').valor
        
        # Em q7, lemos o alvo (Pode ser um 'alias' ou um 'valor')
        self.ctx.consumir('PONTUACAO', '.')
        
        condicao = {
            'esq_alias': alias_esq, 
            'esq_col': col_esq, 
            'op': relacional
        }

        # Bifurcação a partir de q7 baseada no TIPO do token
        token_alvo = self.ctx.token_atual
        
        if token_alvo.tipo == 'IDENTIFICADOR':
            # É Alias.Coluna (q7 -> q8 -> q9 -> q10)
            alias_dir = self.ctx.consumir('IDENTIFICADOR').valor
            self.ctx.consumir('PONTUACAO', '.')
            col_dir = self.ctx.consumir('IDENTIFICADOR').valor
            
            # Validação Semântica do Alias da direita
            self.ctx.ts.validar_alias_existente(alias_dir) 
            
            condicao['dir_tipo'] = 'coluna'
            condicao['dir_alias'] = alias_dir
            condicao['dir_col'] = col_dir
            
        elif token_alvo.tipo in ['NUMERO', 'STRING']:
            # É um valor estático (q7 -> q10)
            # Delega para o AutomatoValor processar e formatar (ex: '10,5' -> '10.5')
            valor_estatico = AutomatoValor(self.ctx).analisar()
            
            condicao['dir_tipo'] = 'valor'
            condicao['dir_val'] = valor_estatico
            
        else:
            raise Exception(f"Erro no Where: O alvo da condição deve ser 'alias.coluna', 'numero' ou 'string'. Obtido: {token_alvo.valor}")
            
        return condicao
            
        return condicao

    def fluxo_q10(self, condicoes_extras):
        token = self.ctx.token_atual
        
        # Se não houver mais tokens ou houver o separador de blocos '&', o Where acabou
        if not token or token.valor == '&':
            return
            
        # q10 -> q11 [label=","]
        elif token.valor == ',':
            self.ctx.consumir('PONTUACAO', ',')
            
            # q11 -> q10 [label="função"] (Reutiliza o AutomatoFuncao!)
            func_resultado = AutomatoFuncao(self.ctx).analisar()
            condicoes_extras.append(func_resultado)
            
            # Volta para q10
            self.fluxo_q10(condicoes_extras)
        else:
            raise Exception(f"Erro no Where: Esperado ',' ou '&', mas obteve '{token.valor}'")