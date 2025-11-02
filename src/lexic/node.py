class Node:
    def __init__(self, nome: str) -> None:
        self.nome = nome
        self.nodes: list[Node] = []
        self.enter = ""
        self.exit = ""

    def add_node(
        self,
        *,
        new_node: "Node | None" = None,
        node_name: str | None = None,
        enter: str | None = None,
        exit_: str | None = None,
    ) -> "None | Node":
        if isinstance(new_node, Node):
            print("IOPAAA")
            self.nodes.append(new_node)
            return None

        if (
            isinstance(enter, str)
            and isinstance(exit_, str)
            and isinstance(node_name, str)
        ):
            node_novo = Node(node_name)
            node_novo.enter = enter
            node_novo.exit = exit_
            self.nodes.append(node_novo)
            return node_novo

        if isinstance(node_name, str):
            node_novo = Node(node_name)
            self.nodes.append(node_novo)
            return node_novo
        return None

    def get_tree(self) -> list[str]:
        print("AST")
        buffer: list[str] = []
        self.printar(buffer, "", "")

        return buffer

    def printar(self, buffer: list[str], prefix: str, children_prefix: str) -> None:
        buffer.append(prefix)
        buffer.append(f"| {self.nome} |")
        buffer.append("\n")
        for node in self.nodes:
            node.printar(buffer, children_prefix + "|___", children_prefix + "|   ")


if __name__ == "__main__":
    nodes = [Node(str(a)) for a in range(1, 10)]
    node_pai = Node("pai")
    for node in nodes:
        node_pai.add_node(new_node=node)
        nodes_filhos = (
            Node(str(a)) for a in range(int(node.nome) * 10, int(node.nome) * 10 + 10)
        )
        for node_filho in nodes_filhos:
            node.add_node(new_node=node_filho)
    print("".join(node_pai.get_tree()))
