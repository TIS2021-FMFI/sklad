from Shelf import Shelf


class ShelvingUnit:
    def __init__(self, name: str, x: float, y: float):
        self.__name = name
        self.__x = x
        self.__y = y
        self.__shelves = dict()

    def get_name(self) -> str:
        return self.__name

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def get_shelves(self) -> dict[Shelf]:
        return self.__shelves

    def add_shelf(self, shelf: Shelf):
        self.__shelves[shelf.get_name()] = shelf

    def __getitem__(self, item: str):
        return self.__shelves[item]

    def __str__(self):
        shelf_string = "{"
        for shelf in self.__shelves.values():
            shelf_string += str(shelf) + ","
        shelf_string = shelf_string[:-1]
        shelf_string += "}"
        return f"ShelvingUnit(name={self.__name}, x={self.__x}, y={self.__y}, shelves={shelf_string})"
