import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from .login_toplevel import LoginWindow
from .register_toplevel import RegisterWindow
import platform

class HomeScreen(tk.Frame):
    """
    This class represents the home frame shown in the main app. It contains a grid of
    images that all users have uploaded to the server.
    """
    def __init__(self, app):
        super().__init__(app.root, bg="#212121")
        self.pack(fill=tk.BOTH, expand=True)
        self.app = app
        self.cache_images = []

    def initiate_main_display(self):
        # First, if the frame is not empty, we destroy all the widgets
        for w in self.winfo_children():
            w.destroy()

        self.app.root.title("Home")
        # Then, we create the main menu
        self.create_main_menu()
        # We create a canvas to put the scrollbar in it
        # Calculate de height that the menu is taking
        self.canvas = tk.Canvas(self, background="#212121", highlightthickness=0, borderwidth=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # We configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.canvas_reconfigure)
        self.show_images()
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if platform.system() == "Windows" or platform.system() == "MacOS":
            self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        else:
            # Binding buttons are different in Linux
            self.canvas.bind_all("<Button-4>", self.on_mousewheel_up)
            self.canvas.bind_all("<Button-5>", self.on_mousewheel_down)

    def canvas_reconfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def on_mousewheel_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_main_menu(self):
        self.main_menu = tk.Menu(self.app.root)
        self.app.root.config(menu=self.main_menu)

        # We create the file menu
        self.file_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.app.root.quit)

        # We create the user menu
        self.user_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="User", menu=self.user_menu)
        self.user_menu.add_command(label="Login", command=self.login)
        self.user_menu.add_command(label="Register", command=self.register)


# DEVELOPER OPTIONS ##################################################
        # clear server
        """self.main_menu.add_command(label="CLEAN SERVER", command=self.clean_server)
        # admin mode
        self.main_menu.add_command(label="LOG AS ADMIN", command=self.admin_mode)

    def admin_mode(self):
        try:
            self.app.api.login("admin", "Admin_123456")
        except ValueError:
            self.app.api.register("admin", "Admin_123456")
            self.app.api.login("admin", "Admin_123456")
        self.app.showUserScreen()

    def clean_server(self):
        self.app.api.server.clear_server()
        self.initiate_main_display()"""
#####################################################################

    def show_images(self):
        self.images = []
        self.app.updateStatus("Getting images from server...")
        for progress, i in self.app.api.get_images(username="@all"):
            self.images.append(i)
            self.app.updateProgress(progress)
        y = 0
        self.app.updateStatus("Loading images...")
        for i in range(len(self.images)):
            image = ImageTk.PhotoImage(self.images[i].image.resize((200, 200)))
            self.cache_images.append(image)
            image_label = tk.Label(self.canvas, image=image)
            if i != 0 and i % 3 == 0:
                y += 210
            self.canvas.create_window(((i % 3) * 210, y), window=image_label, anchor="nw")

    def refresh(self):
        for w in self.winfo_children():
            w.destroy()
        self.initiate_main_display()

    def login(self):
        LoginWindow(self.app)

    def register(self):
        RegisterWindow(self.app)