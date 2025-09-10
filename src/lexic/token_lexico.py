class Token:
    tipo: str
    lexema: str

    def __init__(self, tipo: str, lexema: str) -> None:
        self.tipo = tipo
        self.lexema = lexema

    def __str__(self) -> str:
        return f"<{self.tipo}, {self.lexema}>"
