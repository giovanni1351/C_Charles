from collections.abc import Callable
from functools import wraps

from lexic.token_lexico import Token


def visualizar_exec[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """Decorador que mede o tempo de execução de uma função."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        retorno = func(*args, **kwargs)
        if retorno:
            print(f"Sucesso {func.__name__}")
        else:
            print(f"F total {func.__name__}")
        return retorno

    return wrapper


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.token: Token | None

    def main(self) -> None:
        self.token = self.get_next_token()
        if self.programa() and self.match_t("EOF"):
            print("Sintaticamente correto")
        else:
            self._erro("main")

    def get_next_token(self) -> Token | None:
        if len(self.tokens) > 0:
            return self.tokens.pop(0)
        return None

    def _erro(self, regra: str) -> None:
        print(f"Erro na regra {regra= }")
        print("Regra", regra)
        print("Token invalido", self.token)
        print("----" * 10)
        exit()

    @visualizar_exec
    def cmd_if(self) -> bool:
        return bool(
            self.match_l("if")
            and self.match_l("(")
            and self.condicional()
            and self.match_l(")")
            and self.match_l("->")
            and self.match_l("{")
            and self.expressao()
            and self.match_l("}")
            and self.option_else()
        )

    @visualizar_exec
    def option_else(self) -> bool:
        if (
            self.match_l("else")
            and self.match_l("{")
            and self.bloco()
            and self.match_l("}")
        ):
            return True
        return True

    @visualizar_exec
    def bloco(self) -> bool:
        return self.cmd() and self.bloco_options()

    @visualizar_exec
    def operador_atribuicao(self) -> bool:
        if self.match_t("operador_atribuicao"):
            return True
        self._erro("Operador atribuicao")
        return False

    @visualizar_exec
    def id(self) -> bool:
        if self.match_t("ID"):
            return True
        self._erro("id")
        return False

    @visualizar_exec
    def num(self) -> bool:
        if self.match_t("num"):
            return True
        self._erro("num")
        return False

    @visualizar_exec
    def programa(self) -> bool:
        return bool(
            self.tipo()
            and self.match_l("charles")
            and self.match_l("(")
            and self.match_l(")")
            and self.match_l("->")
            and self.match_l("{")
            and self.bloco()
            and self.match_l("}")
        )

    @visualizar_exec
    def bloco_options(self) -> bool:
        if self.bloco():
            return True
        return True

    @visualizar_exec
    def cmd(self) -> bool:
        if self.leitura():
            return True
        if self.escrita():
            return True

        if self.declarar():
            return True
        if self.atribuicao():
            return True

        if self.cmd_if():
            return True
        return False

    @visualizar_exec
    def declarar(self) -> bool:
        return self.tipo() and self.declarar_options()

    @visualizar_exec
    def declarar_options(self) -> bool:
        return (self.id() and self.match_l(";")) or self.atribuicao()

    @visualizar_exec
    def condicional(self) -> bool: ...

    @visualizar_exec
    def expressao(self) -> bool: ...

    @visualizar_exec
    def exp_prioridade(self) -> bool: ...

    @visualizar_exec
    def fator(self) -> bool: ...

    @visualizar_exec
    def leitura(self) -> bool: ...

    @visualizar_exec
    def escrita(self) -> bool: ...

    @visualizar_exec
    def escrita_options(self) -> bool: ...

    @visualizar_exec
    def atribuicao(self) -> bool:
        return (
            self.id()
            and self.match_l("<-")
            and self.atribuicao_options()
            and self.match_l(";")
        )

    @visualizar_exec
    def atribuicao_options(self) -> bool:
        return self.expressao() or self.texto_string()

    @visualizar_exec
    def texto_string(self) -> bool: ...

    @visualizar_exec
    def operador_relacional(self) -> bool: ...

    @visualizar_exec
    def tipo(self) -> bool:
        return (
            self.match_l("int")
            or self.match_l("float")
            or self.match_l("boolean")
            or self.match_l("string")
        )

    @visualizar_exec
    def operador_logico(self) -> bool: ...

    @visualizar_exec
    def num_int(self) -> bool: ...

    @visualizar_exec
    def num_decimal(self) -> bool: ...

    @visualizar_exec
    def loop_for(self) -> bool: ...

    @visualizar_exec
    def loop_while(self) -> bool: ...

    def match_l(self, lexema: str) -> bool:
        print(f"{lexema= }")
        if self.token is not None and self.token.lexema == lexema:
            self.token = self.get_next_token()
            return True
        return False

    def match_t(self, tipo: str) -> bool:
        if self.token is not None and self.token.tipo == tipo:
            self.token = self.get_next_token()
            return True
        return False
