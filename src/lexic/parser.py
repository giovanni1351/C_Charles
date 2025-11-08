from collections.abc import Callable
from functools import wraps

from lexic.node import Node
from lexic.token_lexico import Token
from lexic.tree import Tree


class ParserError(Exception): ...


def visualizar_exec[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """Decorador que mede o tempo de execução de uma função."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        retorno = func(*args, **kwargs)
        if retorno:
            # print(f"Sucesso {func.__name__}")
            ...
        else:
            print(f"F total {func.__name__}")
        return retorno

    return wrapper


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.token: Token | None
        self.id_hash_table: dict[str, int] = {}
        self.declaracoes: list[Node] = list[Node]()

    def main(self) -> Tree:
        self.token = self.get_next_token()
        node_raiz = Node("programa")
        arvore = Tree(node_raiz)
        try:
            if self.programa(node_raiz) and (self.token is None or self.match_t("EOF")):
                print("Sintaticamente correto")
            else:
                self._erro("main")
        except ParserError as error:
            print(
                f"Ocorreu um erro de parsing, verifique se a sintaxe está correta!\nErro: {error}"
            )
        return arvore

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
        msg = f"{regra}: {message}"
        raise ParserError(msg)

    @visualizar_exec
    def cmd_if(self, node: Node) -> bool:
        node_cmd_if = node.add_node(node_name="cmd_if")
        if (
            self.match_l("if", node=node_cmd_if)
            and self.match_l("(")
            and self.condicional(node=node_cmd_if)
            and self.match_l(")")
            and self.match_l("->", node=node_cmd_if)
            and self.match_l("{")
            and self.bloco(node=node_cmd_if)
            and self.match_l("}")
            and self.option_else(node=node_cmd_if)
        ):
            return True
        self._erro("cmd_if")
        return False

    @visualizar_exec
    def option_else(self, node: Node) -> bool:
        if not self.token:
            self._erro("option_else", "token nulo")
            return False
        node_option_else = node
        if self.token.lexema == "else":
            node_option_else = node.add_node(node_name="option_else")

        if (
            self.token.lexema == "else"
            and self.match_l("else", node=node_option_else)
            and self.match_l("->")
            and self.match_l("{")
            and self.bloco(node_option_else)
            and self.match_l("}")
        ):
            return True
        return True

    @visualizar_exec
    def bloco(self, node: Node) -> bool:
        if node.nome != "bloco":
            node_bloco = node.add_node(
                node_name="bloco", enter="\nbegin\n", exit_="\nend\n"
            )
        else:
            node_bloco = node
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
            and self.cmd(node=node_bloco)
            and self.bloco_options(node=node_bloco)
        ):
            return True
        self._erro("bloco")
        return False

    @visualizar_exec
    def bloco_options(self, node: Node) -> bool:
        # node_bloco_options = node.add_node(node_name="bloco_options")
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
        ) and self.bloco(node):
            return True
        if self.token.lexema == "}":
            return True
        self._erro("bloco_options")
        return False

    @visualizar_exec
    def id(self, node: Node) -> bool:
        node_id = node.add_node(node_name="id")
        if not self.token:
            self._erro("id")
            return False
        lexema = self.token.lexema
        if self.match_t("ID", node_id):
            if self.id_hash_table.get(lexema, None) is not None:
                self.id_hash_table[lexema] += 1
            else:
                self.id_hash_table[lexema] = 1
            return True
        self._erro("id")
        return False

    @visualizar_exec
    def num(self, node: Node) -> bool:
        node_num = node.add_node(node_name="num")
        if not self.token:
            self._erro("num", "token nulo")
            return False
        if self.token.tipo == "INTEGER" and self.num_int(node_num):
            return True

        if self.token.tipo == "FLOATING" and self.num_decimal(node_num):
            return True

        self._erro("num")
        return False

    @visualizar_exec
    def programa(self, node: Node) -> bool:
        node_programa = node.add_node(node_name="programa")
        if not self.token:
            self._erro("programa", "token nulo")
            return False
        if self.token.lexema in ["int", "float", "boolean", "string"]:
            return bool(
                self.tipo(node=node_programa)  # pyright: ignore[reportUnknownArgumentType]
                and self.match_l("charles")
                and self.match_l("(")
                and self.match_l(")")
                and self.match_l("->")
                and self.match_l("{")
                and self.bloco(node=node_programa)
                and self.match_l("}")
            )
        self._erro("programa")
        return False

    @visualizar_exec
    def cmd(self, node: Node) -> bool:
        node_cmd = node.add_node(node_name="cmd")
        if not self.token:
            self._erro("cmd", "token nulo")
            return False
        if self.token.tipo == "ID":
            self.id(node_cmd)
            if (
                self.token.lexema == "<-"
                and self.atribuicao(node_cmd)
                and self.match_l(";")
            ):
                return True
            if (
                self.token.lexema == "<<"
                and self.leitura(node_cmd)
                and self.match_l(";")
            ):
                return True
        if (
            self.token.lexema == "console"
            and self.escrita(node_cmd)
            and self.match_l(";")
        ):
            return True

        if (
            self.token.lexema in ["int", "float", "boolean", "string"]
            and self.declarar(node_cmd)
            and self.match_l(";")
        ):
            return True

        if self.token.lexema == "if" and self.cmd_if(node_cmd):
            return True

        if self.token.lexema == "for" and self.loop_for(node_cmd):
            return True
        if self.token.lexema == "while" and self.loop_while(node_cmd):
            return True
        self._erro("cmd")
        return False

    @visualizar_exec
    def declarar(self, node: Node) -> bool:
        node_declarar = node.add_node(node_name="declarar")
        if self.tipo(node_declarar) and self.declarar_options(node_declarar):
            self.declaracoes.append(node_declarar)
            return True
        self._erro("declarar", "regra não correta")
        return False

    @visualizar_exec
    def declarar_options(self, node: Node) -> bool:
        # node_declarar_options = node.add_node(node_name="declarar_options")
        if self.id(node) and self.declarar_options_linha(node):
            return True
        self._erro("declarar_options", "Regra incorreta, verifique a declaração")
        return False

    @visualizar_exec
    def declarar_options_linha(self, node: Node) -> bool:
        # node_declarar_options_linha = node.add_node(node_name="declarar_options_linha")  # noqa: E501
        if not self.token:
            self._erro("declarar_options_linha")
            return False

        if (
            self.token.lexema == "<-"
            and self.match_l("<-")
            and self.atribuicao_options(node=node)
        ):
            return True

        if self.token.lexema in [";"]:
            return True

        self._erro("declarar_options_linha")
        return False

    @visualizar_exec
    def condicional(self, node: Node) -> bool:
        node_condicional = node.add_node(node_name="condicional")
        if not self.token:
            self._erro("condicional", "token nulo")
            return False
        if (
            self.token.tipo == "ID"
            and self.expressao(node_condicional)
            and self.operador_relacional(node_condicional)
            and self.expressao(node_condicional)
            and self.condicional_linha(node_condicional)
        ):
            return True
        if (
            self.token.lexema == "!"
            and self.match_l("!", node=node_condicional)
            and self.expressao(node_condicional)
            and self.condicional_linha(node_condicional)
        ):
            return True

        self._erro("condicional")
        return False

    @visualizar_exec
    def condicional_linha(self, node: Node) -> bool:
        # node_condicional_linha = node.add_node(node_name="condicional_linha")
        if not self.token:
            self._erro("condicional_linha", "token nulo")
            return False

        if (
            self.token.tipo == "LOGIC_OP"
            and self.operador_logico(node)
            and self.condicional(node)
            and self.condicional_linha(node)
        ):
            return True

        if self.token.lexema in [")", "&&", "||", "!", ";"]:
            return True

        self._erro("condicional_linha")
        return False

    @visualizar_exec
    def expressao(self, node: Node) -> bool:
        node_expressao = node.add_node(node_name="expressao")
        if self.exp_prioridade(node_expressao) and self.expressao_linha(node_expressao):
            return True
        self._erro("expressão")
        return False

    @visualizar_exec
    def expressao_linha(self, node: Node) -> bool:
        # node_expressao_linha = node.add_node(node_name="expressao_linha")
        if not self.token:
            self._erro("expressao_linha", "token nulo")
            return False
        if (
            self.token.lexema == "+"
            and self.match_l("+", node=node)
            and self.exp_prioridade(node)
            and self.expressao_linha(node)
        ):
            return True
        if (
            self.token.lexema == "-"
            and self.match_l("-", node=node)
            and self.exp_prioridade(node)
            and self.expressao_linha(node)
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
            "&",
            "|",
            "!",
            ";",
        ]:
            return True

        self._erro("expressão_linha")
        return False

    @visualizar_exec
    def exp_prioridade(self, node: Node) -> bool:
        # node_exp_prioridade = node.add_node(node_name="exp_prioridade")
        if self.fator(node) and self.exp_prioridade_linha(node):
            return True
        self._erro("exp_prioridade")
        return False

    @visualizar_exec
    def exp_prioridade_linha(self, node: Node) -> bool:
        # node_exp_prioridade_linha = node.add_node(node_name="exp_prioridade_linha")
        if not self.token:
            self._erro("exp_prioridade_linha", "token nulo")
            return False
        if (
            self.token.lexema == "*"
            and self.match_l("*", node=node)
            and self.fator(node)
            and self.exp_prioridade_linha(node)
        ):
            return True
        if (
            self.token.lexema == r"/"
            and self.match_l(r"/", node=node)
            and self.fator(node)
            and self.exp_prioridade_linha(node)
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
            "&",
            "||",
            "|",
            "!",
            ";",
        ]:
            return True
        self._erro("exp_prioridade_linha")
        return False

    @visualizar_exec
    def fator(self, node: Node) -> bool:
        # node_fator = node.add_node(node_name="fator")
        if not self.token:
            self._erro("fator", "token nulo")
            return False
        if self.token.tipo == "ID" and self.id(node):
            return True
        if (
            self.token.lexema == "("
            and self.match_l("(", node=node)
            and self.expressao(node)
            and self.match_l(")", node=node)
        ):
            return True
        if self.token.tipo in ["INTEGER", "FLOATING"] and self.num(node):
            return True
        # if
        self._erro("fator")
        return False

    @visualizar_exec
    def leitura(self, node: Node) -> bool:
        node.add_node(
            node_name="leitura",
            enter=f"\nreadln({node.nodes[0].nodes[0].nome}",
            exit_=");\n",
        )
        if self.match_l("<<") and self.match_l("input"):
            return True
        self._erro("leitura")
        return False

    @visualizar_exec
    def escrita(self, node: Node) -> bool:
        node_escrita = node.add_node(
            node_name="escrita", enter="\nwriteln(", exit_=");\n"
        )
        if not self.token:
            self._erro("escrita", "token nulo")
            return False

        if (
            self.token.lexema == "console"
            and self.match_l("console")
            and self.match_l("<<")
            and self.escrita_options(node_escrita)
        ):
            return True

        self._erro("escrita")
        return False

    @visualizar_exec
    def escrita_options(self, node: Node) -> bool:
        # node_escrita_options = node.add_node(node_name="escrita_options")
        if not self.token:
            self._erro("escrita_options", "token nulo")
            return False

        if self.token.tipo == "ID" and self.id(node):
            return True

        if self.token.tipo == "STRING" and self.texto_string(node):
            return True

        self._erro("escrita_options")
        return False

    @visualizar_exec
    def atribuicao(self, node: Node) -> bool:
        node_atribuicao = node.add_node(node_name="atribuicao", enter=":=")
        if self.match_l("<-") and self.atribuicao_options(node_atribuicao):
            return True
        self._erro("atribuicao")
        return False

    @visualizar_exec
    def atribuicao_options(self, node: Node) -> bool:
        # node_atribuicao_options = node.add_node(
        #     node_name="atribuicao_options", enter=":="
        # )
        if not self.token:
            self._erro("atribuicao_options")
            return False

        if (
            self.token.tipo in ["ID", "INTEGER", "FLOATING"] or self.token.lexema == "("
        ) and self.expressao(node):
            return True
        if self.token.tipo == "STRING" and self.texto_string(node):
            return True
        self._erro("atribuicao_options")
        return False

    @visualizar_exec
    def texto_string(self, node: Node) -> bool:
        node_texto_string = node.add_node(
            node_name="texto_string", enter="'", exit_="'"
        )
        if self.match_t("STRING", node=node_texto_string):
            # node_texto_string.nodes[0].token.lexema.replace('"', "'")
            return True
        self._erro("texto_string")
        return False

    @visualizar_exec
    def operador_relacional(self, node: Node) -> bool:
        node_operador_relacional = node.add_node(node_name="operador_relacional")
        if not self.token:
            self._erro("operador_relacional", "token nulo")
            return False
        if self.token.tipo == "RELACIONAL_OP":
            return self.match_t("RELACIONAL_OP", node=node_operador_relacional)
        self._erro("operador_relacional")
        return False

    @visualizar_exec
    def tipo(self, node: Node) -> bool:
        node_tipo = node.add_node(node_name="tipo")
        if not self.token:
            self._erro("tipo", "token nulo")
            return False
        if self.token.lexema == "int" and self.match_l("int", node=node_tipo):
            return True
        if self.token.lexema == "float" and self.match_l("float", node=node_tipo):
            return True
        if self.token.lexema == "boolean" and self.match_l("boolean", node=node_tipo):
            return True
        if self.token.lexema == "string" and self.match_l("string", node=node_tipo):
            return True
        self._erro("tipo")
        return False

    @visualizar_exec
    def operador_logico(self, node: Node) -> bool:
        node_operador_logico = node.add_node(node_name="operador_logico")
        if not self.token:
            self._erro("operador_logico", "token nulo")
            return False
        if self.token.tipo == "LOGIC_OP" and self.match_t(
            "LOGIC_OP", node=node_operador_logico
        ):
            return True

        self._erro("operador_logico")
        return False

    @visualizar_exec
    def num_int(self, node: Node) -> bool:
        # node_num_int = node.add_node(node_name="num_int")
        if self.match_t("INTEGER", node=node):
            return True
        self._erro("num_int")
        return False

    @visualizar_exec
    def num_decimal(self, node: Node) -> bool:
        # node_num_decimal = node.add_node(node_name="num_decimal")
        if self.match_t("FLOATING", node=node):
            return True
        self._erro("num_decimal")
        return False

    @visualizar_exec
    def loop_for(self, node: Node) -> bool:
        node_loop_for = node.add_node(node_name="loop_for")
        if not self.token:
            self._erro("loop_for", "token nulo")
            return False
        if (
            self.match_l("for")
            and self.match_l("(")
            and self.declarar(node_loop_for)
            and self.match_l(";")
            and self.condicional(node_loop_for)
            and self.match_l(";")
            and self.id(node_loop_for)
            and self.atribuicao(node_loop_for)
            and self.match_l(")")
            and self.match_l("->")
            and self.match_l("{")
            and self.bloco(node_loop_for)
            and self.match_l("}")
        ):
            return True
        self._erro("loop_for", "Regra não correta")
        return False

    @visualizar_exec
    def loop_while(self, node: Node) -> bool:
        node_loop_while = node.add_node(node_name="loop_while")
        if not self.token:
            self._erro("loop_while", "token nulo")
            return False
        if (
            self.match_l("while", node=node_loop_while)
            and self.match_l("(")
            and self.condicional(node_loop_while)
            and self.match_l(")")
            and self.match_l("->")
            and self.match_l("{")
            and self.bloco(node_loop_while)
            and self.match_l("}")
        ):
            return True
        self._erro("loop_while")
        return False

    def traduz(self, texto: str) -> None:
        print(texto, end="")

    def match_l(self, lexema: str, *, node: Node | None = None) -> bool:
        if self.token is not None and self.token.lexema == lexema:
            if node is not None:
                node.add_node(node_name=self.token.lexema, token=self.token)
            self.token = self.get_next_token()
            return True
        self._erro(
            "Token invalido",
            f"Esperado {lexema = } e encontrado {self.token} incorreto para a regra",
            exit_program=False,
        )
        return False

    def match_t(self, tipo: str, node: Node | None = None) -> bool:
        if not self.token:
            self._erro("match_t", "token nulo")
            return False
        if self.token.tipo == tipo:
            if node is not None:
                node.add_node(node_name=self.token.lexema, token=self.token)
            self.token = self.get_next_token()
            return True
        self._erro(
            "Tipo invalido", f"{tipo = } incorreto para a regra", exit_program=False
        )
        return False
