class AutomatoValor:
    def __init__(self, parser_context):
        self.ctx = parser_context

    def analisar(self):
        token = self.ctx.token_atual
        
        # Transição q0 -> numero
        if token.tipo == 'NUMERO':
            valor_bruto = self.ctx.consumir('NUMERO').valor
            # Ajuste de tradução: SQL não entende '10,5', apenas '10.5'
            return valor_bruto.replace(',', '.')
            
        # Transição q0 -> string
        elif token.tipo == 'STRING':
            # Mantém as aspas para o SQL (ex: 'ativo')
            return self.ctx.consumir('STRING').valor
            
        else:
            raise Exception(f"Erro Sintático: Esperado um 'numero' ou 'string'. Obtido: '{token.valor}'")