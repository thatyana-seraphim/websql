class TradutorSQL:
    def __init__(self, tabela_simbolos):
        # Recebe a memória preenchida pelo analisador sintático
        self.ts = tabela_simbolos

    def gerar(self):
        if not self.ts.tabela_principal:
            return "Erro: Tabela principal não definida."

        sql = f"SELECT {self.ts.colunas_select} FROM {self.ts.tabela_principal}"
        
        for join_table in self.ts.tabelas_join:
            sql += f" INNER JOIN {join_table}"
            
        if self.ts.condicao_where:
            sql += f" WHERE {self.ts.condicao_where}"
            
        # Adicionar Group By, Having, Order By aqui seguindo a mesma lógica...
        
        return sql + ";"