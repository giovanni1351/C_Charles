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

    def _erro(
        self,
        regra: str,
        message: str | None = None,
        *,
        exit_program: bool = True,
    ) -> None:
        print(f"Erro na {regra = }")
        if message:
            print(f"{message= }")
        print("Token invalido", self.token)
        print("----" * 10)
        if exit_program:
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
        if not self.token:
            self._erro("option_else", "token nulo")
            return False

        if (
            self.token.lexema == "else"
            and self.match_l("else")
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
            self._erro("bloco", "token nulo")
            return False

        if (
            (
                self.token.lexema
                in [
                    "console",
                    "if",
                    "int",
                    "float",
                    "boolean",
                    "string",
                    "for",
                    "while",
                ]
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
            self._erro("bloco_options", "token nulo")
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
                "for",
                "while",
            ]
            or self.token.tipo == "ID"
        ) and self.bloco():
            return True
        if self.token.lexema == "}":
            return True
        self._erro("bloco_options")
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
            self._erro("num", "token nulo")
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
            self._erro("programa", "token nulo")
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
            self._erro("cmd", "token nulo")
            return False
        if self.token.tipo == "ID":
            print("entrei aqui")
            self.id()
            if self.token.lexema == "<-" and self.atribuicao() and self.match_l(";"):
                return True
            if self.token.lexema == "<<" and self.leitura() and self.match_l(";"):
                return True
        if self.token.lexema == "console" and self.escrita() and self.match_l(";"):
            return True

        if (
            self.token.lexema in ["int", "float", "boolean", "string"]
            and self.declarar()
            and self.match_l(";")
        ):
            return True

        if self.token.lexema == "if" and self.cmd_if():
            return True

        if self.token.lexema == "for" and self.loop_for():
            print("entrou aqui")
            return True
        if self.token.lexema == "while" and self.loop_while():
            return True
        self._erro("cmd")
        return False

    @visualizar_exec
    def declarar(self) -> bool:
        if self.tipo() and self.declarar_options():
            return True
        self._erro("declarar", "regra não correta")
        return False

    @visualizar_exec
    def declarar_options(self) -> bool:
        if self.id() and self.declarar_options_linha():
            return True
        self._erro("declarar_options", "Regra incorreta, verifique a declaração")
        return False

    @visualizar_exec
    def declarar_options_linha(self) -> bool:
        if not self.token:
            self._erro("declarar_options_linha")
            return False

        if (
            self.token.lexema == "<-"
            and self.match_l("<-")
            and self.atribuicao_options()
        ):
            return True

        if self.token.lexema in [";"]:
            return True

        self._erro("declarar_options_linha")
        return False

    @visualizar_exec
    def condicional(self) -> bool:
        if not self.token:
            self._erro("condicional", "token nulo")
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
            self._erro("condicional_linha", "token nulo")
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
            self._erro("expressao_linha", "token nulo")
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
            self._erro("exp_prioridade_linha", "token nulo")
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
            self._erro("fator", "token nulo")
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
        if self.match_l("<<") and self.match_l("input"):
            return True
        self._erro("leitura")
        return False

    @visualizar_exec
    def escrita(self) -> bool:
        if not self.token:
            self._erro("escrita", "token nulo")
            return False

        if (
            self.token.lexema == "console"
            and self.match_l("console")
            and self.match_l("<<")
            and self.escrita_options()
        ):
            return True

        self._erro("escrita")
        return False

    @visualizar_exec
    def escrita_options(self) -> bool:
        if not self.token:
            self._erro("escrita_options", "token nulo")
            return False

        if self.token.tipo == "ID" and self.id():
            return True

        if self.token.tipo == "STRING" and self.texto_string():
            return True

        self._erro("escrita_options")
        return False

    @visualizar_exec
    def atribuicao(self) -> bool:
        if self.match_l("<-") and self.atribuicao_options():
            return True
        self._erro("atribuicao")
        return False

    @visualizar_exec
    def atribuicao_options(self) -> bool:
        if not self.token:
            self._erro("atribuicao_options")
            return False

        if (
            self.token.tipo in ["ID", "INTEGER", "FLOATING"] or self.token.lexema == "("
        ) and self.expressao():
            return True
        if self.token.tipo == "STRING" and self.texto_string():
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
            self._erro("operador_relacional", "token nulo")
            return False
        if self.token.tipo == "RELACIONAL_OP":
            return self.match_t("RELACIONAL_OP")
        self._erro("operador_relacional")
        return False

    @visualizar_exec
    def tipo(self) -> bool:
        if not self.token:
            self._erro("tipo", "token nulo")
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
            self._erro("operador_logico", "token nulo")
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
    def loop_for(self) -> bool:
        if not self.token:
            self._erro("loop_for", "token nulo")
            return False
        if (
            self.match_l("for")
            and self.match_l("(")
            and self.declarar()
            and self.match_l(";")
            and self.condicional()
            and self.match_l(";")
            and self.id()
            and self.atribuicao()
            and self.match_l(")")
            and self.match_l("->")
            and self.match_l("{")
            and self.bloco()
            and self.match_l("}")
        ):
            return True
        self._erro("loop_for", "Regra não correta")
        return False

    @visualizar_exec
    def loop_while(self) -> bool:
        if not self.token:
            self._erro("loop_while", "token nulo")
            return False
        if (
            self.match_l("while")
            and self.match_l("(")
            and self.condicional()
            and self.match_l(")")
            and self.match_l("->")
            and self.match_l("{")
            and self.bloco()
            and self.match_l("}")
        ):
            return True
        self._erro("loop_while")
        return False

    def match_l(self, lexema: str) -> bool:
        if self.token is not None and self.token.lexema == lexema:
            self.token = self.get_next_token()
            return True
        self._erro(
            "Token invalido",
            f"Esperado {lexema = } e encontrado {self.token} incorreto para a regra",
            exit_program=False,
        )
        return False

    def match_t(self, tipo: str) -> bool:
        if not self.token:
            self._erro("match_t", "token nulo")
            return False
        if self.token.tipo == tipo:
            self.token = self.get_next_token()
            return True
        self._erro(
            "Tipo invalido", f"{tipo = } incorreto para a regra", exit_program=False
        )
        return False
