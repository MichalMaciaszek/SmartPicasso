import requests
import tkinter as tk

from constants import FONT, FONT_LARGE, URL_LOGIN, LOGIN_VIEW_NAME, REGISTER_VIEW_NAME, MAIN_VIEW_NAME
from views.abstract_view import AbstractView


class LoginView(tk.Frame, AbstractView):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="SmartPicasso", font=FONT_LARGE)
        label.pack(pady=10, padx=10)

        label1 = tk.Label(self, text='Login:', font=FONT)
        label1.pack()

        input1 = tk.Entry(self)
        input1.insert(0, 'test@test.pl')
        input1.pack()

        label2 = tk.Label(self, text='Password:', font=FONT)
        label2.pack()

        input2 = tk.Entry(self, show="*")
        input2.insert(0, 'test123')
        input2.pack()

        button = tk.Button(self, text="Login", font=FONT,
                           command=lambda: self.login(controller, input1.get(), input2.get()))
        button.pack()

        button2 = tk.Button(self, text="Register", font=FONT, command=lambda: controller.show_frame(REGISTER_VIEW_NAME))
        button2.pack()

    @staticmethod
    def get_view_name() -> str:
        return LOGIN_VIEW_NAME

    def login(self, controller, login, password):
        print(login)
        print(password)
        data = {
            "email": str(login),
            "password": str(password)
        }
        resp = requests.post(URL_LOGIN, json=data)
        print(resp)
        if resp.status_code == 200:
            response = resp.json()
            token = response['token']

            controller.show_frame(MAIN_VIEW_NAME, token)
        else:
            print("bad pass")
            bad_pass_label = tk.Label(self, text='Wrong login/password!', font=FONT)
            bad_pass_label.pack()
        return ()
