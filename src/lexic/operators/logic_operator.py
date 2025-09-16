from typing import override

from lexic.afd import AFD
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class LogicOperator(AFD):
    @override
    def evaluate(self, code: CharacterIterator) -> Token | None:
        atual: str | None = code.current()

        match atual:
            case "<":
                next(code)
                if code.current() == "=":
                    next(code)
                    return Token("LOGIC_OP", "<=")
                if code.current() == "<":
                    next(code)
                    return Token("OUTPUT", "<<")
                return Token("LOGIC_OP", "<")

            case ">":
                next(code)
                if code.current() == "=":
                    next(code)
                    return Token("LOGIC_OP", ">=")
                return Token("LOGIC_OP", ">")

            case "&":
                next(code)
                if code.current() == "&":
                    next(code)
                    return Token("LOGIC_OP", "&&")
                return Token("LOGIC_OP", "&")

            case "=":
                next(code)
                return Token("LOGIC_OP", "=")
            case "!":
                next(code)
                return Token("LOGIC_OP", "!")

            case None:
                return Token("EOF", "$")
            case _:
                return None
