from lexic.depara import depara
from lexic.node import Node


class Tree:
    def __init__(self, root: Node | None = None) -> None:
        self.traducao: str = ""
        self.reserved_types = [
            "EOF",
            "PARENTHESIS",
            "CURLY_BRACKET",
            "SQUARE_BRACKET",
            "START_BLOCK",
            "LOGIC_OP",
            "END_LINE",
            "FLOATING",
            "ID",
            "INTEGER",
            "RESERVED",
            "OUTPUT",
            "ATRIBUICAO",
            "RELACIONAL_OP",
            "MATH_OP",
            "STRING",
        ]
        if root is not None:
            self.root = root

    def set_root(self, node: Node) -> None:
        self.root = node

    def pre_order(self, node: Node | None = None) -> None:
        if node is None:
            self.pre_order(self.root)
            return
        for n in node.nodes:
            self.pre_order(n)

    def print_code(  # noqa: C901
        self, node: Node | None = None, declaracoes: list[Node] | None = None
    ) -> None:
        if node is None:
            self.traducao += "program charles;\n"
            if declaracoes is not None:
                variaveis = set[tuple[str, str]]()
                for declaracao in declaracoes:
                    variaveis.add(
                        (
                            declaracao.nodes[1].nodes[0].nome,
                            declaracao.nodes[0].nodes[0].nome,
                        )
                    )
                if variaveis:
                    self.traducao += "var\n"
                    for identificador, tipo in variaveis:
                        self.traducao += f"    {identificador}: {depara[tipo]};\n"
            self.print_code(self.root)
            self.traducao += "\n"
            print(self.traducao)
            return

        if node.pai and node.nome == "tipo" and node.pai.nome == "programa":
            return

        self.traducao += node.enter

        if (
            node.nome == "cmd"
            and node.nodes[0].nome == "id"
            and node.nodes[1].nome == "atribuicao"
        ):
            self.traducao += node.nodes[0].nodes[0].nome + ":="
            self.print_code(node.nodes[1])
            self.traducao += ";\n"
            return
        if (
            node.nome == "cmd"
            and node.nodes[0].nome == "id"
            and node.nodes[1].nome == "leitura"
        ):
            self.traducao += f"readln({node.nodes[0].nodes[0].nome});\n"
            return
        if node.nome == "declarar":
            self.declarar(node)
            return
        if node.nome == "%":
            self.traducao += " mod "
            return
        if node.nome == "!=":
            self.traducao += " <> "
            return
        if node.nome == "&&" or node.nome == "&":
            self.traducao += ") and ("
            return
        if node.nome == "||" or node.nome == "|":
            self.traducao += ") or ("
            return
        if node.nome == "loop_while":
            self.traducao += "while "
            self.print_code(node.nodes[1])
            self.traducao += " do\n "
            self.print_code(node.nodes[2])
            self.traducao += ";\n"
            return
        if node.nome == "loop_for":
            self.declarar(node.nodes[0])
            self.traducao += " while "
            self.print_code(node.nodes[1])
            self.traducao += " do "
            cmd = Node("cmd")
            cmd.add_node(new_node=node.nodes[2])
            cmd.add_node(new_node=node.nodes[3])
            node.nodes[4].add_node(new_node=cmd)
            self.print_code(node.nodes[4])
            self.traducao += ";\n"
            return
        if node.nome == "cmd_if":
            self.traducao += "if ("
            self.print_code(node.nodes[1])
            self.traducao += ") then "
            self.print_code(node.nodes[3])
            if len(node.nodes) == 5:
                self.print_code(node.nodes[4])
            self.traducao += ";\n"
            return
        if len(node.nodes) == 0:
            if (
                node.nome not in self.reserved_types
                and node.token
                and node.token.tipo == "STRING"
            ):
                self.traducao += node.nome[1:-1].replace("\n", "\\n")

            elif node.token and not depara.get(node.token.lexema):
                self.traducao += node.token.lexema
            elif node.token and depara.get(node.token.lexema):
                self.traducao += depara[node.token.lexema]

        for n in node.nodes:
            self.print_code(n)
        self.traducao += node.exit
        if node.nome == "bloco":
            if node.pai and node.pai.nome == "programa":
                self.traducao += "."
            else:
                # self.traducao += ";"
                ...

    def print_tree(self) -> None:
        print(self.root.get_tree())

    def declarar(self, node: Node) -> None:
        if len(node.nodes) == 2:
            return
        if len(node.nodes) == 3:
            self.print_code(node.nodes[1])
            self.traducao += ":= "
            self.print_code(node.nodes[2])
            self.traducao += ";\n"
            return
