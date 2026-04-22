class TabelaSimbolos:
    def __init__(self):
        self.tabela_principal = None
        self.tabelas_join = []
        self.colunas_select = "*"  # Padrão é * se não for especificado
        self.condicao_where = None
        self.coluna_groupby = None
        self.condicao_having = None
        self.coluna_orderby = None

    def __repr__(self):
        """Apenas para visualizarmos os dados no terminal durante os testes"""
        return str(self.__dict__)