from rich import print  # noqa: A004

from lexic.lexer import Lexer
from lexic.token_lexico import Token


class Main:
    def __init__(self) -> None:
        code: str = "+++---***////;;; teste teste1 teste2* 12213 12 23 21 232"
        lexer: Lexer = Lexer(code)
        tokens: list[Token] = lexer.get_token()
        for token in tokens:
            print(token)


if __name__ == "__main__":
    Main()
