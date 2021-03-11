import tkinter as tk

from constants import FONT, FONT_LARGE, MAIN_VIEW_NAME, PROJECTS_VIEW_NAME, PROFILE_VIEW_NAME
from views.profile_view import ProfileView
from views.project_view import ProjectView
from views.projects_add_view import ProjectsAddView
from views.projects_view import ProjectsView
from views.abstract_view import AbstractView


class MainView(tk.Frame, AbstractView):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frames = {}
        self.token = ''
        for F in (ProfileView, ProjectsView, ProjectsAddView, ProjectView):
            frame = F(parent, controller, self)

            self.frames[F.get_view_name()] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        label = tk.Label(self, text="SmartPicasso", font=FONT_LARGE)
        label.pack(pady=10, padx=10)
        label_u = tk.Label(self, text="Main menu", font=FONT)
        label_u.pack(pady=10, padx=10)

        button_projects = tk.Button(self, text="Projects", font=FONT,
                                    command=lambda: self.show_frame(PROJECTS_VIEW_NAME))
        button_projects.pack()

        button_profile = tk.Button(self, text="My profile", font=FONT,
                                   command=lambda: self.show_frame(PROFILE_VIEW_NAME))
        button_profile.pack()

    @staticmethod
    def get_view_name() -> str:
        return MAIN_VIEW_NAME

    def show_frame(self, view):
        frame = self.frames[view]
        frame.tkraise()

        if self.token:
            print(self.token)
            frame.token = self.token
            frame.start()
