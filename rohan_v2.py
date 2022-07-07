
import os
import sys

import re
import MeCab
import csv

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk

import rohan_subwindow_v2

import pdb

class MainControl(tk.Frame):
# class MainControl:

    def __init__(self, master = None):
        super().__init__(master)

        self.pack()

        # self.master.geometry("300x300")
        master.geometry()
        master.title("Rohan Main Control")
        # master.resizable(0, 0)

        self.master = master
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
        # print('File loaded!!')

        file_name = "conj_symbols.csv"
        with open(file_name) as f:
            reader = csv.reader(f)
            symbol_data = [row for row in reader]

        conj_list = []
        dir_list = []
        for i in range(0, len(symbol_data)):
            conj_list.append(symbol_data[i][2].split('、'))
            dir_list.append(symbol_data[i][4])

        self.new_window = tk.Toplevel()
        process_window = rohan_subwindow_v2.ProcessWindow(data = self.data, conj_list = conj_list, dir_list = dir_list, master = self.new_window)

if __name__ == "__main__":
    root = tk.Tk()
    # root.geometry("500x30")
    main_control = MainControl(master = root)
    main_control.mainloop()
