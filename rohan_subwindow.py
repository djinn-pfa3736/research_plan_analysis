# -*- coding: utf-8 -*-

import re
import MeCab
import csv

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk

import matplotlib.cm as cm

import pdb

class ProcessWindow(tk.Frame):

    def __init__(self, data, conj_list, dir_list, master = None):
        super().__init__(master)

        self.pack()
        self.master.geometry()
        self.master.title("Rohan Process Window")

        self.data = data
        self.conj_list = conj_list
        self.dir_list = dir_list

        # mecab = MeCab.Tagger("-u /usr/lib/mecab/dic/original/original.dic")
        # mecab = MeCab.Tagger(r"-O chasen -u .\research_plan_conj.dic")
        self.mecab = MeCab.Tagger()
        self.create_ui()

    def create_ui(self):

        self.visual_frame = ttk.Frame(self)
        self.visual_frame.pack(side = "left")
        self.visual_frame.columnconfigure(0, weight = 1, uniform = "group1")
 
        self.sentence_frame = ttk.Frame(self)
        self.sentence_frame.pack(side = "left")


        # Visual Window

        # Term Area(Currently noun area)
        self.noun_frame = ttk.Frame(self.visual_frame)
        # self.noun_frame.grid(row = 2, column = 0, sticky = tk.W + tk.E)
        self.noun_frame.grid(row = 2, column = 0, sticky = tk.W + tk.E)

        self.subframe2 = ttk.Frame(self.noun_frame)
        self.subframe2.pack()
        self.noun_label = ttk.Label(self.subframe2, text = "Focused Noun-Bag of Plan ID")
        self.noun_bag = tkinter.Text(self.subframe2)

        self.bar_noun_v = tkinter.Scrollbar(self.subframe2, orient = tkinter.VERTICAL)
        self.bar_noun_v.config(command = self.noun_bag.yview, width = 10)
        self.noun_bag.config(yscrollcommand = self.bar_noun_v.set)
        self.noun_label.grid(row = 0, column = 0)
        self.noun_bag.grid(row = 1, column = 0)
        self.bar_noun_v.grid(row = 1, column = 1, sticky = tk.N + tk.S)

        # Skeleton Area
        self.skeleton_frame = ttk.Frame(self.visual_frame)
        self.skeleton_frame.grid(row = 1, column = 0, sticky = tk.W + tk.E)

        self.subframe1 = ttk.Frame(self.skeleton_frame)
        self.subframe1.grid(row = 0, column = 0)
        self.canvas = tkinter.Canvas(self.subframe1, bg = "white")
        self.canvas.config(scrollregion=(-1500, -1500, 1500, 1500))
        self.canvas.grid(row = 0, column = 0)

        self.bar_v = tkinter.Scrollbar(self.subframe1, orient = tkinter.VERTICAL, width = 10)
        self.bar_v.config(command = self.canvas.yview)
        self.canvas.config(yscrollcommand = self.bar_v.set)
        self.bar_v.grid(row = 0, column = 1, sticky = tk.N + tk.S)

        self.bar_h = tkinter.Scrollbar(self.subframe1, orient = tkinter.HORIZONTAL, width = 10)
        self.bar_h.config(command = self.canvas.xview)
        self.canvas.config(xscrollcommand = self.bar_h.set)
        self.bar_h.grid(row = 1, column = 0, sticky = tk.W + tk.E)

        # Button Area
        self.button_frame = ttk.Frame(self.visual_frame)
        self.button_frame.grid(row = 0, column = 0, sticky = tk.W + tk.E)

        self.id_label = ttk.Label(self.button_frame, text = 'Plan ID: ')
        self.id_input = ttk.Entry(self.button_frame, text = 'Plan ID')
        self.id_button = ttk.Button(self.button_frame, text = 'Load', command = self.draw_skeleton)
        self.id_label.pack(side = "left")
        self.id_input.pack(side = "left")
        self.id_button.pack(side = "left")

        # Sentence Window
        sentence_button_frame = ttk.Frame(self.sentence_frame)
        sentence_label = ttk.Label(sentence_button_frame, text = "Sentence of Plan ID")
        update_skeleton_button = ttk.Button(sentence_button_frame, text = 'Update', command = self.update_skeleton)
        self.sentence = tkinter.Text(self.sentence_frame)
        self.sentence.pack()
        score_label = ttk.Label(sentence_button_frame, text = "Score: ")
        score_val = tk.StringVar()
        scores_vec = ['1', '2', '3', '4', '5', 'NA']
        combobox = ttk.Combobox(sentence_button_frame, textvariable=score_val, values=scores_vec, width=5)
        save_button = ttk.Button(sentence_button_frame, text = "Save", command = self.save_result)

        sentence_label.grid(row=0, column=0, padx=0)
        update_skeleton_button.grid(row=0, column=1, padx=0)
        score_label.grid(row=1, column=0, padx=0)
        combobox.grid(row=1, column=1, padx=0, sticky=tkinter.E + tkinter.W)
        save_button.grid(row=2, column=1, padx=0, sticky=tkinter.E + tkinter.W)
        sentence_button_frame.pack()

    def extract_experiments_info(self, row_count):
        experiment_title_list = []
        experiment_title = ""
        experiment_content_list = []
        experiment_content = ""
        open_flag = 0
        for i in range(0, len(self.data[row_count][9])):
            c = self.data[row_count][9][i]
            if(c == "【"):
                open_flag = 1
                experiment_content_list.append(experiment_content)
                experiment_content = ""
            elif(c == "】"):
                open_flag = 0
                experiment_title_list.append(experiment_title)
                experiment_title = ""
            else:
                if(open_flag == 1):
                    experiment_title += c
                else:
                    experiment_content += c
        return experiment_title_list, experiment_content_list

    def extract_skeleton(self, parse_results, id):

        noun = []
        conj = []
        keywords = []
        skeleton = []
        noun_count = 0
        self.sentence_list = []
        sentence = ""
        for res in parse_results.split('\n'):
            cols = res.split('\t')
            if(1 < len(cols)):
                parts = cols[1].split(',')
                # print(cols)
                if(parts[0].startswith('名詞')):
                    noun.append(cols[0])
                    sentence = sentence + cols[0]
                    # noun_count += 1
                elif(parts[0].startswith('接続詞')):
                    conj.append(cols[0])
                    skeleton.append(noun)
                    skeleton.append(cols[0])
                    sentence = sentence + cols[0]
                    if(id == 1):
                        self.sentence_list.append(sentence)

                    sentence = ""
                    noun = []
                else:
                    sentence = sentence + cols[0]

                if(parts[0].startswith('名詞') or parts[0].startswith('接続詞')):
                    keywords.append(cols[0])
        skeleton.append(noun)
        self.sentence_list.append(sentence)

        # pdb.set_trace()

        return skeleton
    # print(data[i][0] + "\t" + str(skeleton) + "\t" + data[i][12] + "\t" + data[i][13])

    def extract_symbol_skeleton(self):
        ind_vec = [i for i in range(0, len(self.skeleton))]
        symbol_skeleton = []
        for i in ind_vec[1::2]:
            # symbol_skeleton.append(len(skeleton[i - 1]))
            symbol_skeleton.append('N')
            unk_flag = 1
            for j in range(0, len(self.conj_list)):
                if(self.skeleton[i] in self.conj_list[j]):
                    unk_flag = 0
                    symbol_skeleton.append(self.dir_list[j])
            if(unk_flag == 1):
                symbol_skeleton.append(self.skeleton[i] + ':?')
                pdb.set_trace()
        # symbol_skeleton.append(len(skeleton[-1]))
        symbol_skeleton.append('N')
        return symbol_skeleton

    def compile_skeleton(self, symbol_skeleton):
        compiled_skeleton = []
        circle_num = 1
        horizontal_flag = 0
        for i in range(0, len(symbol_skeleton)):
            if(symbol_skeleton[i].startswith('H')):
                horizontal_flag = 1
                circle_num += 1
            elif(symbol_skeleton[i].startswith('V')):
                if(horizontal_flag == 1):
                    horizontal_flag = 0
                    compiled_skeleton.append('H:' + str(circle_num))
                    circle_num = 1
                compiled_skeleton.append('V')
        if(1 < circle_num):
            compiled_skeleton.append('H:' + str(circle_num))
        return compiled_skeleton

    def draw_horizontal_lines(self, start_x, start_y, circle_num, L):

        coords_vec = []
        # coords_vec.append((start_x, start_y))
        # canvas.create_line(start_x, start_y, start_x, start_y + L, fill="black", width=3)

        if(circle_num % 2 == 0):
            origin_x = start_x - (circle_num/2 - 1)*L - L/2
        else:
            origin_x = start_x - ((circle_num - 1)/2)*L
        # origin_y = start_y + L
        origin_y = start_y

        coord = (origin_x, origin_y)
        coords_vec.append(coord)

        for i in range(1, circle_num):
            x1 = origin_x + (i - 1)*L
            x2 = origin_x + i*L
            self.canvas.create_line(x1, origin_y, x2, origin_y, fill="black", width=1)
            coord = (x2, origin_y)
            end_coord = (x2, origin_y)
            coords_vec.append(coord)

        return end_coord, coords_vec

    def draw_lines(self, compiled_skeleton, start_x, start_y, L):

        current_x = start_x
        current_y = start_y
        coords_vec = []

        if(len(compiled_skeleton) == 0):
            coords_vec.append((start_x, start_y))
        else:
            for s in compiled_skeleton:
                if(s.startswith('V')):
                    self.canvas.create_line(current_x, current_y, current_x, current_y + L, fill="black", width=1)
                    if((current_x, current_y) not in coords_vec):
                        coords_vec.append((current_x, current_y))
                    current_y = current_y + L
                elif(s.startswith('H')):
                    _, circle_num = s.split(':')
                    circle_num = int(circle_num)
                    (current_x, current_y), subcoords_vec = self.draw_horizontal_lines(current_x, current_y, circle_num, L)
                    coords_vec.extend(subcoords_vec)
            if(compiled_skeleton[-1].startswith('V')):
                coords_vec.append((current_x, current_y))
        return coords_vec

    def draw_circles(self, skeleton, coords_vec):
        radius_vec = [len(x) for x in skeleton[0::2]]

        for i in range(0, len(coords_vec)):
            coord = coords_vec[i]
            r = radius_vec[i]/4
            # r = 10
            color_vec = cm.jet(radius_vec[i])
            color_offset = 255
            html_color = '#%02X%02X%02X' % (int(color_vec[0]*color_offset), int(color_vec[1]*color_offset), int(color_vec[2]*color_offset))
            # pdb.set_trace()
            tags_id = 'nounbag_' + str(i)
            # canvas.create_oval(coord[0] - r, coord[1] - r, coord[0] + r, coord[1] + r, fill=html_color, outline="#777", width=5, tags=tags_id)
            self.canvas.create_oval(coord[0] - r, coord[1] - r, coord[0] + r, coord[1] + r, fill="#aaa", outline="#777", width=5, tags=tags_id)
            self.canvas.tag_bind(tags_id, "<ButtonPress-1>", self.clicked_canvas)

    def clicked_canvas(self, event):

        item_id = self.canvas.find_closest(event.x, event.y)
        tag = self.canvas.gettags(item_id[0])[0]
        item = self.canvas.type(tag)
        _, bag_id = tag.split('_')
        bag_id = int(bag_id)
        bags = self.skeleton[0::2]
        self.noun_bag.delete('1.0', 'end')
        self.noun_bag.insert('1.0', '\n(' + str(len(bags[bag_id])) + ' words)')
        self.noun_bag.insert('1.0', bags[bag_id])

        self.sentence.delete('1.0', tkinter.END)
        self.sentence.tag_configure('RED', foreground = '#ff0000')
        for i in range(0, len(self.sentence_list)):
            if(i == bag_id):
                self.sentence.insert(tkinter.END, self.sentence_list[i], 'RED')
            else:
                self.sentence.insert(tkinter.END, self.sentence_list[i])
                # print("Do nothing...")

    def save_result(self):
        with open('corrected_result.csv', 'a') as f:
             row_data = id_input1.get() + "," + score1_val.get() + "," + sentence1.get('1.0', 'end -1c')
             print(row_data, file=f)

    def draw_skeleton(self):

        self.canvas.delete('all')
        row_count = int(self.id_input.get())

        self.parse_results = self.mecab.parse(self.data[row_count][8])
        self.sentence.delete('1.0', 'end')
        self.sentence.insert('1.0', self.data[row_count][8])
        self.skeleton = self.extract_skeleton(self.parse_results, 1)
        symbol_skeleton = self.extract_symbol_skeleton()
        compiled_skeleton = self.compile_skeleton(symbol_skeleton)

        max_r = int(max([len(x) for x in self.skeleton[0::2]])/2)
        L = max_r + 40

        start_x = 150
        start_y = 100
        coords_vec = self.draw_lines(compiled_skeleton, start_x, start_y, L)
        self.draw_circles(self.skeleton, coords_vec)

    def update_skeleton(self):

        self.canvas.delete('all')
        updated_sentence = self.sentence.get('1.0', 'end -1c')
        parse_results = self.mecab.parse(updated_sentence)
        self.skeleton = self.extract_skeleton(parse_results, 1)
        symbol_skeleton = self.extract_symbol_skeleton()
        compiled_skeleton = self.compile_skeleton(symbol_skeleton)

        max_r = int(max([len(x) for x in self.skeleton[0::2]])/2)
        L = max_r + 40

        start_x = 150
        start_y = 100
        coords_vec = self.draw_lines(compiled_skeleton, start_x, start_y, L)
        self.draw_circles(self.skeleton, coords_vec)

if __name__ == '__main__':

    with open("a.csv") as f:
        reader = csv.reader(f)
        data = [row for row in reader]

    file_name = "conj_symbols.csv"
    with open(file_name) as f:
        reader = csv.reader(f)
        symbol_data = [row for row in reader]

    conj_list = []
    dir_list = []
    for i in range(0, len(symbol_data)):
        conj_list.append(symbol_data[i][2].split('、'))
        dir_list.append(symbol_data[i][4])

    root = tk.Tk()
    process_window = ProcessWindow(data = data, conj_list = conj_list, dir_list = dir_list, master = root)
    process_window.pack()
    process_window.mainloop()