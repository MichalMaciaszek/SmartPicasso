import requests
import tkinter as tk

from constants import FONT, FONT_B, FONT_LARGE, URL_PROFILE, PROFILE_VIEW_NAME, MAIN_VIEW_NAME
from views.abstract_view import AbstractView


class ProfileView(tk.Frame, AbstractView):

    def __init__(self, parent, controller, main_view_controller):
        tk.Frame.__init__(self, parent)
        self.token = ''
        label = tk.Label(self, text="SmartPicasso", font=FONT_LARGE)
        label.pack(pady=10, padx=10)
        label_l1 = tk.Label(self, text="Login:", font=FONT_B)
        label_l1.pack(pady=10, padx=10)
        self.label_username = tk.Label(self, text='', font=FONT)
        self.label_username.pack(pady=10, padx=10)
        label_n1 = tk.Label(self, text="Name:", font=FONT_B)
        label_n1.pack(pady=10, padx=10)
        self.label_first_name = tk.Label(self, text='', font=FONT)
        self.label_first_name.pack(pady=10, padx=10)
        label_ln1 = tk.Label(self, text="Last name", font=FONT_B)
        label_ln1.pack(pady=10, padx=10)
        self.label_last_name = tk.Label(self, text='', font=FONT)
        self.label_last_name.pack(pady=10, padx=10)

        button_profile = tk.Button(self, text="Back", font=FONT,
                                   command=lambda: controller.show_frame(MAIN_VIEW_NAME, self.token))
        button_profile.pack()

    @staticmethod
    def get_view_name() -> str:
        return PROFILE_VIEW_NAME

    def start(self):
        headers = {'Authorization': 'Bearer ' + self.token}
        resp = requests.get(URL_PROFILE, headers=headers)
        response = resp.json()
        print(response)
        self.label_username['text'] = response['profile']['username']
        self.label_first_name['text'] = response['profile']['first_name']
        self.label_last_name['text'] = response['profile']['last_name']
