import re

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo  # 'KEYWORD' ou 'VALUE'
        self.valor = valor

    def __repr__(self):
        return f"[{self.tipo}: {self.valor}]"

class Scanner:
    def __init__(self):
        # Captura nossas palavras-chave exatas (Grupo 1) OU captura qualquer outro texto como valor (Grupo 2)
        # Ex: "URLTablesusuarios" -> 'URL', 'Tables', 'usuarios'
        padrao = r'(URL|Tables|join|select|where|orderby|groupby|having|\&)|([a-zA-Z0-9_,=><\']+)'
        self.regex = re.compile(padrao)

    def tokenizar(self, entrada_bruta):
        tokens = []
        for match in self.regex.finditer(entrada_bruta):
            keyword, valor = match.groups()
            if keyword:
                tokens.append(Token('KEYWORD', keyword))
            elif valor:
                tokens.append(Token('VALUE', valor))
        return tokens