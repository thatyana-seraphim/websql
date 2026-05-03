from semantico.tabela_simbolos import TabelaSimbolos
from sintatico.sub_automatos.automato_tables import AutomatoTables
from sintatico.sub_automatos.automato_join import AutomatoJoin
from sintatico.sub_automatos.automato_select import AutomatoSelect
from sintatico.sub_automatos.automato_where import AutomatoWhere
from sintatico.sub_automatos.automato_groupby import AutomatoGroupby
from sintatico.sub_automatos.automato_having import AutomatoHaving
from sintatico.sub_automatos.automato_orderby import AutomatoOrderby

class ParserPrincipal:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos] if self.tokens else None
        
        # Instancia a Tabela de Símbolos (A Memória do Compilador)
        self.ts = TabelaSimbolos()

    def consumir(self, tipo_esperado=None, valor_esperado=None):
        token = self.token_atual
        if not token:
            raise Exception("Erro Sintático: Fim inesperado da URL.")
            
        if tipo_esperado and token.tipo != tipo_esperado:
            raise Exception(f"Erro Sintático: Esperava tipo '{tipo_esperado}', obteve '{token.tipo}'")
        if valor_esperado and token.valor != valor_esperado:
            raise Exception(f"Erro Sintático: Esperava '{valor_esperado}', obteve '{token.valor}'")
        
        self.pos += 1
        self.token_atual = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        return token

    def analisar(self):

        # Inicia e delega o fluxo para o sub-autômato de Tables
        sub_tables = AutomatoTables(self)
        sub_tables.analisar()

        while self.token_atual:
            if self.token_atual.valor == '&':
                # Consome o separador de blocos e avança
                self.consumir('PONTUACAO', '&')
                continue
                
            elif self.token_atual.valor == 'expand':
                # Delega para o Automato de Join
                AutomatoJoin(self).analisar()
                
            elif self.token_atual.valor == 'select':
                # Delega para o Automato de Select
                AutomatoSelect(self).analisar()

            elif self.token_atual.valor == 'where':
                # Delega para o Automato de Where
                AutomatoWhere(self).analisar()
            
            elif self.token_atual.valor == 'groupby':
                # Delega para o Automato de GroupBy
                AutomatoGroupby(self).analisar()
            
            elif self.token_atual.valor == 'having':
                # Delega para o Automato de Having
                AutomatoHaving(self).analisar()

            elif self.token_atual.valor == 'orderby':
                # Delega para o Automato de OrderBy
                AutomatoOrderby(self).analisar()    
        
            else:
                # Quando encontrar uma palavra ainda não implementada (ex: where, orderby)
                # o loop é quebrado até criarmos os próximos sub-autômatos.
                break
                
        return self.ts

    def fluxo_q1(self):
        if self.token_atual and self.token_atual.valor == 'join':
            self.consumir('KEYWORD', 'join')
            # Pega o valor do join (ex: tabela categorias)
            if self.token_atual and self.token_atual.tipo == 'VALUE':
                alvo_join = self.consumir('VALUE')
                self.ts.tabelas_join.append(alvo_join.valor)
            
            # Aqui entraria a chamada para o sub-autômato de Join no futuro
            self.consumir('KEYWORD', '&')
            self.fluxo_q1() # Recursão para múltiplos joins ou ir pro select

        elif self.token_atual and self.token_atual.valor == 'select':
            self.consumir('KEYWORD', 'select')
            # Se tiver colunas especificadas após o select, salva na tabela de símbolos
            if self.token_atual and self.token_atual.tipo == 'VALUE':
                colunas = self.consumir('VALUE')
                self.ts.colunas_select = colunas.valor
            
            # Continua o fluxo (where, orderby, etc... simplificado aqui para brevidade)
            if self.token_atual and self.token_atual.valor == '&':
                self.consumir('KEYWORD', '&')
                self.fluxo_opcionais()

    def fluxo_opcionais(self):
        # Aqui ficarão as transições para q6 (where), q8 (groupby), q12 (orderby)...
        if self.token_atual and self.token_atual.valor == 'where':
            self.consumir('KEYWORD', 'where')
            if self.token_atual and self.token_atual.tipo == 'VALUE':
                condicao = self.consumir('VALUE')
                self.ts.condicao_where = condicao.valor
            # (Pode chamar um `&` e continuar...)