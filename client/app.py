import tkinter as tk

from constants import LOGIN_VIEW_NAME
from views.login_view import LoginView
from views.main_view import MainView
from views.register_view import RegisterView


class SmartPicasso(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.title('SmartPicasso')
        self.geometry('800x600')

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginView, MainView, RegisterView):
            frame = F(container, self)

            self.frames[F.get_view_name()] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LOGIN_VIEW_NAME)

    def show_frame(self, view, token=None):
        frame = self.frames[view]
        frame.tkraise()

        if token:
            frame.token = token


app = SmartPicasso()
app.mainloop()
