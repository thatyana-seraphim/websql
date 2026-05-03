from sintatico.sub_automatos.automato_funcao import AutomatoFuncao

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
        
        # Correção estrutural: Inserindo o ponto exigido pela sintaxe
        self.ctx.consumir('PONTUACAO', '.')
        
        # Em q7, lemos o alvo (Pode ser um 'alias' ou um 'valor')
        alvo = self.ctx.consumir().valor
        
        condicao = {
            'esq_alias': alias_esq, 
            'esq_col': col_esq, 
            'op': relacional
        }

        # Bifurcação a partir de q7
        if self.ctx.token_atual and self.ctx.token_atual.valor == '.':
            # É Alias.Coluna (q7 -> q8 -> q9 -> q10)
            self.ctx.consumir('PONTUACAO', '.')
            col_dir = self.ctx.consumir('IDENTIFICADOR').valor
            self.ctx.ts.validar_alias_existente(alvo) # alvo era o alias
            
            condicao['dir_tipo'] = 'coluna'
            condicao['dir_alias'] = alvo
            condicao['dir_col'] = col_dir
        else:
            # É um valor estático (q7 -> q10)
            condicao['dir_tipo'] = 'valor'
            condicao['dir_val'] = alvo
            
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