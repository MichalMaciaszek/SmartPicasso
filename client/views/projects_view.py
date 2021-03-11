import requests
import tkinter as tk

from constants import FONT, FONT_LARGE, URL_PROJECTS, PROJECTS_VIEW_NAME, PROJECTS_ADD_VIEW_NAME, PROJECT_VIEW_NAME, \
    MAIN_VIEW_NAME
from views.abstract_view import AbstractView


class ProjectsView(tk.Frame, AbstractView):

    def __init__(self, parent, controller, main_view_controller):
        tk.Frame.__init__(self, parent)
        self.token = ''
        self.projects_buttons = []
        self.main_view_controller = main_view_controller
        label = tk.Label(self, text="SmartPicasso", font=FONT_LARGE)
        label.pack(pady=10, padx=10)
        button_add = tk.Button(self, text="Add project", font=FONT,
                               command=lambda: self.main_view_controller.show_frame(PROJECTS_ADD_VIEW_NAME))
        button_add.pack()

        button_back = tk.Button(self, text="Back", font=FONT,
                                command=lambda: controller.show_frame(MAIN_VIEW_NAME, self.token))
        button_back.pack()
        label0 = tk.Label(self, text='Projects:', font=FONT)
        label0.pack()

    @staticmethod
    def get_view_name() -> str:
        return PROJECTS_VIEW_NAME

    def start(self):
        for button in self.projects_buttons:
            button.destroy()
        self.projects_buttons = []
        headers = {'Authorization': 'Bearer ' + self.token}
        resp = requests.get(URL_PROJECTS, headers=headers)
        response = resp.json()
        print(response)
        for projects in response:
            button_proj = tk.Button(self, text=projects['name'], font=FONT,
                                    command=lambda: self.main_view_controller.show_frame(PROJECT_VIEW_NAME))
            button_proj.pack()
            self.projects_buttons.append(button_proj)
