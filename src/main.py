import os
import sys
from typing import TYPE_CHECKING

from lexic.lexer import Lexer
from lexic.parser import Parser, ParserError

if TYPE_CHECKING:
    from lexic.token_lexico import Token


class Main:
    def __init__(self) -> None:
        with open(sys.argv[1], encoding="utf-8") as arquivo:
            code = arquivo.read()
            lexer: Lexer = Lexer(code)
            tokens: list[Token] = lexer.get_token()
            parser = Parser(tokens)
            try:
                arvore = parser.main()
            except ParserError as error:
                print(f"Ocorreu um erro de parsing {error}")
                exit()
            arvore.print_tree()
            arvore.print_code(node=None, declaracoes=parser.declaracoes)
            if "--no-fpc" in sys.argv:
                return
            with open("traducao.pas", "w") as file:
                file.write(arvore.traducao)
            os.system("fpc traducao.pas")  # noqa: S605, S607
            os.remove("traducao.pas")
            try:
                if "--limpo" in sys.argv:
                    os.system("cls")
            except:
                ...
            os.system("traducao.exe")  # noqa: S605, S607
            try:
                os.remove("traducao.exe")
            except FileNotFoundError:
                print("Erro na compilação do código, provavelmente um erro semantico!")
                exit()
            os.remove("traducao.o")


if __name__ == "__main__":
    Main()
