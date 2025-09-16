from typing import override

from lexic.afd import AFD
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class StringOperator(AFD):
    @override
    def evaluate(self, code: CharacterIterator) -> Token | None:
        characters: str = ""
        i: int = code.get_index()
        if code[i] is None:
            return Token("EOF", "$")
        if code[i] != '"':
            return None
        if code[i] == '"':
            characters += '"'
            i += 1

        while True:
            atual: str | None = code[i]
            if atual is None:
                break
            if atual == '"':
                characters += atual
                i += 1

                break

            characters += atual
            i += 1
        code.set_index(new_index=i)
        if characters.startswith('"') and characters.endswith('"'):
            return Token("STRING", characters)

        return None
