class TabelaSimbolos:
    def __init__(self):
        self.tabelas_principais = []
        self.tabelas_join = []
        self.colunas_select = []  # Padrão é * se não for especificado
        self.condicao_where = None
        self.coluna_groupby = None
        self.condicao_having = None
        self.coluna_orderby = None

    def adicionar_tabela(self, nome, alias):
        self.tabelas_principais.append({'nome': nome, 'alias': alias})

    def alias_existe(self, alias):
        # Verifica se o alias está na lista de tabelas principais
        # No futuro, o JOIN também adicionará aliases aqui
        return any(t['alias'] == alias for t in self.tabelas_principais)

    def adicionar_coluna(self, funcao, alias, coluna):
        # Validação Semântica: O alias deve existir
        if not self.alias_existe(alias):
            raise Exception(f"Erro Semântico: O alias '{alias}' não foi declarado no bloco de tabelas.")
        
        self.colunas_select.append({
            'funcao': funcao,
            'alias': alias,
            'coluna': coluna
        })

    def definir_todas_colunas(self):
        self.colunas_select = '*'

    def __repr__(self):
        """Apenas para visualizarmos os dados no terminal durante os testes"""
        return str(self.__dict__)