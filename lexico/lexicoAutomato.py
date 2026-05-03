import re

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo  # 'KEYWORD' ou 'VALUE'
        self.valor = valor

    def __repr__(self):
        return f"[{self.tipo}: {self.valor}]"

class Scanner:
    def __init__(self):
        # 1. Pontuação Estrutural do seu autômato
        pontuacao = r'(/|:|,|\?|\&|\.|=|\*|\(|\))'
        
        # 2. Palavras reservadas e Expressões que você definiu
        relacional = r'\b(eq|neg|gt|gte|lt|lte|like|in)\b'
        agregacao = r'\b(count|sum|avg|min|max)\b'
        keywords = r'\b(select|expand|on|where|orderby|groupby|having|and|or|asc|desc)\b'
        
        # 3. Identificadores (letra seguida de letras/dígitos) e Números
        identificador = r'\b([a-zA-Z][a-zA-Z0-9_]*)\b' 
        numero = r'\b([0-9]+)\b'

        # Agrupa tudo em um único Regex usando grupos nomeados para facilitar
        padrao = f'(?P<PONTUACAO>{pontuacao})|(?P<RELACIONAL>{relacional})|(?P<AGREGACAO>{agregacao})|(?P<KEYWORD>{keywords})|(?P<IDENTIFICADOR>{identificador})|(?P<NUMERO>{numero})'
        self.regex = re.compile(padrao)

    def tokenizar(self, entrada_bruta):
        tokens = []
        for match in self.regex.finditer(entrada_bruta):
            tipo = match.lastgroup
            valor = match.group(tipo)
            tokens.append(Token(tipo, valor))
        return tokens