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

    def print_code(self, node: Node | None = None) -> None:
        if node is None:
            self.print_code(self.root)
            print()
            return
        print(node.enter)
        if len(node.nodes) == 0:
            print(node)

        for n in node.nodes:
            self.print_code(n)
        print(node.exit)

    def print_tree(self) -> None:
        print(self.root.get_tree())
