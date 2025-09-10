from typing import TYPE_CHECKING

from rich import print  # noqa: A004

from lexic.lexer import Lexer

if TYPE_CHECKING:
    from lexic.token_lexico import Token


class Main:
    def __init__(self) -> None:
        code: str = "+++---***////;;; teste teste1 teste2* 12213i12a23b21 232 string float int for while if else else if input console"
        lexer: Lexer = Lexer(code)
        tokens: list[Token] = lexer.get_token()
        for token in tokens:
            print(token)


if __name__ == "__main__":
    Main()
