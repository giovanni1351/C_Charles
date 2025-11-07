from lexic.depara import depara
from lexic.node import Node


class Tree:
    def __init__(self, root: Node | None = None) -> None:
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

    def print_code(
        self, node: Node | None = None, declaracoes: list[Node] | None = None
    ) -> None:
        if node is None:
            print("program charles;\n")
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
                    print("var\n")
                    for identificador, tipo in variaveis:
                        print(f"    {identificador}: {depara[tipo]};")
            self.print_code(self.root)
            print()
            return

        if node.pai and node.nome == "tipo" and node.pai.nome == "programa":
            return

        print(
            # "entrada,",
            node.enter,
            end="",
        )
        if (
            node.nome == "cmd"
            and node.nodes[0].nome == "id"
            and node.nodes[1].nome == "atribuicao"
        ):
            print(node.nodes[0].nodes[0].nome, ":=", end="")
            self.print_code(node.nodes[1])
            print(";", end="")
            return
        if (
            node.nome == "cmd"
            and node.nodes[0].nome == "id"
            and node.nodes[1].nome == "leitura"
        ):
            print("")
            return
        if node.nome == "declarar":
            self.declarar(node)
            return
        if node.nome == "loop_for":
            self.declarar(node.nodes[0])
            print("while ", end="")
            self.print_code(node.nodes[1])
            print("do")
            cmd = Node("cmd")
            cmd.add_node(new_node=node.nodes[2])
            cmd.add_node(new_node=node.nodes[3])
            node.nodes[4].add_node(new_node=cmd)
            self.print_code(node.nodes[4])
            return

        if len(node.nodes) == 0:
            if (
                node.nome not in self.reserved_types
                and node.token
                and node.token.tipo == "STRING"
            ):
                print(node.nome[1:-1].replace("\n", "\\n"), end="")

            elif node.token and not depara.get(node.token.lexema):
                print(node.token.lexema, end=" ")
            elif node.token and depara.get(node.token.lexema):
                print(depara[node.token.lexema], end=" ")

        for n in node.nodes:
            self.print_code(n)
        print(
            # "saida,",
            node.exit,
            end="",
        )
        if node.pai and node.pai.nome == "programa" and node.nome == "bloco":
            print(".", end="")

    def print_tree(self) -> None:
        print(self.root.get_tree())

    def declarar(self, node: Node) -> None:
        if len(node.nodes) == 2:
            return
        if len(node.nodes) == 3:
            self.print_code(node.nodes[1])
            print(":= ", end="")
            self.print_code(node.nodes[2])
            print(";")
            return
