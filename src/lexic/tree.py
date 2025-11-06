from lexic.node import Node


class Tree:
    def __init__(self, root: Node | None = None) -> None:
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
            if declaracoes is not None:
                print("vars")
                for declaracao in declaracoes:
                    print(
                        f"    {declaracao.nodes[1].nodes[0].nome}: "
                        f"{declaracao.nodes[0].nodes[0].nome};"
                    )
            self.print_code(self.root)
            print()
            return
        print(node.enter, end="")
        if len(node.nodes) == 0:
            if node.token:
                # print(node.nome, end=" ")
                print(node.token.lexema, end=" ")

        for n in node.nodes:
            self.print_code(n)
        print(node.exit, end="")

    def print_tree(self) -> None:
        print(self.root.get_tree())
