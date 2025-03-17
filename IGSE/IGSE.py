import json
import tkinter as tk
from tkinter import LEFT
import random

root = tk.Tk()
root.configure(bg="dark slate grey", pady=7, padx=15)


class Point:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(x - 1.8, y - 1.8, x + 1.8, y + 1.8)
        self.selected = False

        self.offset_x = 0
        self.offset_y = 0

        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_move)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_release)

    def delete(self):
        self.canvas.delete(self.id)

    def on_press(self, event):
        self.selected = True
        self.offset_x = event.x - self.canvas.coords(self.id)[0]
        self.offset_y = event.y - self.canvas.coords(self.id)[1]

    def on_move(self, event):
        if self.selected:
            x = event.x - self.offset_x
            y = event.y - self.offset_y
            self.canvas.coords(self.id, x, y, x + self.canvas.coords(self.id)[2]-self.canvas.coords(self.id)[0],
                               y + self.canvas.coords(self.id)[3]-self.canvas.coords(self.id)[1])

    def on_release(self, event):
        self.selected = False


class Line:
    def __init__(self, canvas, start_x, start_y, end_x, end_y):
        self.canvas = canvas
        self.id = canvas.create_line(start_x, start_y, end_x, end_y)

    def delete(self):
        self.canvas.delete(self.id)


class Square:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x + size, y + size)
        self.selected = False

        self.offset_x = 0
        self.offset_y = 0

        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_move)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_release)

    def delete(self):
        self.canvas.delete(self.id)

    def on_press(self, event):
        self.selected = True
        self.offset_x = event.x - self.canvas.coords(self.id)[0]
        self.offset_y = event.y - self.canvas.coords(self.id)[1]

    def on_move(self, event):
        if self.selected:
            x = event.x - self.offset_x
            y = event.y - self.offset_y
            self.canvas.coords(self.id, x, y, x + self.canvas.coords(self.id)[2]-self.canvas.coords(self.id)[0],
                               y + self.canvas.coords(self.id)[3]-self.canvas.coords(self.id)[1])

    def on_release(self, event):
        self.selected = False


class Circle:
    def __init__(self, canvas, x, y, radius):
        self.canvas = canvas
        self.id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius)
        self.selected = False

        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_move)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_release)

    def delete(self):
        self.canvas.delete(self.id)

    def on_press(self, event):
        self.selected = True
        self.offsetx = event.x
        self.offsety = event.y

    def on_move(self, event):
        if self.selected:
            dx = event.x - self.offsetx
            dy = event.y - self.offsety
            self.canvas.move(self.id, dx, dy)
            self.offsetx = event.x
            self.offsety = event.y

    def on_release(self, event):
        self.selected = False

class Triangle:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.id = canvas.create_polygon(x, y - size, x - size, y + size, x + size, y + size)
        self.selected = False

        self.offset_x = 0
        self.offset_y = 0

        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_move)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_release)

    def delete(self):
        self.canvas.delete(self.id)

    def on_press(self, event):
        self.selected = True
        self.offset_x = event.x - self.canvas.coords(self.id)[0]
        self.offset_y = event.y - self.canvas.coords(self.id)[1]

    def on_move(self, event):
        if self.selected:
            dx = event.x - (self.canvas.coords(self.id)[0] + self.offset_x)
            dy = event.y - (self.canvas.coords(self.id)[1] + self.offset_y)

            coords = self.canvas.coords(self.id)

            new_coords = [
                coords[0] + dx, coords[1] + dy,
                coords[2] + dx, coords[3] + dy,
                coords[4] + dx, coords[5] + dy
            ]

            self.canvas.coords(self.id, *new_coords)

    def on_release(self, event):
        self.selected = False

class ShapesFunctionality:
    def __init__(self, master):
        self.master = master
        self.master.title("IGSE")

        self.shapes_lst = []

        self.selected_color = "black"
        self.instructions_visible = True

        self.latest_line = None
        self.latest_square = None
        self.latest_circle = None
        self.latest_triangle = None

        self.create_menu()

        self.canvas = tk.Canvas(self.master, width=1000, height=600)
        self.canvas.pack(fill="both", expand=True, padx=30, pady=20)

        self.canvas.bind("<Button-1>", self.create_shape)
        self.canvas.bind("<B2-Motion>", self.create_shape)
        self.canvas.bind("<Button-3>", self.random_shapes)

        self.master.bind("<Control-z>", lambda event: self.undo())  # For Windows / Linux
        self.master.bind("<Command-z>", lambda event: self.undo())  # For macOS

        self.title_text = self.canvas.create_text(
            475, 60, text="Welcome to IGSE", font="Arial 30 bold", fill="white", justify="center"
        )

        self.subtitle_text = self.canvas.create_text(
            475, 90, text="Interactive Geometric Shape Editor", font="Arial 20", fill="white", justify="center"
        )

        self.instructions_text = self.canvas.create_text(
            100, 350,  # Position
            text=(
                "Follow the instructions below to create and manipulate geometric shapes efficiently:\n\n"
                "Select a Shape:\n"
                "   • Choose the desired shape from the menu on the left. Available options include "
                "points, lines, squares, circles, and triangles.\n\n"
                "Create a Shape:\n"
                "   • Left Mouse Button: Click to create an individual shape at the clicked location.\n"
                "   • Right Mouse Button: Hold to continuously draw with the selected shape.\n"
                "   • Scroll Button: Shapes will be placed randomly around the canvas, adding variety to your design.\n\n"
                "Move a Shape:\n"
                "   • To move any shape, simply click and drag it to your desired location on the canvas.\n\n"
                "Resize a Shape:\n"
                "   • Use the '+' and '–' buttons to increase or decrease the size of the most recently created shape.\n\n"
                "Clear & Undo:\n"
                "   • If you make a mistake or wish to reset the canvas, use the CLEAR or UNDO options available "
                "in the menu. You can also\nuse CTRL+Z (Windows/Linux) or COMMAND+Z (MacOS) to "
                "revert the last action.\n\n"
                "Save & Load:\n"
                "   • Save your designs and reload them later with the SAVE and LOAD buttons.\n\n"
                "Hide/Show Instructions:\n"
                "   • Click the 'instructions' button on bottom left side to hide this guide and bring it back whenever needed."
            ),
            font="Arial 15", fill="silver", width=1000, anchor="w"
        )

    def create_menu(self):
        menu = tk.Frame(self.master)
        menu.pack(side=LEFT, fill="y", pady=20)

        menu_message = tk.Message(menu, text="Tools:", font="Arial 17", width=70, fg="silver")
        menu_message.pack()

        shapes = [
            "Point", "Line", "Square", "Circle", "Triangle"
        ]
        self.shape_name = tk.StringVar(value="SHAPES")
        shape_dropdown = tk.OptionMenu(menu, self.shape_name, *shapes)
        shape_dropdown.pack(pady=10)

        colors = [
            "Brown", "Red", "Orange", "Yellow", "Gold", "Green", "Lime", "Pink",
                  "Magenta", "Purple", "Blue", "Cyan", "White", "Silver", "Black"
        ]
        self.color_name = tk.StringVar(value="COLORS")
        color_dropdown = tk.OptionMenu(menu, self.color_name, *colors, command=self.on_color_select)
        color_dropdown.pack(pady=10)

        clear_button = tk.Button(menu, text="CLEAR", width=8, command=self.clear_canvas)
        clear_button.pack(pady=10)

        undo_button = tk.Button(menu, text="UNDO", width=8, command=self.undo)
        undo_button.pack(pady=10)

        full_name_message = tk.Message(menu, text="Resize last element:", font="Arial 15", width=110, justify="center",
                                       fg="silver")
        full_name_message.pack(pady=10)

        self.resize_button = tk.Button(menu, text='+', command=self.resize_up)
        self.resize_button.pack()

        self.resize_button_down = tk.Button(menu, text="–", command=self.resize_down)
        self.resize_button_down.pack(pady=20)

        save_button = tk.Button(menu, text="SAVE", width=8, command=self.save_canvas)
        save_button.pack()

        load_button = tk.Button(menu, text="LOAD", width=8, command=self.load_canvas)
        load_button.pack(pady=25)

        announce = tk.Message(menu, text="Created by:", font="Arial 10", width=110, justify="left")
        announce.pack()

        owner_name = tk.Message(menu, text="RUMEN\nILIEV", font="Arial 15", width=110, justify="center")
        owner_name.pack()

        instructions_button = tk.Button(menu, text="instructions", width=8, command=self.toggle_instructions)
        instructions_button.pack(pady=10, side="bottom")

    def on_color_select(self, color):
        self.selected_color = color

    def toggle_instructions(self):
        if self.instructions_visible:
            self.canvas.delete(self.title_text)
            self.canvas.delete(self.subtitle_text)
            self.canvas.delete(self.instructions_text)
            self.instructions_visible = False
        else:
            self.title_text = self.canvas.create_text(
                475, 60, text="Welcome to IGSE", font="Arial 30 bold", fill="white", justify="center"
            )

            self.subtitle_text = self.canvas.create_text(
                475, 90, text="Interactive Geometric Shape Editor", font="Arial 20", fill="white", justify="center"
            )

            self.instructions_text = self.canvas.create_text(
                100, 350,  # Position
                text=(
                    "Follow the instructions below to create and manipulate geometric shapes efficiently:\n\n"
                    "Select a Shape:\n"
                    "   • Choose the desired shape from the menu on the left. Available options include "
                    "points, lines, squares, circles, and triangles.\n\n"
                    "Create a Shape:\n"
                    "   • Left Mouse Button: Click to create an individual shape at the clicked location.\n"
                    "   • Right Mouse Button: Hold to continuously draw with the selected shape.\n"
                    "   • Scroll Button: Shapes will be placed randomly around the canvas, adding variety to your design.\n\n"
                    "Move a Shape:\n"
                    "   • To move any shape, simply click and drag it to your desired location on the canvas.\n\n"
                    "Resize a Shape:\n"
                    "   • Use the '+' and '–' buttons to increase or decrease the size of the most recently created shape.\n\n"
                    "Clear & Undo:\n"
                    "   • If you make a mistake or wish to reset the canvas, use the CLEAR or UNDO options available "
                    "in the menu. You can also\nuse CTRL+Z (Windows/Linux) or COMMAND+Z (MacOS) to "
                    "revert the last action.\n\n"
                    "Save & Load:\n"
                    "   • Save your designs and reload them later with the SAVE and LOAD buttons.\n\n"
                    "Hide/Show Instructions:\n"
                    "   • Click the 'instructions' button on bottom left side to hide this guide and bring it back whenever needed."
                ),
                font="Arial 15", fill="silver", width=1000, anchor="w"
            )
            self.instructions_visible = True

    def create_shape(self, event):
        shape = self.shape_name.get()

        if shape == "Point":
            self.create_point(event.x, event.y)
        elif shape == "Line":
            self.create_line(event.x, event.y)
        elif shape == "Square":
            self.create_square(event.x, event.y)
        elif shape == "Circle":
            self.create_circle(event.x, event.y)
        elif shape == "Triangle":
            self.create_triangle(event.x, event.y)

    def create_point(self, x, y):
        point = self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill=self.selected_color)
        self.shapes_lst.append(point)

    def create_line(self, x, y):
        line = self.canvas.create_line(x, y, x + 50, y + 50, fill=self.selected_color, width=2)
        self.shapes_lst.append(line)
        self.latest_line = line

    def create_square(self, x, y):
        square = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill=self.selected_color)
        self.shapes_lst.append(square)
        self.latest_square = square

    def create_circle(self, x, y):
        radius = 20
        circle = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=self.selected_color)
        self.shapes_lst.append(circle)
        self.latest_circle = circle

    def create_triangle(self, x, y):
        size = 20
        triangle = self.canvas.create_polygon(x, y - size, x - size, y + size, x + size, y + size,
                                              fill=self.selected_color)
        self.shapes_lst.append(triangle)
        self.latest_triangle = triangle

    def random_shapes(self, event):
        shape = self.shape_name.get()
        x, y = random.randint(0, 1000), random.randint(0, 600)

        if shape == 'Point':
            self.create_point(x, y)
        elif shape == "Line":
            self.create_line(x, y)
        elif shape == 'Square':
            self.create_square(x, y)
        elif shape == "Circle":
            self.create_circle(x, y)
        elif shape == "Triangle":
            self.create_triangle(x, y)

    def resize_up(self):
        shape = self.shape_name.get()

        if shape == "Line" and self.latest_line:
            width = self.canvas.itemcget(self.latest_line, 'width')
            new_width = float(width) + 1
            self.canvas.itemconfigure(self.latest_line, width=new_width)
        elif shape == "Square" and self.latest_square:
            current_square_size = self.canvas.coords(self.latest_square)
            self.canvas.coords(self.latest_square, current_square_size[0] - 5, current_square_size[1] - 5,
                               current_square_size[2] + 5, current_square_size[3] + 5)
        elif shape == "Circle" and self.latest_circle:
            current_circle_size = self.canvas.coords(self.latest_circle)
            self.canvas.coords(self.latest_circle, current_circle_size[0] - 5, current_circle_size[1] - 5,
                               current_circle_size[2] + 5, current_circle_size[3] + 5)
        elif self.latest_triangle:
            coords = self.canvas.coords(self.latest_triangle)

            cx = (coords[0] + coords[2] + coords[4]) / 3
            cy = (coords[1] + coords[3] + coords[5]) / 3

            scale = 1.2
            new_coords = []
            for i in range(0, len(coords), 2):
                new_x = cx + (coords[i] - cx) * scale
                new_y = cy + (coords[i + 1] - cy) * scale
                new_coords.extend([new_x, new_y])

            if len(new_coords) == 6:
                self.canvas.coords(self.latest_triangle, new_coords[0], new_coords[1],
                                   new_coords[2], new_coords[3], new_coords[4], new_coords[5])

    def resize_down(self):
        shape = self.shape_name.get()

        if shape == "Line" and self.latest_line:
            width = self.canvas.itemcget(self.latest_line, 'width')
            new_width = float(width) - 1
            self.canvas.itemconfigure(self.latest_line, width=new_width)
        elif shape == "Square" and self.latest_square:
            current_square_size = self.canvas.coords(self.latest_square)
            self.canvas.coords(self.latest_square, current_square_size[0] + 5, current_square_size[1] + 5,
                               current_square_size[2] - 5, current_square_size[3] - 5)
        elif shape == "Circle" and self.latest_circle:
            current_radius = self.canvas.coords(self.latest_circle)
            self.canvas.coords(self.latest_circle, current_radius[0] + 5, current_radius[1] + 5,
                               current_radius[2] - 5, current_radius[3] - 5)
        elif self.latest_triangle:
            coords = self.canvas.coords(self.latest_triangle)

            cx = (coords[0] + coords[2] + coords[4]) / 3
            cy = (coords[1] + coords[3] + coords[5]) / 3

            scale = 0.8
            new_coords = []
            for i in range(0, len(coords), 2):
                new_x = cx + (coords[i] - cx) * scale
                new_y = cy + (coords[i + 1] - cy) * scale
                new_coords.extend([new_x, new_y])

            if len(new_coords) == 6:
                self.canvas.coords(self.latest_triangle, new_coords[0], new_coords[1],
                                   new_coords[2], new_coords[3], new_coords[4], new_coords[5])

    def save_canvas(self):
        shapes = []
        for i in self.shapes_lst:
            shape_type = self.canvas.type(i)
            coords = self.canvas.coords(i)
            color = self.canvas.itemcget(i, "fill")
            shapes.append({"type": shape_type, "coords": coords, "color": color})

        with open("IGSE_History.json", "w") as file:
            json.dump(shapes, file)

    def load_canvas(self):
        try:
            with open("IGSE_History.json", "r") as file:
                shapes = json.load(file)
                self.clear_canvas()
                for i in shapes:
                    coords = i["coords"]
                    if i["type"] == "oval":
                        self.create_circle(coords[0] + 20, coords[1] + 20)
                    elif i["type"] == "rectangle":
                        self.create_square(coords[0], coords[1])
                    elif i["type"] == "line":
                        self.create_line(coords[0], coords[1])
                    elif i["type"] == "polygon":
                        self.create_triangle(coords[0], coords[1])
        except FileNotFoundError:
            print("No saved file found.")

    def undo(self):
        if self.shapes_lst:
            shape = self.shapes_lst.pop()
            self.canvas.delete(shape)

    def clear_canvas(self):
        [self.canvas.delete(x) for x in self.shapes_lst]
        self.shapes_lst.clear()


app = ShapesFunctionality(root)
root.mainloop()
