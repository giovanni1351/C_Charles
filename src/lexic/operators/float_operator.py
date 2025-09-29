from typing import override

from lexic.afd import AFD
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class FloatOperator(AFD):
    @override
    def evaluate(self, code: CharacterIterator) -> Token | None:
        characters: str = ""
        i = code.get_index()
        point_finded = False
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
            if atual == "." and not point_finded and len(characters) > 0:
                characters += atual
                i += 1
                point_finded = True
                continue
            break
        code.set_index(i)
        if len(characters) > 0:
            return Token(tipo="FLOATING", lexema=characters)

        return None
