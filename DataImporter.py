from openpyxl import *
from Warehouse import Warehouse
from ShelvingUnit import *
from state1 import State

class DataImporter:

    def __init__(self):
        self.__globalPath = "export.XLSX"  # later will be changed for normal

    def setDataFile(self, path: str):
        self.__globalPath = path

    def getShelvingUnits(self, warehouse: Warehouse) -> ShelvingUnit:
        wb = load_workbook(self.__globalPath)
        ws = wb["Sheet1"]
        warehouse_places = ws['B']
        materials = ws['C']
        for i in range(1, len(warehouse_places)):
            names = warehouse_places[i].value.split('-')
            if len(names) == 3:
                shelvingunit_name, shelf_name, cell_name = names
            else:
                shelvingunit_name = names[0]
                shelf_name = names[1]
                cell_name = names[2]
            material = materials[i].value
            if (material != "<< prázdny >>"):
                warehouse[shelvingunit_name][shelf_name][cell_name].set_state(State.OCCUPIED)
            else:
                warehouse[shelvingunit_name][shelf_name][cell_name].set_state(State.FREE)



