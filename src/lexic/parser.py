from lexic.token_lexico import Token


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.token: Token | None

    def main(self) -> None:
        self.token = self.get_next_token()
        if self.ifelse() and self.match_t("EOF"):
            print("Sintaticamente correto")
        else:
            self._erro("main")

    def get_next_token(self) -> Token | None:
        if len(self.tokens) > 0:
            return self.tokens.pop(0)
        return None

    def _erro(self, regra: str) -> None:
        print("Regra", regra)
        print("Token invalido", self.token)
        print("----" * 10)

    def ifelse(self) -> bool:
        if (
            self.match_l("if")
            and self.condicao()
            and self.match_l("then")
            and self.expressao()
            and self.match_l("else")
            and self.expressao()
        ):
            return True
        self._erro("ifelse")
        return False

    def condicao(self) -> bool:
        if self.id() and self.operador() and self.num():
            return True

        self._erro("condicao")
        return False

    def expressao(self) -> bool:
        if self.id() and self.operador_atribuicao() and self.num():
            return True

        self._erro("Expressão")
        return False

    def operador(self) -> bool:
        if self.match_t("operador_condicional"):
            return True
        self._erro("operador")
        return False

    def operador_atribuicao(self) -> bool:
        if self.match_t("operador_atribuicao"):
            return True
        self._erro("Operador atribuicao")
        return False

    def id(self) -> bool:
        if self.match_t("id"):
            return True
        self._erro("id")
        return False

    def num(self) -> bool:
        if self.match_t("num"):
            return True
        self._erro("num")
        return False

    def match_l(self, lexema: str) -> bool:
        if self.token is not None and self.token.lexema == lexema:
            self.token = self.get_next_token()
            return True
        return False

    def match_t(self, tipo: str) -> bool:
        if self.token is not None and self.token.tipo == tipo:
            self.token = self.get_next_token()
            return True
        return False
