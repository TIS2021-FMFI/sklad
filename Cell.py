from state1 import State
class Cell:
    def __init__(self, name: str, position: int, blocked: bool):
        self.__name = name
        self.__position = position
        self.__blocked = blocked
        self.__state = State.FREE

    def set_state(self, state: State):
        self.__state = state

    def get_state(self):
        return self.__state
        
    def get_name(self) -> str:
        return self.__name

    def get_position(self) -> int:
        return self.__position

    def is_blocked(self) -> bool:
        return self.__blocked

    def change_block_state(self):
        self.__blocked = not self.__blocked

    def __str__(self):
        return "\n" + " "*12 + f"Cell(name={self.__name}, position={self.__position}, blocked={self.__blocked}, state={self.__state})"


