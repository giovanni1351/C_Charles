import sys
from typing import TYPE_CHECKING

from rich import print  # noqa: A004

from lexic.lexer import Lexer
from lexic.parser import Parser

if TYPE_CHECKING:
    from lexic.token_lexico import Token


class Main:
    def __init__(self) -> None:
        with open(sys.argv[1], encoding="utf-8") as arquivo:
            code = arquivo.read()
            lexer: Lexer = Lexer(code)
            tokens: list[Token] = lexer.get_token()
            parser = Parser(tokens)
            arvore = parser.main()
            arvore.print_tree()
            arvore.print_code(node=None, declaracoes=parser.declaracoes)
            print(parser.id_hash_table)


if __name__ == "__main__":
    Main()
