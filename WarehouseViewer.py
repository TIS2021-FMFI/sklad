from Warehouse import Warehouse
import tkinter as tk

class WarehouseViewer:


    def __init__(self, warehouse : Warehouse, canvas : tk.Canvas):    
        self.warehouse = warehouse
        self.canvas = canvas


    def draw_shelving_unit_top_down(self, unit_id : str):
        unit = self.warehouse[unit_id]
        button = tk.Canvas(self.canvas)
        button.config(width=self.__min_width, height=self.__min_height)
        col, row = unit.get_x(), unit.get_y()
        button.grid(column = col, row = row, sticky='news')
        button.bind('<ButtonPress-1>', lambda x : self.draw_shelving_unit_side(unit_id))

    def draw_shelving_unit_side(self, unit_id : str):       
        print(unit_id)
        unit = self.warehouse[unit_id]   

    def draw_shelving_units(self):
        k, u = max(self.warehouse.get_shelving_units().items(), key=lambda i: i[1].get_x())
        max_col = u.get_x()

        k, u = max(self.warehouse.get_shelving_units().items(), key=lambda i: i[1].get_y())
        max_row = u.get_y()

        width = canvas.winfo_screenwidth()
        height = canvas.winfo_screenheight()

        self.__min_width = width / max_col
        self.__min_height = (height - self.__min_width)/ max_row

        for name in self.warehouse.get_shelving_units().keys():
            self.draw_shelving_unit_top_down(name)

        col_count, row_count = self.canvas.grid_size()

        for col in range(col_count):
            self.canvas.grid_columnconfigure(col, minsize=self.__min_width)

        for row in range(row_count):
            if row % 2:
                self.canvas.grid_rowconfigure(row, minsize=self.__min_width)
            else:
                self.canvas.grid_rowconfigure(row, minsize=self.__min_height)
        #floor_plan = [[None] * (max_col + 1)  for i in range(max_row + 1)]





if __name__ == '__main__':
    config_path = 'warehouse_config.json'
    warehouse_name = 'gefco'
    w = Warehouse(warehouse_name, config_path)
    w.load_configuration()

    root = tk.Tk()
    #root.attributes('-fullscreen', True)
    root.state('zoomed')

    canvas = tk.Canvas(root, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    v = WarehouseViewer(w, canvas)
    v.draw_shelving_units()
    print(canvas.winfo_screenheight())
    
