from rich import print  # noqa: A004

from lexic.lexer import Lexer
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class Main:
    def __init__(self) -> None:
        identifier: Token = Token("ID", "Resultado")
        num = Token("NUM", "3")
        print(identifier)
        print(num)

        code: str = "+++"
        lexer: Lexer = Lexer(code)
        tokens: list[Token] = lexer.get_token()
        for token in tokens:
            print(token)


if __name__ == "__main__":
    Main()
    exemplo = "asdasdsadas"
    iterador = CharacterIterator(exemplo)
