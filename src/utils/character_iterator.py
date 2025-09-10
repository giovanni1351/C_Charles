class CharacterIterator:
    def __init__(self, string: str) -> None:
        self.string = string
        self._index: int = 0

    def current(self) -> str | None:
        if self._index < len(self.string):
            return self.string[self._index]
        return None

    def __iter__(self) -> "CharacterIterator":
        return self

    def __next__(self) -> str:
        if self._index >= len(self.string):
            raise StopIteration
        ch = self.string[self._index]
        self._index += 1
        return ch

    def __getitem__(self, position: int) -> str | None:
        if position >= len(self.string):
            return None
        return self.string[position]

    def get_index(self) -> int:
        return self._index

    def set_index(self, new_index: int) -> None:
        self._index = new_index
