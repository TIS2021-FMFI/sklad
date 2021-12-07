import Cell


class Shelf:
    def __init__(self, shelf_name: str, level: int):
        self.__name = shelf_name
        self.__level = level
        self.__cells = dict()

    def get_name(self) -> str:
        return self.__name

    def get_level(self) -> int:
        return self.__level

    def get_cells(self) -> dict[Cell]:
        return self.__cells

    def add_cell(self, cell: Cell):
        self.__cells[cell.get_name()] = cell

    def __getitem__(self, item: str):
        return self.__cells[item]

    def __str__(self):
        cell_string = "{"
        for cell in self.__cells.values():
            cell_string += str(cell) + ","
        cell_string = cell_string[:-1]
        cell_string += "}"
        return f"Shelf(name={self.__name}, level={self.__level}, cells={cell_string})"



