class Cell:
    def __init__(self, name: str, position: int, blocked: bool):
        self.__name = name
        self.__position = position
        self.__blocked = blocked

    def get_name(self) -> str:
        return self.__name

    def get_position(self) -> int:
        return self.__position

    def is_blocked(self) -> bool:
        return self.__blocked

    def change_block_state(self):
        self.__name = not self.__blocked

    def __str__(self):
        return f"Cell(name={self.__name}, position={self.__position}, blocked={self.__blocked})"

