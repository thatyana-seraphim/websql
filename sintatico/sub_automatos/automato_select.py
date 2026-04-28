class AutomatoSelect:
    def __init__(self, parser_context):
        self.ctx = parser_context

    def analisar(self):
        # start -> q0 -> q1 [label="select"]
        self.ctx.consumir('KEYWORD', 'select')
        
        # q1 -> q2 [label="="]
        self.ctx.consumir('PONTUACAO', '=')
        
        # Inicia a validação das colunas
        self.fluxo_q2()

    def fluxo_q2(self):
        token = self.ctx.token_atual

        # REGRA: Trata o curinga '*' (q2 -> q8)
        if token and token.valor == "*":
            self.ctx.consumir('PONTUACAO', '*')
            self.ctx.ts.definir_todas_colunas()
            return  # Encerra no estado de aceitação q8
        
        # REGRA: Impede que erros de digitação (ex: 'coun') sejam tratados como função
        elif token.tipo == 'AGREGACAO':
            # q2 -> q3 [label="agregacao"]
            funcao = self.ctx.consumir('AGREGACAO').valor
            
            # q3 -> q4 [label="."]
            self.ctx.consumir('PONTUACAO', '.') 
            
            # Delega para q4 passando a função capturada
            self.fluxo_q4(funcao)

        # REGRA: Trata o alias direto, sem agregação
        elif token.tipo == 'IDENTIFICADOR':
            # q2 -> q5 [label="alias"]
            # Como não tem agregação, enviamos 'None' como função
            self.fluxo_q5(funcao=None)
            
        else:
            raise Exception(f"Erro Sintático em q2: Esperado '*', Agregação ou Alias. Obtido: '{token.valor}'")

    def fluxo_q4(self, funcao):
        # q4 -> q5 [label="alias"] (Caminho para quando há agregação)
        alias = self.ctx.consumir('IDENTIFICADOR').valor
        
        # Segue para o ponto em comum q5
        self.fluxo_q5_direto(funcao, alias)

    def fluxo_q5(self, funcao):
        # q2 -> q5 [label="alias"] (Caminho direto, sem agregação)
        alias = self.ctx.consumir('IDENTIFICADOR').valor
        
        # Segue para o ponto em comum q5
        self.fluxo_q5_direto(funcao, alias)

    def fluxo_q5_direto(self, funcao, alias):
        # q5 -> q6 [label="."]
        self.ctx.consumir('PONTUACAO', '.')
        
        # q6 -> q7 [label="coluna"]
        coluna = self.ctx.consumir('IDENTIFICADOR').valor
        
        # REGRA: A Validação Semântica ocorre AQUI.
        # O método 'adicionar_coluna' da Tabela de Símbolos vai disparar um erro
        # se o 'alias' fornecido não existir no array de tabelas.
        self.ctx.ts.adicionar_coluna(funcao, alias, coluna)
        
        self.fluxo_q7()

    def fluxo_q7(self):
        # Verifica se existe recursão para novas colunas
        if self.ctx.token_atual and self.ctx.token_atual.valor == ',':
            # q7 -> q2 [label=","]
            self.ctx.consumir('PONTUACAO', ',')
            self.fluxo_q2()
        else:
            # Estado final de aceitação q7
            return