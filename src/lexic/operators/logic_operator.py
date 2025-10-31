from typing import override

from lexic.afd import AFD
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class LogicOperator(AFD):
    @override
    def evaluate(self, code: CharacterIterator) -> Token | None:  # noqa: C901
        atual: str | None = code.current()

        match atual:
            case "<":
                next(code)
                if code.current() == "=":
                    next(code)
                    return Token("RELACIONAL_OP", "<=")
                if code.current() == "<":
                    next(code)
                    return Token("OUTPUT", "<<")
                if code.current() == "-":
                    next(code)
                    return Token("ATRIBUICAO", "<-")
                return Token("RELACIONAL_OP", "<")

            case ">":
                next(code)
                if code.current() == "=":
                    next(code)
                    return Token("RELACIONAL_OP", ">=")
                return Token("RELACIONAL_OP", ">")

            case "&":
                next(code)
                if code.current() == "&":
                    next(code)
                    return Token("LOGIC_OP", "&&")
                return Token("LOGIC_OP", "&")

            case "=":
                next(code)
                return Token("RELACIONAL_OP", "=")
            case "!":
                next(code)
                if code.current() == "=":
                    next(code)
                    return Token("RELACIONAL_OP", "!=")
                return Token("LOGIC_OP", "!")

            case None:
                return Token("EOF", "$")
            case _:
                return None
