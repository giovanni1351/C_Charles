from lexic.token_lexico import Token


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.token: Token | None

    def main(self) -> None:
        self.token = self.get_next_token()
        if self.cmd_if() and self.match_t("EOF"):
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

    def cmd_if(self) -> bool:
        if (
            self.match_l("if")
            and self.match_l("(")
            and self.condicional()
            and self.match_l(")")
            and self.match_l("->")
            and self.match_l("{")
            and self.expressao()
            and self.match_l("}")
            and self.option_else()
        ):
            return True
        self._erro("ifelse")
        return False

    def option_else(self) -> bool:
        if (
            self.match_l("else")
            and self.match_l("{")
            and self.bloco()
            and self.match_l("}")
        ):
            return True
        return True

    def bloco(self) -> bool:
        return self.cmd() and self.bloco_options()

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

    def programa(self) -> bool:
        return bool(
            self.tipo()
            and self.match_l("charles()")
            and self.match_l("{")
            and self.bloco()
            and self.match_l("}")
        )

    def bloco_options(self) -> bool:
        if self.bloco():
            return True
        return True

    def cmd(self) -> bool:
        if self.leitura():
            return True
        if self.escrita():
            return True

        if self.atribuicao():
            return True

        if self.cmd_if():
            return True

        return self.declarar()

    def declarar(self) -> bool: ...

    def declarar_options(self) -> bool: ...

    def condicional(self) -> bool: ...

    def expressao(self) -> bool: ...

    def exp_prioridade(self) -> bool: ...

    def fator(self) -> bool: ...

    def leitura(self) -> bool: ...

    def escrita(self) -> bool: ...

    def escrita_options(self) -> bool: ...

    def atribuicao(self) -> bool: ...

    def atribuicao_options(self) -> bool: ...

    def texto_string(self) -> bool: ...

    def operador_relacional(self) -> bool: ...

    def tipo(self) -> bool: ...

    def operador_logico(self) -> bool: ...

    def num_int(self) -> bool: ...

    def num_decimal(self) -> bool: ...

    def loop_for(self) -> bool: ...

    def loop_while(self) -> bool: ...

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
