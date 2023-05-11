import tkinter
from tkinter import LEFT
import random

window = tkinter.Tk()
window.configure(bg="dark slate grey", pady=7, padx=15)


class Point:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.id = canvas.create_oval(x - 1.8, y - 1.8, x + 1.8, y + 1.8)
        self.selected = False

        self.offset_x = 0
        self.offset_y = 0

        self.canvas.tag_bind(self.id, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.on_release)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.on_move)

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
        self.id = canvas.create_line(start_x, start_y, end_x, end_y, width=1)

    def delete(self):
        self.canvas.delete(self.id)


class Square:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x + size, y + size)
        self.selected = False

        self.offset_x = 0
        self.offset_y = 0

        self.canvas.tag_bind(self.id, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.on_release)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.on_move)

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

        self.canvas.tag_bind(self.id, '<ButtonPress-1>', self.select)
        self.canvas.tag_bind(self.id, '<ButtonRelease-1>', self.release)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.move)

    def delete(self):
        self.canvas.delete(self.id)

    def select(self, event):
        self.selected = True
        self.offsetx = event.x
        self.offsety = event.y

    def move(self, event):
        if self.selected:
            dx = event.x - self.offsetx
            dy = event.y - self.offsety
            self.canvas.move(self.id, dx, dy)
            self.offsetx = event.x
            self.offsety = event.y

    def release(self, event):
        self.selected = False


class ShapesFunctionality:
    def __init__(self, master):
        self.master = master
        self.master.title('~ Course Project ~')

        self.shapes_lst = []

        self.selected_color = ''

        self.create_menu()

        self.canvas = tkinter.Canvas(self.master, width=1000, height=600)
        self.canvas.pack(fill="both", expand=True, padx=30, pady=20)

        self.canvas.bind('<Button-1>', self.create_shape)
        self.canvas.bind('<Button-3>', self.random_shapes)

        self.scroll_click_enabled = False

    def create_menu(self):
        menu = tkinter.Frame(self.master)
        menu.pack(side=LEFT, fill='y', pady=20)

        menu_message = tkinter.Message(menu, text="Menu", font="Times 20 italic underline bold", width=70)
        menu_message.pack()

        clear_button = tkinter.Button(menu, text='Clear', width=7, command=self.clear_canvas)
        clear_button.pack(pady=10)

        undo_button = tkinter.Button(menu, text="Undo", width=7, command=self.undo)
        undo_button.pack(pady=10)

        shapes = ['Point', 'Line', 'Square', 'Circle']
        self.shape_name = tkinter.StringVar(value='Shapes')
        shape_dropdown = tkinter.OptionMenu(menu, self.shape_name, *shapes)
        shape_dropdown.pack(pady=10)

        colors = ['Brown', 'Red', 'Orange', 'Yellow', 'Gold', 'Green', 'Lime', 'Pink',
                  'Magenta', 'Purple', 'Blue', 'Cyan', 'White', 'Silver', 'Black']
        self.color_name = tkinter.StringVar(value='Colors')
        color_dropdown = tkinter.OptionMenu(menu, self.color_name, *colors, command=self.on_color_select)
        color_dropdown.pack(pady=10)

        self.resize_button = tkinter.Button(menu, text='+', command=self.resize_up)
        self.resize_button.pack()

        self.resize_button_down = tkinter.Button(menu, text="-", command=self.resize_down)
        self.resize_button_down.pack()

        create_button = tkinter.Button(menu, text='Create', width=7, command=self.toggle_scroll_click_enabled)
        create_button.pack(pady=10)

        message = tkinter.Message(menu, text="2001261038", font="Times 15 italic bold", width=80)
        message.pack(side="bottom")
        fname_message = tkinter.Message(menu, text="Rumen\nIliev", font="Times 20 italic bold")
        fname_message.pack(side='bottom')

    def on_color_select(self, event):
        self.selected_color = self.color_name.get()

    def toggle_scroll_click_enabled(self):
        self.scroll_click_enabled = not self.scroll_click_enabled

        shape = self.shape_name.get()

        if shape == 'Point':
            self.canvas.bind('<Button-1>', self.create_point)
            self.canvas.bind('<B1-Motion>', self.create_point)

        elif shape == "Line":
            self.canvas.bind('<Button-1>', self.start_line)
            self.canvas.bind('<B1-Motion>', self.draw_line)

        elif shape == 'Square':
            self.canvas.bind('<Button-1>', self.create_square)
            self.canvas.bind('<B1-Motion>', self.create_square)

        elif shape == "Circle":
            self.canvas.bind('<Button-1>', self.create_circle)
            self.canvas.bind('<B1-Motion>', self.create_circle)

    # Create
    def create_shape(self, event):
        if not self.scroll_click_enabled:
            return

        shape = self.shape_name.get()

        if shape == 'Point':
            self.create_point(event)
        elif shape == "Line":
            self.start_line(event)
            self.draw_line(event)
        elif shape == 'Square':
            self.create_square(event)
        elif shape == "Circle":
            self.create_circle(event)

    def create_point(self, coordinates):
        if self.scroll_click_enabled:
            return
        x, y = coordinates.x, coordinates.y

        point = Point(self.canvas, x, y)
        point.canvas.itemconfig(point.id, fill=self.selected_color)

        self.shapes_lst.append(point)

    # Create Line
    def start_line(self, coordinates):
        if self.scroll_click_enabled:
            return

        self.start_x, self.start_y = coordinates.x, coordinates.y
        self.current_line = Line(self.canvas, self.start_x, self.start_y, self.start_x, self.start_y)
        self.current_line.canvas.itemconfig(self.current_line.id, fill=self.selected_color)

        self.latest_line = self.current_line

    def draw_line(self, coordinates):
        if self.start_x and self.start_y and self.current_line:
            self.canvas.coords(self.current_line.id, self.start_x, self.start_y, coordinates.x, coordinates.y)

        self.shapes_lst.append(self.current_line)

    def create_square(self, coordinates):
        if self.scroll_click_enabled:
            return

        x, y = coordinates.x, coordinates.y
        size = 20

        square = Square(self.canvas, x, y, size)
        square.canvas.itemconfig(square.id, fill=self.selected_color)
        self.latest_square = square

        self.shapes_lst.append(square)

    def create_circle(self, coordinates):
        if self.scroll_click_enabled:
            return

        x, y = coordinates.x, coordinates.y

        circle = Circle(self.canvas, x, y, 20)
        circle.canvas.itemconfig(circle.id, fill=self.selected_color)
        self.latest_circle = circle

        self.shapes_lst.append(circle)

    # Random
    def random_shapes(self, event):
        if not self.scroll_click_enabled:
            return

        shape = self.shape_name.get()

        if shape == 'Point':
            self.random_points(event)
        elif shape == "Line":
            self.random_lines(event)
        elif shape == 'Square':
            self.random_squares(event)
        elif shape == "Circle":
            self.random_circles(event)

    def random_points(self, coordinates):
        if not self.scroll_click_enabled:
            return

        x = random.randint(0, 1000)
        y = random.randint(0, 600)
        point = Point(self.canvas, x, y)
        point.canvas.itemconfig(point.id, fill=self.selected_color)

        self.shapes_lst.append(point)

    def random_lines(self, coordinates):
        if not self.scroll_click_enabled:
            return

        start_x, start_y = random.randint(0, 1000), random.randint(0, 600)
        end_x, end_y = random.randint(0, 1000), random.randint(0, 600)

        line = Line(self.canvas, start_x, start_y, end_x, end_y)
        line.canvas.itemconfig(line.id, fill=self.selected_color)
        self.latest_line = line

        self.shapes_lst.append(line)

    def random_squares(self, coordinates):
        if not self.scroll_click_enabled:
            return

        x = random.randint(0, 1000)
        y = random.randint(0, 600)
        size = random.randint(5, 70)

        square = Square(self.canvas, x, y, size)
        square.canvas.itemconfig(square.id, fill=self.selected_color)
        self.latest_square = square

        self.shapes_lst.append(square)

    def random_circles(self, coordinates):
        if not self.scroll_click_enabled:
            return

        x = random.randint(0, 1000)
        y = random.randint(0, 600)

        circle = Circle(self.canvas, x, y, 20)
        circle.canvas.itemconfig(circle.id, fill=self.selected_color)
        self.latest_circle = circle

        self.shapes_lst.append(circle)

    # Resize shapes
    def resize_up(self):
        shape = self.shape_name.get()

        if shape == "Line":
            if self.latest_line:
                width = self.canvas.itemcget(self.latest_line.id, 'width')
                new_width = float(width) + 1

                self.canvas.itemconfigure(self.latest_line.id, width=new_width)
        elif shape == "Square":
            if self.latest_square:
                current_square_size = self.canvas.coords(self.latest_square.id)
                self.canvas.coords(self.latest_square.id, current_square_size[0] - 5, current_square_size[1] - 5,
                                   current_square_size[2] + 5, current_square_size[3] + 5)
        elif shape == "Circle":
            if self.latest_circle:
                current_circle_size = self.canvas.coords(self.latest_circle.id)
                self.canvas.coords(self.latest_circle.id, current_circle_size[0] - 5, current_circle_size[1] - 5,
                                   current_circle_size[2] + 5, current_circle_size[3] + 5)

    def resize_down(self):
        shape = self.shape_name.get()

        if shape == "Line":
            if self.latest_line:
                width = self.canvas.itemcget(self.latest_line.id, 'width')
                new_width = float(width) - 1

                self.canvas.itemconfigure(self.latest_line.id, width=new_width)
        elif shape == "Square":
            if self.latest_square:
                current_square_size = self.canvas.coords(self.latest_square.id)
                self.canvas.coords(self.latest_square.id, current_square_size[0] + 5, current_square_size[1] + 5,
                                   current_square_size[2] - 5, current_square_size[3] - 5)
        elif shape == "Circle":
            if self.latest_circle:
                current_radius = self.canvas.coords(self.latest_circle.id)
                self.canvas.coords(self.latest_circle.id, current_radius[0] + 5, current_radius[1] + 5,
                                   current_radius[2] - 5, current_radius[3] - 5)

    def undo(self):
        if self.shapes_lst:
            shape = self.shapes_lst.pop()
            shape.delete()

    def clear_canvas(self):
        [x.delete() for x in self.shapes_lst]


app = ShapesFunctionality(window)
window.mainloop()
