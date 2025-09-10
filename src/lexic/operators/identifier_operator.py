from typing import override

from lexic.afd import AFD
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class IdentifierOperator(AFD):
    @override
    def evaluate(self, code: CharacterIterator) -> Token | None:
        characters: str = ""
        i = code.get_index()
        while True:
            atual: str | None = code[i]
            if atual is None:
                break
            i += 1
            if atual in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXZY":
                characters += atual
                continue
            if atual in "0123456789" and len(characters) > 1:
                characters += atual
                continue
            break
        code.set_index(i)
        if len(characters) > 0:
            return Token(tipo="ID", lexema=characters)

        return None
