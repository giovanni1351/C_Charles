import sys
from typing import TYPE_CHECKING

from rich import print  # noqa: A004

from lexic.lexer import Lexer
from lexic.parser import Parser

if TYPE_CHECKING:
    from lexic.token_lexico import Token


class Main:
    def __init__(self) -> None:
        # code: str = """
        # +++---***////;;; teste teste1 teste2* 12213i12a23b21
        # 232 string float int for while if else else if input console
        # << >>
        # > <= %
        # >= <=

        # ) ( ) }  { } {} [] ]]]] ->
        # """
        with open(sys.argv[1], encoding="utf-8") as arquivo:
            code = arquivo.read()
            print(code)
            lexer: Lexer = Lexer(code)
            tokens: list[Token] = lexer.get_token()
            for token in tokens:
                print(token)
            parser = Parser(tokens)
            arvore = parser.main()
            arvore.print_tree()
            arvore.print_code()
            print(parser.id_hash_table)


if __name__ == "__main__":
    Main()
