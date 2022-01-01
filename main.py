from Warehouse import Warehouse
from DataImporter import DataImporter
from WarehouseViewer import WarehouseViewer
import tkinter as tk
if __name__ == "__main__":
    #w = Warehouse("121", "C:\\uniba\\TiS\\sklad\\config_mock_data.json")
    config_path = "martins_config_2.json"
    warehouse_name = 'gefco'
    w = Warehouse(warehouse_name, config_path)
    w.load_configuration()
    di = DataImporter()
    di.getShelvingUnits(w)
    root = tk.Tk()
    root.state('zoomed')
    #img = tk.PhotoImage(file = 'retezce_gefco_ilustrace.png')
    #background_label = tk.Label(root, image=img)
    #background_label.place(x=0, y=0, relwidth=1, relheight=1)
    canvas = tk.Canvas(root, bg='white', highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    v = WarehouseViewer(w, canvas)
    v.show()
    tk.mainloop()
