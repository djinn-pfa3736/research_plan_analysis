
import os
import sys

import re
import MeCab

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk

import rohan_subwindow

import pdb

class MainControl(tk.Frame):

    def __init__(self, master = None):
        super().__init__(master)

        self.pack()

        # self.master.geometry("300x300")
        self.master.geometry()
        self.master.title("Rohan Main Control")

        self.create_ui()


    def create_ui(self):

        self.input_label = ttk.Label(self, text = "CSV File Name: ")
        self.input_label.pack(side = "left")

        self.file_name = tk.StringVar()
        self.file_name_entry = ttk.Entry(self, textvariable = self.file_name)
        self.file_name_entry.pack(side = "left")

        self.choose_button = ttk.Button(self, text = "Choose", command = self.choose_file)
        self.choose_button.pack(side = "left")

        self.load_button = ttk.Button(self, text = "Create Window", command = self.load_file)
        self.load_button.pack(side = "left")


    def choose_file(self):
        file_type = [("","*")]
        input_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = tkinter.filedialog.askopenfilename(filetypes = file_type, initialdir = input_dir)
        self.file_name.set(file_path)

def load_file(self):
    file_name = self.file_name_entry.get()
    # file_name = sys.argv[1]
    with open(file_name) as f:
        reader = csv.reader(f)

    self.data = [row for row in reader]
    print('File loaded!!')

if __name__ == "__main__":
    root = tk.Tk()
    main_control = MainControl(master = root)
    main_control.pack()
    main_control.mainloop()
