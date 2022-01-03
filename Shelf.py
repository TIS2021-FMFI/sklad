import Cell
from state1 import State

class Shelf:
    def __init__(self, shelf_name: str, level: int):
        self.__name = shelf_name
        self.__level = level
        self.__accessible = None
        self.__cells = dict()

    def get_name(self) -> str:
        return self.__name

    def get_number_of_free_cells(self) -> int:
        counter = 0
        for cell in self.__cells.keys():
            if self.__cells[cell].get_state() == State.FREE:
                counter += 1
        return counter

    def get_number_of_blocked_cells(self) -> int:
        return sum(map(lambda x: x.is_blocked(), self.__cells.values()))

    def get_level(self) -> int:
        return self.__level

    def get_cells(self) -> dict[Cell]:
        return self.__cells

    def add_cell(self, cell: Cell):
        self.__cells[cell.get_name()] = cell
        
    def get_accessible(self):
        return self.__accessible

    def __getitem__(self, item: str):
        return self.__cells[item]

    def __str__(self):
        cell_string = "{"
        for cell in self.__cells.values():
            cell_string += str(cell) + ","
        cell_string = cell_string[:-1]
        cell_string += "}"
        return "\n" + " "*8 + f"\nShelf(name={self.__name}, level={self.__level}, cells={cell_string})"



