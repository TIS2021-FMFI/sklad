from Warehouse import Warehouse
from WarehouseViewer import WarehouseViewer
from repeatedTimer import RepeatedTimer
from DataImporter import DataImporter
import pyglet as pyg
import tkinter as tk
import sys

class WarehouseController:
    def __init__(self):
        config_path = './data/warehouse_config.json'
        warehouse_name = 'gefco'
        self.__warehouse = Warehouse(warehouse_name, config_path)
        self.__warehouse.load_configuration()

        list_of_displays = pyg.canvas.Display().get_screens()
        list_of_roots = []
        root = tk.Tk()
        root.title("Nahlad skladu")
        for x,display in enumerate(list_of_displays):
            if x == 0: # main display is showed first, 
                root.state('zoomed')
                canvas = tk.Canvas(root, bg='white', highlightthickness=0)
                canvas.pack(fill=tk.BOTH, expand=True)
                list_of_roots.append([root,display.width,
                                 display.height, display.x, display.y, canvas])
            else:
                rk = tk.Toplevel(root) # new root window for secondary display
                rk.state('zoomed')
                canvas = tk.Canvas(rk, bg='white', highlightthickness=0)
                canvas.pack(fill=tk.BOTH, expand=True)
                list_of_roots.append([rk,display.width,
                                 display.height, display.x, display.y, canvas]) #root, resolution x , resolution y, top left position of monitor x, top left position of monitor y
        
        data_importer = DataImporter()
        data_importer.setDataFile(self.get_congif_path_from_file())
        data_importer.getShelvingUnits(self.__warehouse)

        list_of_viewers = [] # list of roots with data
        for roots in list_of_roots: # fill roots with data
            viewer = WarehouseViewer(self.__warehouse, roots[5], roots[4], roots[3])
            list_of_viewers.append(viewer)

        for x in list_of_roots: # move root on virtual display, 
            x[0].geometry('%dx%d+%d+%d' % (x[1], x[2] ,
                               x[3], x[4]))

        list_of_rt = []
        for viewer in list_of_viewers:  # update displays
            viewer.show()
            list_of_rt.append(RepeatedTimer(20, self.update, data_importer, self.__warehouse, viewer))

        try:
            tk.mainloop()   
        finally:
            for rt in list_of_rt:
                rt.stop()
            self.__warehouse.save_configuration()
            sys.exit()

    def get_congif_path_from_file(self):
        with open("./data/config.txt", "r") as file:
            for line in file:
                if "#" not in line:
                    return line

    def update(self, data_importer, warehouse, viewer):
        data_importer.getShelvingUnits(warehouse)
        viewer.update_button_text()
        viewer.update_button_cell_background()


if __name__ == '__main__':
    controller = WarehouseController()

