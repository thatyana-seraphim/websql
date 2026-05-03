class TradutorSQL:
    def __init__(self, tabela_simbolos):
        # O Tradutor recebe a Tabela de Símbolos já validada
        self.ts = tabela_simbolos

        # Mapa de conversão: Linguagem URL -> Linguagem SQL
        self.mapa_operadores = {
            'eq': '=',
            'neg': '!=',
            'gt': '>',
            'gte': '>=',
            'lt': '<',
            'lte': '<=',
            'like': 'LIKE',
            'in': 'IN'
        }
    
    def formatar_condicao_funcao(self, cond):
        """Converte o retorno do AutomatoFuncao para a sintaxe SQL"""
        logico = cond['logico'].upper() # AND ou OR
        esq = f"{cond['esq_alias']}.{cond['esq_col']}"
        op = self.mapa_operadores.get(cond['relacional'], cond['relacional'])
        
        if cond['dir_tipo'] == 'coluna':
            dir_val = f"{cond['dir_alias']}.{cond['dir_col']}"
        else:
            # Se for um valor direto (ex: 1, 'ativo')
            dir_val = cond['dir_val']
            
        return f" {logico} {esq} {op} {dir_val}"

    def gerar(self):
        # 1. Validação básica
        if not self.ts.tabelas_principais:
            return "-- Erro: Nenhuma tabela principal definida."

        # 2. Construção da cláusula SELECT (Tratando q7 e q8)
        if self.ts.colunas_select == '*':
            select_str = "*"
        else:
            partes_select = []
            for c in self.ts.colunas_select:
                campo = f"{c['alias']}.{c['coluna']}"
                partes_select.append(f"{c['funcao'].upper()}({campo})" if c['funcao'] else campo)
            select_str = ", ".join(partes_select) if partes_select else "*"

        sql = f"SELECT {select_str}\n"

        # 3. Construção da cláusula FROM 
        clausulas_from = [f"{t['nome']} {t['alias']}" for t in self.ts.tabelas_principais]
        sql += "FROM " + ", ".join(clausulas_from) + "\n"

        # 4. Construção da cláusula JOIN (Expand)
        for j in self.ts.tabelas_join:
            tab = j['tabela']
            alias = j['alias']
            
            # Formata a condição principal (agora suporta valores diretos)
            cp = j['condicao_principal']
            op_princ = self.mapa_operadores.get(cp['op'], cp['op'])
            esq_clause = f"{cp['esq_alias']}.{cp['esq_col']}"
            
            if cp['dir_tipo'] == 'coluna':
                dir_clause = f"{cp['dir_alias']}.{cp['dir_col']}"
            else:
                dir_clause = cp['dir_val']
                
            on_clause = f"{esq_clause} {op_princ} {dir_clause}"
            
            # Concatena as funções extras (And/Or) se existirem
            for cond_extra in j['condicoes_extras']:
                on_clause += self.formatar_condicao_funcao(cond_extra)
                
            sql += f"INNER JOIN {tab} {alias} ON ({on_clause})\n"

        # 5. Adiciona outras cláusulas se existirem (Where, OrderBy, etc.)
        if hasattr(self.ts, 'condicao_where') and self.ts.condicao_where:
            cw = self.ts.condicao_where
            cp = cw['condicao_principal']
            
            # Formata a condição principal do WHERE
            op_princ = self.mapa_operadores.get(cp['op'], cp['op'])
            esq_clause = f"{cp['esq_alias']}.{cp['esq_col']}"
            
            if cp['dir_tipo'] == 'coluna':
                dir_clause = f"{cp['dir_alias']}.{cp['dir_col']}"
            else:
                dir_clause = cp['dir_val']
                
            where_clause = f"{esq_clause} {op_princ} {dir_clause}"
            
            # Concatena as funções extras (And/Or) se existirem
            for cond_extra in cw['condicoes_extras']:
                where_clause += self.formatar_condicao_funcao(cond_extra)
                
            sql += f"WHERE {where_clause}\n"
        
        # 6. Construção da cláusula GROUP BY
        if hasattr(self.ts, 'coluna_groupby') and self.ts.coluna_groupby:
            partes_groupby = [f"{c['alias']}.{c['coluna']}" for c in self.ts.coluna_groupby]
            sql += f"GROUP BY {', '.join(partes_groupby)}\n"

        # 7. Construção da cláusula HAVING
        if hasattr(self.ts, 'condicao_having') and self.ts.condicao_having:
            having_parts = []
            
            for index, cond in enumerate(self.ts.condicao_having):
                # Monta a parte esquerda: SUM(p.valor)
                esq_str = f"{cond['agregacao'].upper()}({cond['esq_alias']}.{cond['esq_col']})"
                op_str = self.mapa_operadores.get(cond['op'], cond['op'])
                
                # Monta a parte direita
                alvo = cond['dir']
                dir_str = f"{alvo['alias']}.{alvo['coluna']}" if alvo['tipo'] == 'coluna' else alvo['valor']
                
                cond_str = f"{esq_str} {op_str} {dir_str}"
                
                # Se for a 1ª condição, não tem operador lógico antes. Se não for, tem.
                if index == 0:
                    having_parts.append(cond_str)
                else:
                    having_parts.append(f"{cond['logico'].upper()} {cond_str}")
                    
            sql += f"HAVING {' '.join(having_parts)}\n"

        # 8. Construção da cláusula ORDER BY
        if hasattr(self.ts, 'coluna_orderby') and self.ts.coluna_orderby:
            partes_orderby = [f"{c['alias']}.{c['coluna']} {c['direcao']}" for c in self.ts.coluna_orderby]
            sql += f"ORDER BY {', '.join(partes_orderby)}\n"

        # Remove última quebra de linha e finaliza
        return sql.strip() + ";"
            