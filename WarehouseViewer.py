from Warehouse import Warehouse
import tkinter as tk
from PIL import ImageTk, Image
import tkinter.font as tkFont
import Cell
from state1 import State


class WarehouseViewer:

    def __init__(self, warehouse: Warehouse, canvas: tk.Canvas, display_width: int , display_height: int):
        self.warehouse = warehouse
        self.canvas = canvas

        unit_id, unit = max(self.warehouse.get_shelving_units().items(), key=lambda i: i[1].get_x())
        self.__max_col = unit.get_x()

        unit_id, unit = max(self.warehouse.get_shelving_units().items(), key=lambda i: i[1].get_y())
        self.__max_row = unit.get_y()
        
        width = display_width
        height = display_height

        self.__min_width = width / self.__max_col
        self.__min_height = (height - self.__min_width) / self.__max_row
        self.__DELTA_FONT_FOR_WAREHOUSE = 1/140 #1/97.375   # const
        self.__DELTA_FONT_FOR_SHELF = 1 / 120        # const
        self.__DELTA_SIZE_IMAGE = [429 / 1536, 400 / 864] #[143 / 1536, 313 / 864]
        self.__font_for_warehouse = tkFont.Font(family='sans', weight='bold',
                                                size=int((width+height)*self.__DELTA_FONT_FOR_WAREHOUSE))
        self.__font_for_shelving_unit = tkFont.Font(family='sans', weight='bold',
                                                    size=int((width+height)*self.__DELTA_FONT_FOR_SHELF))
        self.canvas.bind("<Configure>", lambda x: self.resize())

        self.__buttons_shelves = {}
        self.__labels = []

        self.__detail_window = None
        self.__buttons_cells = {}

        self.__legend_image = Image.open("./data/legend_sk.png")
        self.__imageTk = ImageTk.PhotoImage(self.__legend_image)

    def draw_shelving_unit_top_down(self, unit_id: str):
        unit = self.warehouse[unit_id]
        buttons_frame = tk.Frame(self.canvas)
        buttons_frame.config(width=self.__min_width, height=self.__min_height)
        col, row = unit.get_x(), unit.get_y()
       
        rel_width = 1 / (self.__max_col + 2)                                    # (0..1)
        rel_height = (2 - (rel_width * self.__max_row)) / (self.__max_row + 2)  # (0..1)
        rel_pos_x = (col+1) * rel_width                                         # (0..1)
        rel_pos_y = (row / 2) * rel_height + (row / 2) * rel_width              # (0..1)

        buttons_frame.place(relx=rel_pos_x, rely=rel_pos_y, relheight=rel_height, relwidth=rel_width)
        self.draw_shelving_unit_buttons(unit_id, buttons_frame)

    def draw_shelving_unit_buttons(self, unit_id: str, root: tk.Frame):
        shelves_count = len(self.warehouse[unit_id].get_shelves())
        rel_width = 1                                                           # (0..1)
        rel_height = 2 / (2 * shelves_count + 1)                                # (0..1)
        
        su_label = tk.Label(root, text=unit_id)
        su_label.place(relx=0, rely=0, relheight=rel_height / 2, relwidth=rel_width)
        su_label.config(font=self.__font_for_warehouse)
        # self.__labels.append(su_label)
        for i, shelf in enumerate(self.warehouse[unit_id].get_shelves().values()):
            rel_y = (shelves_count - i - 1) * rel_height + (rel_height / 2)
            count_free_cells = shelf.get_number_of_free_cells()
            count_blocked_cells = shelf.get_number_of_blocked_cells()
            text = f"{count_free_cells}" if (count_blocked_cells == 0) else f"{count_free_cells}({count_blocked_cells})"
            button = tk.Button(root, text=text, font=self.__font_for_warehouse,
                               bg=self.get_colour_by_count(count_free_cells))
            button.config(command=lambda: self.shelving_unit_button_press(unit_id))
            button.place(relx=0, rely=rel_y, relheight=rel_height, relwidth=rel_width)
            self.__buttons_shelves[button] = shelf

    def update_button_text(self):
        for button in self.__buttons_shelves:
            shelf = self.__buttons_shelves[button]
            count_free_cells = shelf.get_number_of_free_cells()
            count_blocked_cells = shelf.get_number_of_blocked_cells()
            text = f"{count_free_cells}" if (count_blocked_cells == 0) else f"{count_free_cells}({count_blocked_cells})"
            button.config(text=text, bg=self.get_colour_by_count(count_free_cells))

    @staticmethod
    def get_colour_by_count(count: int) -> str:
        if count <= 4:
            return "red"
        elif count <= 10:
            return "yellow"
        return "green"

    @staticmethod
    def get_colour(cell: Cell):
        if cell.is_blocked():
            return "gray"
        if cell.get_state() == State.FREE:
            return "green"
        return "red"

    def open_new_window(self, unit_id: str) -> tk.Toplevel:
        if self.__detail_window is not None:
            self.close_detail_window()
        self.__detail_window = tk.Toplevel()
        self.__detail_window.title(f"Regal cislo: {unit_id}")
        self.__detail_window.state('zoomed')
        self.__detail_window.protocol("WM_DELETE_WINDOW", self.close_detail_window)
        return self.__detail_window

    def close_detail_window(self):
        self.__detail_window.destroy()
        self.__detail_window = None
        self.__buttons_cells = {}


    def shelving_unit_button_press(self, unit_id: str):
        window = self.open_new_window(unit_id)
        self.draw_shelving_unit_side(window, unit_id)
        window.bind("<Configure>", lambda x: self.resize_shelf(window))
        
    def cell_button_press(self, button: tk.Button, cell: Cell):
        cell.change_block_state()
        self.update_button_text()
        button.config(bg=self.get_colour(cell))
    
    def draw_shelving_unit_side(self, root, unit_id: str):
        unit = self.warehouse[unit_id]
        shelves_count = len(unit.get_shelves())
        rel_height = 1 / shelves_count
        
        for shelf in unit.get_shelves().values():
            cells_count = len(shelf.get_cells())
            rel_width = 1 / cells_count
            rel_y = (shelves_count - shelf.get_level() - 1) * rel_height
            for cell in shelf.get_cells().values():
                rel_x = (cell.get_position() - 1) * rel_width
                button = tk.Button(root, text=f"{shelf.get_name()}-{cell.get_name()}",
                                   font=self.__font_for_shelving_unit, bg=self.get_colour(cell))
                self.set_cell_button(button, rel_y, rel_x, rel_height, rel_width, cell)

    def set_cell_button(self, button: tk.Button, rel_y: float, rel_x: float,
                        rel_height: float, rel_width: float, cell: Cell):
        button.place(relx=rel_x, rely=rel_y, relheight=rel_height, relwidth=rel_width)
        button.config(command=lambda: self.cell_button_press(button, cell))
        self.__buttons_cells[button] = cell

    def update_button_cell_background(self):
        for button in self.__buttons_cells:
            cell = self.__buttons_cells[button]
            button.config(bg=self.get_colour(cell))

    def resize(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.__font_for_warehouse.config(size=int((width+height)*self.__DELTA_FONT_FOR_WAREHOUSE))
        self.canvas.delete("legend")
        self.__legend_image = Image.open("./data/legend_sk.png").resize((int(width * self.__DELTA_SIZE_IMAGE[0]),
                                                               int(height * self.__DELTA_SIZE_IMAGE[1])))
        self.__imageTk = ImageTk.PhotoImage(self.__legend_image)
        self.canvas.create_image(width - self.__legend_image.width // 2, height - self.__legend_image.height // 2,
                                 image=self.__imageTk, tag="legend")

    def resize_shelf(self, root):
        width = root.winfo_width()
        height = root.winfo_height()
        self.__font_for_shelving_unit.config(size=int((width + height) * self.__DELTA_FONT_FOR_SHELF))

    def draw_levels_of_unit(self):
        x_pos = 0
        y_pos = -99
        for unit in self.warehouse.get_shelving_units().values():
            y = unit.get_y()
            if y_pos != y:
                y_pos = y
                level_frame = tk.Frame(self.canvas)
                level_frame.config(width=int(self.__min_width), height=int(self.__min_height))
                rel_width = 1 / (self.__max_col + 2)    # (0..1)
                rel_height = (2 - (rel_width * self.__max_row)) / (self.__max_row + 2)  # (0..1)
                rel_pos_y = (y_pos / 2) * rel_height + (y_pos / 2) * rel_width   # (0..1)
                level_frame.place(relx=x_pos, rely=rel_pos_y, relheight=rel_height, relwidth=rel_width)

                shelves_count = len(unit.get_shelves())
                rel_width = 1  # (0..1)
                rel_height = 2 / (2 * shelves_count + 1)  # (0..1)

                for lvl in range(len(unit.get_shelves())):
                    rel_y = (shelves_count - lvl - 1) * rel_height + (rel_height / 2)
                    label = tk.Label(level_frame, text=chr(65+lvl), font=self.__font_for_warehouse)
                    label.place(relx=0, rely=rel_y, relheight=rel_height, relwidth=rel_width)
                    self.__labels.append(label)
                
    def draw_legend(self):
        width = self.canvas.winfo_screenwidth()
        height = self.canvas.winfo_screenheight()
        self.__legend_image = Image.open("./data/legend_sk.png")
        self.__imageTk = ImageTk.PhotoImage(self.__legend_image)
        self.canvas.create_image(width-self.__legend_image.width//2,
                                 height-self.__legend_image.height//2, image=self.__imageTk, tag="legend")

    def show(self):
        for name in self.warehouse.get_shelving_units().keys():
            self.draw_shelving_unit_top_down(name)
        self.draw_legend()
        self.draw_levels_of_unit()
