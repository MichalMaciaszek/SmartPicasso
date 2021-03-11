import requests
import tkinter as tk

from constants import FONT, FONT_LARGE, URL_REGISTER, REGISTER_VIEW_NAME, LOGIN_VIEW_NAME
from views.abstract_view import AbstractView


class RegisterView(tk.Frame, AbstractView):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="SmartPicasso", font=FONT_LARGE)
        label.pack(pady=10, padx=10)
        label_u = tk.Label(self, text="Register", font=FONT)
        label_u.pack(pady=10, padx=10)

        label0 = tk.Label(self, text='Email:', font=FONT)
        label0.pack()

        input0 = tk.Entry(self)
        input0.pack()

        label1 = tk.Label(self, text='Login:', font=FONT)
        label1.pack()

        input1 = tk.Entry(self)
        input1.pack()

        label2 = tk.Label(self, text='Password:', font=FONT)
        label2.pack()

        input2 = tk.Entry(self, show="*")
        input2.pack()

        label3 = tk.Label(self, text='First name:', font=FONT)
        label3.pack()

        input3 = tk.Entry(self)
        input3.pack()

        label4 = tk.Label(self, text='Last name:', font=FONT)
        label4.pack()

        input4 = tk.Entry(self)
        input4.pack()

        button1 = tk.Button(self, text="Register", font=FONT,
                            command=lambda: self.register(controller, input0.get(), input1.get(), input2.get(),
                                                          input3.get(), input4.get()))
        button1.pack()

        button2 = tk.Button(self, text="Cancel", font=FONT, command=lambda: controller.show_frame(LOGIN_VIEW_NAME))
        button2.pack()

    @staticmethod
    def get_view_name() -> str:
        return REGISTER_VIEW_NAME

    def register(self, controller, email, login, passw, name, lastname):
        data = {
            "email": str(email),
            "password": str(passw),
            "profile": {
                "username": str(login),
                "first_name": str(name),
                "last_name": str(lastname)
            }
        }
        print(data)
        response = requests.post(URL_REGISTER, json=data)
        print(response)
        if response.status_code == 201:
            response = response.json()
            controller.show_frame(LOGIN_VIEW_NAME)
        else:
            print("sth wrong")
            bad_pass_label = tk.Label(self, text='Something went wrong!', font=FONT)
            bad_pass_label.pack()
        return ()
