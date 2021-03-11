import PIL.Image
import PIL.ImageTk
import tkinter as tk
import os
import cv2

from constants import PROJECT_VIEW_NAME, FONT, PROJECTS_VIEW_NAME
from gestures.gesture_recognition import MyVideoCapture
from views.abstract_view import AbstractView


class ProjectView(tk.Frame, AbstractView):

    def __init__(self, parent, controller, main_view_controller):
        tk.Frame.__init__(self, parent)
        self.token = ''
        self.window = controller
        self.main_view_controller = main_view_controller
        self.delay = 20
        self.canvas_width = 800
        self.canvas_height = 415
        self.start_draw = False
        self.vid = None
        self.vid_canvas = None
        self.canvas = None
        self.back_button = None
        self.clear_button = None
        self.save_button = None
        self.bottom_frame = None
        self.top_frame = None
        self.first_time = True
        self.other_gestures_flag_possible = False
    @staticmethod
    def get_view_name() -> str:
        return PROJECT_VIEW_NAME

    def start(self):
        self.vid = MyVideoCapture()
        self.canvas_width = self.window.winfo_width()
        self.canvas_height = self.window.winfo_height() - 185
        self.top_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=0)
        self.top_frame.pack(fill=tk.BOTH, side=tk.TOP)
        self.canvas = tk.Canvas(self.top_frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.grid(row=0, column=0)

        self.bottom_frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.bottom_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)
        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(1, weight=1)
        self.bottom_frame.columnconfigure(2, weight=15)
        self.back_button = tk.Button(self.bottom_frame, text="Back", font=FONT,
                                     command=lambda: self.back_to_projects_view())
        self.back_button.grid(row=0, column=0, sticky=tk.SW, pady=10, padx=5)
        self.clear_button = tk.Button(self.bottom_frame, text="Clear", font=FONT,
                                      command=lambda: self.clear_canvas())
        self.clear_button.grid(row=0, column=1, sticky=tk.SW, pady=10, padx=5)
        self.save_button = tk.Button(self.bottom_frame, text="Save", font=FONT,
                                     command=lambda: self.save())
        self.save_button.grid(row=0, column=2, sticky=tk.SW, pady=10, padx=5)
        self.vid_canvas = tk.Canvas(self.bottom_frame, width=self.vid.width, height=self.vid.height)
        self.vid_canvas.grid(row=0, column=3, sticky=tk.E)

        self.update()

    def create_window(self):
        window = tk.Toplevel()
        e1 = tk.Entry(window)
        e1.grid(row=0, column=1)
        okVar = tk.IntVar()
        tk.Button(window,text = 'Write',command=lambda: okVar.set(1)).grid(row=1,
                                    column=1,
                                    sticky=tk.W,
                                    pady=4)
        #print(okVar)
        self.window.wait_variable(okVar)
        self.text_to_write = e1.get()
        #print(self.text_to_write)
        window.destroy()
        #self.window.wait_window(window)


    def update(self):
        # Get a frame from the video source
        if self.vid is not None:
            fingers, frame, success = self.vid.get_frame()
            if fingers is not None:
                index_finger = fingers['index']
                middle_finger = fingers['middle']
                start_stop = fingers['start_stop']
                if fingers['ninja'] != 'nothing' and self.other_gestures_flag_possible == True:
                    #print('trying')
                    self.create_window()

                    cv2.waitKey(10)
                    self.other_gestures_flag_possible = False
                    x = index_finger['x']
                    y = index_finger['y']
                    x, y = self.scale_points(x, y)
                    self.canvas.create_text(x,y,fill="darkblue", text= self.text_to_write, tags='text',font=("Purisa", 20))

                if start_stop == 'start':
                    print('start')
                    self.start_draw = True
                    self.first_time = True
                    self.other_gestures_flag_possible = False

                elif start_stop == 'stop':
                    print('stop')
                    self.start_draw = False
                    self.first_time = False
                    self.other_gestures_flag_possible = True

                if self.start_draw and index_finger['straight'] and middle_finger['straight']:

                    x = index_finger['x']
                    y = index_finger['y']
                    x, y = self.scale_points(x, y)
                    if self.first_time == True:
                        self.previous_x = x
                        self.previous_y = y
                        self.first_time = False
                        #print("first_time")
                    canvas_id = self.canvas.create_line(x, y, x + 2, y + 2, self.previous_x, self.previous_y, tags='point', width=3, fill = 'red')
                    self.canvas.after(100, self.canvas.delete, canvas_id)
                    #self.canvas.create_line(x, y, x+1, y+1, self.previous_x, self.previous_y, tags='point', width=3)
                    self.previous_x = x
                    self.previous_y = y

                if self.start_draw and index_finger['straight'] and not middle_finger['straight']:

                    x = index_finger['x']
                    y = index_finger['y']
                    x, y = self.scale_points(x, y)
                    if self.first_time == True:
                        self.previous_x = x
                        self.previous_y = y
                        self.first_time = False
                        #print("first_time")
                    self.canvas.create_line(x, y, x+1, y+1, self.previous_x, self.previous_y, tags='point', width=3)

                    self.previous_x = x
                    self.previous_y = y
            if success:
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.vid_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            self.window.after(self.delay, self.update)

    def back_to_projects_view(self):
        self.main_view_controller.show_frame(PROJECTS_VIEW_NAME)
        self.vid.release()
        self.destroy_widgets()

    def clear_canvas(self):
        self.canvas.delete('all')

    def save(self):
        self.canvas.postscript(file='image.eps')
        img = PIL.Image.open('image.eps')
        img.save('image.png', 'png')
        os.remove('image.eps')

    def destroy_widgets(self):
        self.vid = None
        self.top_frame.destroy()
        self.canvas.destroy()
        self.bottom_frame.destroy()
        self.vid_canvas.destroy()
        self.back_button.destroy()

    def scale_points(self, x, y):
        return x*self.canvas_width, y*self.canvas_height
