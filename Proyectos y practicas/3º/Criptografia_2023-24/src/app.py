import tkinter as tk
from screens.home_screen import HomeScreen
from screens.user_screen import UserScreen
from screens.loading_screen import LoadingScreen
from packages.client import Client


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.api = Client()
        self.root.geometry("700x400")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create the frames and position them in the grid
        self.frames = {}
        for fr in (HomeScreen, UserScreen, LoadingScreen):
            frame = fr(self)
            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.current_screen = HomeScreen
        self.showHomeScreen()
        # Initiate the app
        self.root.mainloop()

    def resetProgress(self):
        """Resets the progress bar to 0"""
        self.frames[LoadingScreen].progress_bar["value"] = 0
        self.frames[LoadingScreen].update()

    def updateProgress(self, progress):
        """Updates the progress bar to the given value"""
        self.frames[LoadingScreen].progress_bar["value"] = progress
        self.frames[LoadingScreen].update()

    def updateStatus(self, status):
        """Updates the loading status label to the given value"""
        self.frames[LoadingScreen].update_status(status)

    def showScreen(self, name):
        #shows the screen
        frame = self.frames[name]
        self.current_screen = frame
        frame.tkraise()

    def showHomeScreen(self):
        self.frames[LoadingScreen].initiate_main_display()
        self.showScreen(LoadingScreen)
        self.root.after(100, self.__showHomeScreen)

    def __showHomeScreen(self):
        self.frames[HomeScreen].initiate_main_display()
        self.showScreen(HomeScreen)

    def showUserScreen(self):
        self.frames[LoadingScreen].initiate_main_display()
        self.showScreen(LoadingScreen)
        self.root.after(100, self.__showUserScreen)

    def __showUserScreen(self):
        self.frames[UserScreen].initiate_main_display()
        self.showScreen(UserScreen)


if __name__ == '__main__':
    App()
