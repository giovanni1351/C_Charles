from string import ascii_letters
from typing import ClassVar, override

from lexic.afd import AFD
from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class KeyWordOperator(AFD):
    key_words_list: ClassVar[list[str]] = [
        "string",
        "float",
        "int",
        "for",
        "while",
        "if",
        "else",
        "else if",
        "input",
        "boolean",
        "console",
    ]

    @override
    def evaluate(self, code: CharacterIterator) -> Token | None:
        characters: str = ""
        i: int = code.get_index()
        if code[i] is None:
            return Token("EOF", "$")
        while True:
            atual: str | None = code[i]
            if atual is None:
                break
            if atual in ascii_letters:
                characters += atual
                i += 1
                continue
            if atual in "0123456789" and len(characters) > 1:
                characters += atual
                i += 1
                continue
            break
        code.set_index(new_index=i)
        if len(characters) > 0 and characters in self.key_words_list:
            return Token("RESERVED", characters)

        return None
