import tkinter as tk
from tkinter import filedialog
from  tkinter import messagebox
from PIL import Image, ImageTk

class ImageSelectorWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root, background="#212121")
        self.geometry("225x550")
        self.resizable(False, False)
        self.title("Image Selector")
        self.app = app
        self.cache_images = []

        self.filepath = filedialog.askopenfilename(title="Select file",
                                              filetypes=(("png files", "*.png"), ("all files", "*.*")))
        if self.filepath:
            self.initiate_main_display()
        else:
            self.destroy()

    def initiate_main_display(self):
        # We will create a canvas for the image
        self.canvas = tk.Canvas(self, background="#212121", highlightthickness=0, borderwidth=0, width=200, height=200)
        self.canvas.pack(side=tk.TOP, expand=True, padx=10, pady=10)
        # Update canvas
        self.canvas.after(10, self.update_canvas_selection)

        self.image = Image.open(self.filepath)
        tk_image = ImageTk.PhotoImage(self.image.resize((200,200)))
        self.cache_images.append(tk_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

        # Label for the coordinates
        coordinates_label = tk.Label(self, text="Encrypting zone", background="#212121", foreground="#ffffff")
        coordinates_label.pack(side=tk.TOP)
        coordinates_label = tk.Label(self, text=f"image size: {self.image.width}x{self.image.height}", background="#212121", foreground="#ffffff")
        coordinates_label.pack(side=tk.TOP)

        # We will create a frame for the x and y coordinates and width and height
        x_frame = tk.Frame(self, background="#212121")
        x_frame.pack(side=tk.TOP)
        self.x_label = tk.Label(x_frame, text="X", background="#212121", foreground="#ffffff")
        self.x_label.pack(side=tk.LEFT, padx=10, pady=15)
        self.x_entry = tk.Entry(x_frame)
        self.x_entry.pack(side=tk.RIGHT, padx=10, pady=15)

        y_frame = tk.Frame(self, background="#212121")
        y_frame.pack(side=tk.TOP)
        self.y_label = tk.Label(y_frame, text="Y", background="#212121", foreground="#ffffff")
        self.y_label.pack(side=tk.LEFT, padx=10, pady=15)
        self.y_entry = tk.Entry(y_frame)
        self.y_entry.pack(side=tk.RIGHT, padx=10, pady=15)

        width_frame = tk.Frame(self, background="#212121")
        width_frame.pack(side=tk.TOP)
        self.width_label = tk.Label(width_frame, text="Width", background="#212121", foreground="#ffffff")
        self.width_label.pack(side=tk.LEFT, padx=10, pady=15)
        self.width_entry = tk.Entry(width_frame)
        self.width_entry.pack(side=tk.RIGHT, padx=10, pady=15)

        height_frame = tk.Frame(self, background="#212121")
        height_frame.pack(side=tk.TOP)
        self.height_label = tk.Label(height_frame, text="Height", background="#212121", foreground="#ffffff")
        self.height_label.pack(side=tk.LEFT, padx=10, pady=15)
        self.height_entry = tk.Entry(height_frame)
        self.height_entry.pack(side=tk.RIGHT, padx=10, pady=15)

        # Done button
        button = tk.Button(self, text="Done", command=self.check_and_send)
        button.pack(side=tk.BOTTOM, padx=10, pady=30)

    def check_and_send(self):
        try:
            x = self.x_entry.get()
            y = self.y_entry.get()
            width = self.width_entry.get()
            height = self.height_entry.get()
            # remove whitespaces
            x = x.replace(" ", "")
            y = y.replace(" ", "")
            width = width.replace(" ", "")
            height = height.replace(" ", "")
            if x == "" and y == "" and width == "" and height == "":
                x = 0
                y = 0
                width = self.image.width
                height = self.image.height
            else:
                x = int(x)
                y = int(y)
                width = int(width)
                height = int(height)

            x, y, width, height = self.check_bounds(x, y, width, height)
            self.app.api.upload_photo(self.filepath, x, y, width, height)
            self.app.showUserScreen()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))


    def update_canvas_selection(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())

            x, y, width, height = self.check_bounds(x, y, width, height)
            proportion_w_ratio = 200/self.image.width
            proportion_h_ratio = 200/self.image.height
            x *= proportion_w_ratio
            width *= proportion_w_ratio
            y *= proportion_h_ratio
            height *= proportion_h_ratio
            # Create a rectangle in the canvas
            if self.canvas.find_withtag("selection"):
                self.canvas.delete("selection")
            self.canvas.create_rectangle(x, y, x + width, y + height, outline="#ff0000", tag="selection", width=3)

            # Place the rectangle above the image
            self.canvas.tag_raise("selection")
            self.canvas.update()
        except:
            pass
        self.canvas.after(100, self.update_canvas_selection)

    def check_bounds(self, x, y, width, height) -> tuple:
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x + width > self.image.width:
            width = self.image.width - x
        if y + height > self.image.height:
            height = self.image.height - y
        return x, y, width, height
