import re

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo  # 'KEYWORD' ou 'VALUE'
        self.valor = valor

    def __repr__(self):
        return f"[{self.tipo}: {self.valor}]"

class Scanner:
    def __init__(self):
        # Autômato String: q0 -> q1 ['] -> q2 [letra/digito] -> q3 [']
        string = r"(?P<STRING>'[^']*')" 
        
        # Autômato Número: Suporta '-', dígitos, e a transição da ',' (ex: -10,5)
        numero = r"(?P<NUMERO>-?\d+(,\d+)?)" 
        
        pontuacao = r"(?P<PONTUACAO>[/:,\?&\.=\(\)\*])"
        relacional = r"(?P<RELACIONAL>\b(eq|neg|gt|gte|lt|lte|like|in)\b)"
        agregacao = r"(?P<AGREGACAO>\b(count|sum|avg|min|max)\b)"
        keywords = r"(?P<KEYWORD>\b(select|expand|on|where|orderby|groupby|having|and|or|asc|desc)\b)"
        identificador = r"(?P<IDENTIFICADOR>\b[a-zA-Z][a-zA-Z0-9_]*\b)"

        # O Regex compila todas as regras na ordem correta
        padrao = f"{string}|{numero}|{relacional}|{agregacao}|{keywords}|{identificador}|{pontuacao}"
        self.regex = re.compile(padrao)

    def tokenizar(self, entrada_bruta):
        tokens = []
        for match in self.regex.finditer(entrada_bruta):
            tipo = match.lastgroup
            valor = match.group(tipo)
            tokens.append(Token(tipo, valor))
        return tokens