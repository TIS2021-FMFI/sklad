from ShelvingUnit import ShelvingUnit
from Shelf import Shelf
from Cell import Cell
import json


class Warehouse:
    def __init__(self, name: str, config_path: str):
        self.__name = name
        self.__config_path = config_path
        self.__shelving_units = dict()
        self.__warehouse = dict()

    def get_name(self) -> str:
        return self.__name

    def get_shelving_units(self) -> dict[ShelvingUnit]:
        return self.__shelving_units

    def get_warehouse(self) -> dict:
        return self.__warehouse

    def add_shelving_unit(self, shelving_unit: ShelvingUnit):
        self.__shelving_units[shelving_unit.get_name()] = shelving_unit

    def __str__(self):
        shelving_unit_string = "{"
        for shelving_unit in self.__shelving_units.values():
            shelving_unit_string += str(shelving_unit) + ","
        shelving_unit_string = shelving_unit_string[:-1]
        shelving_unit_string += "}"
        return f"Warehouse(name={self.__name}, shelvingUnits={shelving_unit_string})"

    def __getitem__(self, item: str):
        return self.__shelving_units[item]

    def load_configuration(self):
        with open(self.__config_path) as config_file:
            self.__warehouse = json.load(config_file)
            for su_name in self.__warehouse.keys():
                su_x = self.__warehouse[su_name]['x']
                su_y = self.__warehouse[su_name]['y']
                shelving_unit = ShelvingUnit(su_name, su_x, su_y)
                for s_name in self.__warehouse[su_name].keys():
                    if s_name != 'x' and s_name != 'y':
                        s_level = self.__warehouse[su_name][s_name]['height']
                        shelf = Shelf(s_name, s_level)
                        for c_name in self.__warehouse[su_name][s_name].keys():
                            if c_name != 'height':
                                c_position = self.__warehouse[su_name][s_name][c_name]['position']
                                c_is_blocked = self.__warehouse[su_name][s_name][c_name]['blocked']
                                cell = Cell(c_name, c_position, c_is_blocked)
                                shelf.add_cell(cell)
                        shelving_unit.add_shelf(shelf)
                self.__shelving_units[su_name] = shelving_unit

    def save_configuration(self):
        for shelving_unit in self.__shelving_units.values():
            for shelf in shelving_unit.get_shelves().values():
                for cell in shelf.get_cells().values():
                    self.__warehouse[shelving_unit.get_name()][shelf.get_name()][cell.get_name()]['blocked'] = cell.is_blocked()
        with open(self.__config_path, "w") as output_file:
            json.dump(self.__warehouse, output_file, indent=4)



