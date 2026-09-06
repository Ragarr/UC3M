import tkinter as tk
import tkinter.ttk as ttk
import sys

class LoadingScreen(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, background="#525252")
        self.app = app
        self.loading_status = "Doing nothing..."

    def initiate_main_display(self):
        # First, if the frame is not empty, we destroy all the widgets
        for w in self.winfo_children():
            w.destroy()

        # Eliminate the menu
        self.app.root.config(menu=None)

        # Loading label
        self.loading_label = tk.Label(self, text="Loading...", background="#525252",
                                      foreground="#ffffff", font="Helvetica 20 bold")
        self.loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Add a progress bar
        self.progress_bar = ttk.Progressbar(self, mode="determinate", length=200)
        self.progress_bar.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.progress_bar.start()

    def update_status(self, status):
        # Eliminate previous status label (if exists)
        if hasattr(self, "status_label"):
            self.status_label.destroy()
        # Add a label to show the status
        self.status_label = tk.Label(self, text=status, background="#525252",
                                      foreground="#ffffff", font="Helvetica 10 bold")
        self.status_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        self.update_idletasks()
        self.update()
