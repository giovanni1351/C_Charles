from typing import cast

from lexic.afd import AFD
from lexic.operators import (
    BracketsOperator,
    EndLineOperator,
    FloatOperator,
    IdentifierOperator,
    IntegerOperator,
    KeyWordOperator,
    LogicOperator,
    MathOperator,
    StringOperator,
)
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class Lexer:
    afds: list[AFD]
    tokens: list[Token]
    code: CharacterIterator

    def __init__(self, code: str) -> None:
        self.code = CharacterIterator(string=code)
        self.afds = []
        self.tokens = []
        self.afds = [
            IntegerOperator(),
            FloatOperator(),
            StringOperator(),
            BracketsOperator(),
            EndLineOperator(),
            KeyWordOperator(),
            IdentifierOperator(),
            LogicOperator(),
            MathOperator(),
        ]

    def skip_white_space(self) -> None:
        while self.code.current() == " " or self.code.current() == "\n" or self.code.current() == "\t":  # noqa: E501
            next(self.code)

    def error(self) -> None:
        line = 1
        column = 1
        for i, character in enumerate(self.code.string):
            if i == self.code.get_index() and character == self.code.current():
                break
            if character == "\n":
                line += 1
                column = 1
                continue
            column += 1

        msg = (
            f"Error: Token not recognized: {self.code.current()} error"
            f" in {line = } and {column = }"
        )
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
