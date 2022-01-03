from Warehouse import Warehouse
from WarehouseViewer import WarehouseViewer
from repeatedTimer import RepeatedTimer
from DataImporter import DataImporter
import tkinter as tk


class WarehouseController:
    def __init__(self):
        config_path = 'martins_config_2.json'
        warehouse_name = 'gefco'
        self.__warehouse = Warehouse(warehouse_name, config_path)
        self.__warehouse.load_configuration()

        root = tk.Tk()
        root.state('zoomed')
        canvas = tk.Canvas(root, bg='white', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        data_importer = DataImporter()
        data_importer.getShelvingUnits(self.__warehouse)
        viewer = WarehouseViewer(self.__warehouse, canvas)
        viewer.show()
        rt = RepeatedTimer(10, self.update, data_importer, self.__warehouse, viewer)
        try:
            tk.mainloop()
        finally:
            rt.stop()
            self.__warehouse.save_configuration()


    def update(self, data_importer, warehouse, viewer):
        data_importer.getShelvingUnits(warehouse)
        viewer.update_button_text()

if __name__ == '__main__':
    controller = WarehouseController()
