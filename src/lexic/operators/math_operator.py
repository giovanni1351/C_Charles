from typing import override

from lexic.afd import AFD
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class MathOperator(AFD):
    @override
    def evaluate(self, code: CharacterIterator) -> Token | None:
        atual = code.current()

        match atual:
            case "+":
                next(code)
                return Token("PLUS", "+")
            case "-":
                next(code)
                return Token("MINUS", "-")

            case "*":
                next(code)
                return Token("TIMES", "*")

            case "/":
                next(code)
                return Token("DIVIDE", "/")

            case None:
                return Token("EOF", "$")
            case _:
                return None
