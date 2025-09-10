from typing import cast

from lexic.afd import AFD
from lexic.operators.decimal_operator import DecimalOperator
from lexic.operators.end_line_operator import EndLineOperator
from lexic.operators.identifier_operator import IdentifierOperator
from lexic.operators.math_operator import MathOperator
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class Lexer:
    afds: list[AFD]
    tokens: list[Token]
    code: CharacterIterator

    def __init__(self, code: str) -> None:
        self.code = CharacterIterator(code)
        self.afds = []
        self.tokens = []
        self.afds = [
            MathOperator(),
            DecimalOperator(),
            IdentifierOperator(),
            EndLineOperator(),
        ]

    def skip_white_space(self) -> None:
        while self.code.current() == " " or self.code.current() == "\n":
            next(self.code)

    def error(self) -> None:
        msg = f"Error: Token not recognized: {self.code.current()}"
        raise RuntimeError(msg)

    def search_next_token(self) -> Token | None:
        pos: int = self.code.get_index()
        for afd in self.afds:
            t: Token | None = afd.evaluate(self.code)
            if t is not None:
                return t
            self.code.set_index(pos)
        return None

    def get_token(self) -> list[Token]:
        t: Token | None = None
        while True:
            self.skip_white_space()
            t = self.search_next_token()
            if t is None:
                self.error()

            if t and t.tipo == "EOF":
                break
            t = cast("Token", t)
            self.tokens.append(t)
        return self.tokens
