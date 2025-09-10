from abc import ABC, abstractmethod

from lexic.token_lexico import Token
from utils.character_iterator import CharacterIterator


class AFD(ABC):
    @abstractmethod
    def evaluate(self, code: CharacterIterator) -> Token | None: ...

    def is_token_separator(self, code: CharacterIterator) -> bool | None:
        """Ele vai verificar o final do token, ou seja, todos os caracteres que
        identificam o final de um token
        """
        atual = code.current()
        return atual in [" ", "+", "-", "*", "/", "(", ")", "\n", None]
