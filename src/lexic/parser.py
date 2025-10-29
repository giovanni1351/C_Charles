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
        if self.programa() and (self.token is None or self.match_t("EOF")):
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
        if (
            self.match_l("if")
            and self.match_l("(")
            and self.condicional()
            and self.match_l(")")
            and self.match_l("->")
            and self.match_l("{")
            and self.bloco()
            and self.match_l("}")
            and self.option_else()
        ):
            return True
        self._erro("cmd_if")
        return False

    @visualizar_exec
    def option_else(self) -> bool:
        if (
            self.match_l("else")
            and self.match_l("->")
            and self.match_l("{")
            and self.bloco()
            and self.match_l("}")
        ):
            return True
        return True

    @visualizar_exec
    def bloco(self) -> bool:
        if not self.token:
            return False

        if (
            (
                self.token.lexema
                in ["console", "if", "int", "float", "boolean", "string"]
                or self.token.tipo == "ID"
            )
            and self.cmd()
            and self.bloco_options()
        ):
            return True
        self._erro("bloco")
        return False

    @visualizar_exec
    def bloco_options(self) -> bool:
        if not self.token:
            return False
        if (
            self.token.lexema
            in [
                "console",
                "if",
                "int",
                "float",
                "boolean",
                "string",
            ]
            or self.token.tipo == "ID"
        ) and self.bloco():
            return True
        if self.token.lexema == "}":
            return True
        self._erro("bloco_options")
        return False

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
        if not self.token:
            self._erro("num")
            return False
        if self.token.tipo == "INTEGER" and self.num_int():
            return True

        if self.token.tipo == "FLOATING" and self.num_decimal():
            return True

        self._erro("num")
        return False

    @visualizar_exec
    def programa(self) -> bool:
        if not self.token:
            self._erro("programa")
            return False
        if self.token.lexema in ["int", "float", "boolean", "string"]:
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
        self._erro("programa")
        return False

    @visualizar_exec
    def cmd(self) -> bool:
        if not self.token:
            return False
        if self.token.tipo == "ID":
            print("entrei aqui")
            self.id()
            if self.token.lexema == "<-" and self.atribuicao():
                return True
            if self.token.lexema == "<<" and self.leitura():
                return True
        if self.token.lexema == "console" and self.escrita():
            return True

        if (
            self.token.lexema in ["int", "float", "boolean", "string"]
            and self.declarar()
        ):
            return True

        if self.token.lexema == "if" and self.cmd_if():
            return True
        self._erro("cmd")
        return False

    @visualizar_exec
    def declarar(self) -> bool:
        return self.tipo() and self.declarar_options()

    @visualizar_exec
    def declarar_options(self) -> bool:
        return (self.id() and self.match_l(";")) or self.atribuicao()

    @visualizar_exec
    def condicional(self) -> bool:
        if not self.token:
            self._erro("condicional")
            return False
        if (
            self.token.tipo == "ID"
            and self.expressao()
            and self.operador_relacional()
            and self.expressao()
            and self.condicional_linha()
        ):
            return True
        if (
            self.token.lexema == "!"
            and self.match_l("!")
            and self.expressao()
            and self.condicional_linha()
        ):
            return True

        self._erro("condicional")
        return False

    @visualizar_exec
    def condicional_linha(self) -> bool:
        if not self.token:
            self._erro("condicional_linha")
            return False

        if (
            self.token.tipo == "LOGIC_OP"
            and self.operador_logico()
            and self.condicional()
            and self.condicional_linha()
        ):
            return True

        if self.token.lexema in [")", "&&", "||", "!", ";"]:
            return True

        self._erro("condicional_linha")
        return False

    @visualizar_exec
    def expressao(self) -> bool:
        if self.exp_prioridade() and self.expressao_linha():
            return True
        self._erro("expressão")
        return False

    @visualizar_exec
    def expressao_linha(self) -> bool:
        if not self.token:
            return False
        if (
            self.token.lexema == "+"
            and self.match_l("+")
            and self.exp_prioridade()
            and self.expressao_linha()
        ):
            return True
        if (
            self.token.lexema == "-"
            and self.match_l("-")
            and self.exp_prioridade()
            and self.expressao_linha()
        ):
            return True
        if self.token.lexema in [
            ">",
            "<",
            ">=",
            "<=",
            "=",
            "!=",
            ")",
            "&&",
            "||",
            "!",
            ";",
        ]:
            return True

        self._erro("expressão_linha")
        return False

    @visualizar_exec
    def exp_prioridade(self) -> bool:
        if self.fator() and self.exp_prioridade_linha():
            return True
        self._erro("exp_prioridade")
        return False

    @visualizar_exec
    def exp_prioridade_linha(self) -> bool:
        if not self.token:
            self._erro("exp_prioridade_linha")
            return False
        if (
            self.token.lexema == "*"
            and self.match_l("*")
            and self.fator()
            and self.exp_prioridade_linha()
        ):
            return True
        if (
            self.token.lexema == r"/"
            and self.match_l(r"/")
            and self.fator()
            and self.exp_prioridade_linha()
        ):
            return True

        if self.token.lexema in [
            "+",
            "-",
            ">",
            "<",
            ">=",
            "<=",
            "=",
            "!=",
            ")",
            "&&",
            "||",
            "!",
            ";",
        ]:
            return True
        self._erro("exp_prioridade_linha")
        return False

    @visualizar_exec
    def fator(self) -> bool:
        if not self.token:
            self._erro("fator")
            return False
        if self.token.tipo == "ID" and self.id():
            return True
        if self.token.tipo in ["INTEGER", "FLOATING"] and self.num():
            return True
        # if
        self._erro("fator")
        return False

    @visualizar_exec
    def leitura(self) -> bool:
        if self.match_l("<<") and self.match_l("input") and self.match_l(";"):
            return True
        self._erro("leitura")
        return False

    @visualizar_exec
    def escrita(self) -> bool:
        if not self.token:
            self._erro("escrita")
            return False

        if (
            self.token.lexema == "console"
            and self.match_l("console")
            and self.match_l("<<")
            and self.escrita_options()
            and self.match_l(";")
        ):
            return True

        self._erro("escrita")
        return False

    @visualizar_exec
    def escrita_options(self) -> bool:
        if not self.token:
            self._erro("escrita_options")
            return False

        if self.token.tipo == "ID" and self.id():
            return True

        if self.token.tipo == "STRING" and self.texto_string():
            return True

        self._erro("escrita_options")
        return False

    @visualizar_exec
    def atribuicao(self) -> bool:
        if self.match_l("<-") and self.atribuicao_options() and self.match_l(";"):
            return True
        self._erro("atribuicao")
        return False

    @visualizar_exec
    def atribuicao_options(self) -> bool:
        if self.expressao() or self.texto_string():
            return True
        self._erro("atribuicao_options")
        return False

    @visualizar_exec
    def texto_string(self) -> bool:
        if self.match_t("STRING"):
            return True
        self._erro("texto_string")
        return False

    @visualizar_exec
    def operador_relacional(self) -> bool:
        if not self.token:
            self._erro("operador_relacional")
            return False
        if self.token.tipo == "RELACIONAL_OP":
            return self.match_t("RELACIONAL_OP")
        self._erro("operador_relacional")
        return False

    @visualizar_exec
    def tipo(self) -> bool:
        if not self.token:
            self._erro("tipo")
            return False
        if self.token.lexema == "int" and self.match_l("int"):
            return True
        if self.token.lexema == "float" and self.match_l("float"):
            return True
        if self.token.lexema == "boolean" and self.match_l("boolean"):
            return True
        if self.token.lexema == "string" and self.match_l("string"):
            return True
        self._erro("tipo")
        return False

    @visualizar_exec
    def operador_logico(self) -> bool:
        if not self.token:
            self._erro("operador_logico")
            return False
        if self.token.tipo == "LOGIC_OP" and self.match_t("LOGIC_OP"):
            return True

        self._erro("operador_logico")
        return False

    @visualizar_exec
    def num_int(self) -> bool:
        if self.match_t("INTEGER"):
            return True
        self._erro("num_int")
        return False

    @visualizar_exec
    def num_decimal(self) -> bool:
        if self.match_t("FLOATING"):
            return True
        self._erro("num_decimal")
        return False

    @visualizar_exec
    def loop_for(self) -> bool: ...

    @visualizar_exec
    def loop_while(self) -> bool: ...

    def match_l(self, lexema: str) -> bool:
        # print(f"{lexema= }")
        if self.token is not None and self.token.lexema == lexema:
            self.token = self.get_next_token()
            return True
        return False

    def match_t(self, tipo: str) -> bool:
        if not self.token:
            self._erro("match_t")
            return False
        if self.token.tipo == tipo:
            self.token = self.get_next_token()
            return True
        return False
