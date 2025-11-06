from typing import overload

from lexic.token_lexico import Token


class Node:
    def __init__(
        self, nome: str, token: Token | None = None, pai: "Node| None" = None
    ) -> None:
        self.nome = nome
        self.nodes: list[Node] = []
        self.token = token
        self.enter = ""
        self.exit = ""
        self.pai = pai

    @overload
    def add_node(
        self,
        *,
        new_node: "Node | None" = None,
        node_name: None = None,
        enter: str | None = None,
        exit_: str | None = None,
        token: Token | None = None,
    ) -> "None": ...

    @overload
    def add_node(
        self,
        *,
        new_node: "Node | None" = None,
        node_name: str,
        enter: str | None = None,
        exit_: str | None = None,
        token: Token | None = None,
    ) -> "Node": ...

    def add_node(
        self,
        *,
        new_node: "Node | None" = None,
        node_name: str | None = None,
        enter: str | None = None,
        exit_: str | None = None,
        token: Token | None = None,
    ) -> "None | Node ":
        if isinstance(new_node, Node):
            new_node.pai = self
            self.nodes.append(new_node)
            return None

        if (
            isinstance(enter, str)
            and isinstance(exit_, str)
            and isinstance(node_name, str)
        ):
            node_novo = Node(node_name, token=token, pai=self)
            node_novo.enter = enter
            node_novo.exit = exit_
            self.nodes.append(node_novo)
            return node_novo

        if isinstance(node_name, str):
            node_novo = Node(node_name, token=token, pai=self)
            self.nodes.append(node_novo)
            return node_novo
        return None

    def get_tree(self) -> str:
        buffer: list[str] = []
        self.printar(buffer, "", "")

        return "".join(buffer)

    def printar(self, buffer: list[str], prefix: str, children_prefix: str) -> None:
        buffer.append(prefix)
        buffer.append(f"{self.nome} {self.token if self.token else ''}")
        buffer.append("\n")
        for i, node in enumerate(self.nodes):
            if i == len(self.nodes):
                node.printar(buffer, children_prefix + "`-- ", children_prefix + "   ")
            else:
                node.printar(buffer, children_prefix + "+---", children_prefix + "|  ")
