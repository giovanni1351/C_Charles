from typing import override

from lexic.afd import AFD
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class BracketsOperator(AFD):
    @override
    def evaluate(self, code: CharacterIterator) -> Token | None:
        atual: str | None = code.current()
        if atual is None:
            return Token("EOF", "$")
        match atual:
            case "(":
                next(code)
                return Token("PARENTHESIS", "(")

            case ")":
                next(code)
                return Token("PARENTHESIS", ")")

            case "{":
                next(code)
                return Token("CURLY_BRACKET", "{")
            case "}":
                next(code)
                return Token("CURLY_BRACKET", "}")
            case "[":
                next(code)
                return Token("SQUARE_BRACKET", "[")
            case "]":
                next(code)
                return Token("SQUARE_BRACKET", "]")
            case "-":
                next(code)
                if code.current() == ">":
                    next(code)
                    return Token("START_BLOCK", "->")
                return Token("LOGIC_OP", "-")
            case _:
                return None
