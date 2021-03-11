import requests
import tkinter as tk

from constants import FONT, URL_PROJECTS, PROJECTS_ADD_VIEW_NAME, PROJECTS_VIEW_NAME
from views.abstract_view import AbstractView


class ProjectsAddView(tk.Frame, AbstractView):

    def __init__(self, parent, controller, main_view_controller):
        tk.Frame.__init__(self, parent)
        self.token = ''

        label0 = tk.Label(self, text='Project name:', font=FONT)
        label0.pack()

        input0 = tk.Entry(self)
        input0.pack()

        button_add = tk.Button(self, text="Confirm and add", font=FONT,
                               command=lambda: self.add_project(main_view_controller, input0.get()))
        button_add.pack()

        button_back = tk.Button(self, text="Back", font=FONT,
                                command=lambda: main_view_controller.show_frame(PROJECTS_VIEW_NAME))
        button_back.pack()

    @staticmethod
    def get_view_name() -> str:
        return PROJECTS_ADD_VIEW_NAME

    def start(self):
        print("ok")

    def add_project(self, controller, project_name):
        headers = {'Authorization': 'Bearer ' + self.token}
        data = {
            "name": str(project_name)
        }
        print(data)
        response = requests.post(URL_PROJECTS, json=data, headers=headers)
        print(response)
        if response.status_code == 201:
            response = response.json()
            controller.show_frame(PROJECTS_VIEW_NAME)
        else:
            print("sth wrong")
            bad_pass_label = tk.Label(self, text='Something went wrong!', font=FONT)
            bad_pass_label.pack()
        return ()
