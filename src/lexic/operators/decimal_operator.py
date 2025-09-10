from typing import override

from lexic.afd import AFD
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class DecimalOperator(AFD):
    @override
    def evaluate(self, code: CharacterIterator) -> Token | None:
        characters: str = ""
        i = code.get_index()
        if code[i] is None:
            return Token("EOF", "$")
        while True:
            atual: str | None = code[i]
            if atual is None:
                break
            if atual in "0123456789":
                characters += atual
                i += 1
                continue
            break
        code.set_index(i)
        if len(characters) > 0:
            return Token(tipo="DECIMAL", lexema=characters)

        return None
