class TabelaSimbolos:
    def __init__(self):
        self.tabelas_principais = []
        self.tabelas_join = []
        self.colunas_select = []  # Padrão é * se não for especificado
        self.condicao_where = []
        self.coluna_groupby = []
        self.condicao_having = []
        self.coluna_orderby = []

    def alias_existe(self, alias):
        """Verifica se o alias já existe no escopo global da query."""
        existe_principal = any(t['alias'] == alias for t in self.tabelas_principais)
        existe_join = any(j['alias'] == alias for j in self.tabelas_join)
        return existe_principal or existe_join

    def validar_alias_existente(self, alias):
        """Trava de segurança: Usada quando o usuário TENTA usar um alias."""
        if not self.alias_existe(alias):
            raise Exception(f"Erro Semântico: O alias '{alias}' não foi declarado.")

    def registrar_nova_tabela(self, nome, alias, is_join=False):
        """Trava de segurança: Usada quando o usuário CRIA um novo alias."""
        if self.alias_existe(alias):
            raise Exception(f"Erro Semântico: O alias '{alias}' já está em uso por outra tabela e não pode ser reatribuído.")
        
        if is_join:
            # Pré-registra o JOIN na memória para que o alias passe a existir.
            # Isso é crucial para que a validação dentro do ON funcione.
            self.tabelas_join.append({
                'tabela': nome,
                'alias': alias,
                'condicao_principal': None,
                'condicoes_extras': []
            })
        else:
            self.tabelas_principais.append({'nome': nome, 'alias': alias})
        
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
    
    def adicionar_join(self, tabela, alias, condicao_principal, condicoes_extras):
        """Busca o JOIN que foi pré-registrado e atualiza com as condições capturadas."""
        for j in self.tabelas_join:
            if j['tabela'] == tabela and j['alias'] == alias:
                j['condicao_principal'] = condicao_principal
                j['condicoes_extras'] = condicoes_extras
                break
    
    # Adicione este método dentro da classe TabelaSimbolos
    def adicionar_where(self, condicao_principal, condicoes_extras):
        self.condicao_where = {
            'condicao_principal': condicao_principal,
            'condicoes_extras': condicoes_extras
        }
    
    # Adicione este método dentro da classe TabelaSimbolos
    def adicionar_groupby(self, alias, coluna):
        """Valida e adiciona uma coluna à cláusula GROUP BY."""
        self.validar_alias_existente(alias)
        
        self.coluna_groupby.append({
            'alias': alias,
            'coluna': coluna
        })

    def adicionar_having(self, agregacao, alias_esq, col_esq, relacional, alvo_dict, logico=None):
        """Valida e armazena uma condição do HAVING."""
        # Valida o lado esquerdo
        self.validar_alias_existente(alias_esq)
        
        # Valida o lado direito (se for um alias.coluna)
        if alvo_dict['tipo'] == 'coluna':
            self.validar_alias_existente(alvo_dict['alias'])

        self.condicao_having.append({
            'logico': logico, # None para a 1ª condição, 'and'/'or' para as demais
            'agregacao': agregacao,
            'esq_alias': alias_esq,
            'esq_col': col_esq,
            'op': relacional,
            'dir': alvo_dict
        })

    def adicionar_orderby(self, alias, coluna, direcao):
        """Valida e adiciona uma coluna à cláusula ORDER BY."""
        self.validar_alias_existente(alias)
        
        self.coluna_orderby.append({
            'alias': alias,
            'coluna': coluna,
            'direcao': direcao.upper() # ASC ou DESC
        })

    def __repr__(self):
        """Apenas para visualizarmos os dados no terminal durante os testes"""
        return str(self.__dict__)