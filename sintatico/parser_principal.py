from semantico.tabela_simbolos import TabelaSimbolos
from sintatico.sub_automatos.automato_tables import AutomatoTables
from sintatico.sub_automatos.automato_select import AutomatoSelect

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
            raise Exception("Fim inesperado da URL.")
            
        if tipo_esperado and token.tipo != tipo_esperado:
            raise Exception(f"Sintaxe Errada: Esperava tipo '{tipo_esperado}', obteve '{token.tipo}'")
        if valor_esperado and token.valor != valor_esperado:
            raise Exception(f"Sintaxe Errada: Esperava '{valor_esperado}', obteve '{token.valor}'")
        
        self.pos += 1
        self.token_atual = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        return token

    def analisar(self):
        """
        # start -> q0 -> q1
        self.consumir('KEYWORD', 'URL')
        self.consumir('KEYWORD', 'Tables')
        
        # O próximo token DEVE ser o nome da tabela principal (um VALUE)
        if self.token_atual and self.token_atual.tipo == 'VALUE':
            tabela = self.consumir('KEYWORD' if False else 'VALUE') # Hack simples p/ clareza
            self.ts.tabela_principal = tabela.valor
        else:
            raise Exception("Esperado o nome da tabela após 'Tables'")

        self.fluxo_q1()
        
        """

        # Inicia e delega o fluxo para o sub-autômato de Tables
        sub_tables = AutomatoTables(self)
        sub_tables.analisar()

        if self.token_atual.valor == 'select':
            # 1. Delega para o sub-autômato processar a lista de colunas
            sub_select = AutomatoSelect(self)
            sub_select.analisar()
            # 2. Ao voltar do sub-autômato, verificamos se há um '&' 
            # para seguir para a próxima cláusula (Where, Join, etc)
            if self.token_atual and self.token_atual.valor == '&':
                self.consumir('PONTUACAO', '&')
                # self.fluxo_proximas_clausulas()

        return self.ts  # Retorna a tabela preenchida!

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