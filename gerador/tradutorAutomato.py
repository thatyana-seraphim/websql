class TradutorSQL:
    def __init__(self, tabela_simbolos):
        # O Tradutor recebe a Tabela de Símbolos já validada
        self.ts = tabela_simbolos

    def gerar(self):
        # 1. Validação básica
        if not self.ts.tabelas_principais:
            return "-- Erro: Nenhuma tabela definida."

        # 2. Construção da cláusula SELECT (usamos o padrão * se vazio)
        if self.ts.colunas_select == '*':
            select_str = "*"
        else:
            partes_select = []
            for c in self.ts.colunas_select:
                # Formata u.nome ou sum(u.valor)
                campo = f"{c['alias']}.{c['coluna']}"
                if c['funcao']:
                    partes_select.append(f"{c['funcao'].upper()}({campo})")
                else:
                    partes_select.append(campo)
            
            # Se a lista estiver vazia por algum motivo, assume * como fallback
            select_str = ", ".join(partes_select) if partes_select else "*"

        sql = f"SELECT {select_str} "

        # 3. Construção da cláusula FROM para o sub-autómato Tables
        # Transformamos [{'nome': 'usuarios', 'alias': 'u'}, {'nome': 'pedidos', 'alias': 'p'}]
        # em ["usuarios u", "pedidos p"]
        clausulas_from = [f"{t['nome']} {t['alias']}" for t in self.ts.tabelas_principais]
        
        # Junta as tabelas com vírgulas
        sql += "FROM " + ", ".join(clausulas_from)

        # 4. Adiciona outras cláusulas se existirem (ex: Where, Joins)
        if self.ts.condicao_where:
            sql += f" WHERE {self.ts.condicao_where}"
            
        if self.ts.coluna_orderby:
            sql += f" ORDER BY {self.ts.coluna_orderby}"

        return sql + ";"