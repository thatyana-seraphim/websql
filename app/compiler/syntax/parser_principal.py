from app.compiler.semantic.tabela_simbolos import TabelaSimbolos
from app.compiler.syntax.sub_syntax.automato_tables import AutomatoTables
from app.compiler.syntax.sub_syntax.automato_join import AutomatoJoin
from app.compiler.syntax.sub_syntax.automato_select import AutomatoSelect
from app.compiler.syntax.sub_syntax.automato_where import AutomatoWhere
from app.compiler.syntax.sub_syntax.automato_groupby import AutomatoGroupby
from app.compiler.syntax.sub_syntax.automato_having import AutomatoHaving
from app.compiler.syntax.sub_syntax.automato_orderby import AutomatoOrderby

class ParserPrincipal:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos] if self.tokens else None
        
        # Instancia a Tabela de Símbolos (A Memória do Compilador)
        self.ts = TabelaSimbolos()

    def throw_error(self, message: str):
        """
        Monta uma string mostrando exatamente onde o compilador se perdeu.
        Pega os 3 tokens anteriores e os 3 próximos.
        """
        inicio = max(0, self.pos - 3)
        fim = min(len(self.tokens), self.pos + 4)
        
        # Monta o trecho do erro
        trecho_tokens = []
        for i in range(inicio, fim):
            if i == self.pos:
                # Destaca o token que causou o problema com colchetes
                trecho_tokens.append(f"[{self.tokens[i].valor}]")
            else:
                trecho_tokens.append(self.tokens[i].valor)
                
        contexto_visual = "".join(trecho_tokens)
        
        # Levanta a exceção com a mensagem original + o contexto
        raise Exception(f"Syntax Error: {message} | Perto de: '... {contexto_visual} ...'")

    def consumir(self, tipo_esperado=None, valor_esperado=None):
        token = self.token_atual
        if not token:
            self.throw_error("Fim inesperado da URL.")
            
        if tipo_esperado and token.tipo != tipo_esperado:
           self.throw_error(f"Esperava um tipo '{tipo_esperado}', mas obteve '{token.tipo}' no valor '{token.valor}'")

        if valor_esperado and token.valor != valor_esperado:
            self.throw_error(f"Esperava o valor '{valor_esperado}', mas obteve '{token.valor}'")
        
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
                self.throw_error(f"Bloco desconhecido ou não implementado: '{self.token_atual.valor}'")
                break
                
        return self.ts