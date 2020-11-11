import sys
import csv
import re
import MeCab

import tkinter as tk
import matplotlib.cm as cm

import pdb

def extract_experiments_info(row_count):
    experiment_title_list = []
    experiment_title = ""
    experiment_content_list = []
    experiment_content = ""
    open_flag = 0
    for i in range(0, len(data[row_count][9])):
        c = data[row_count][9][i]
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

def extract_skeleton(parse_results, id):
    # pdb.set_trace()
    global sentence_list1
    global sentence_list2

    noun = []
    conj = []
    keywords = []
    skeleton = []
    noun_count = 0
    sentence_list1 = []
    sentence_list2 = []
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
                    sentence_list1.append(sentence)
                else:
                    sentence_list2.append(sentence)
                sentence = ""
                noun = []
            else:
                sentence = sentence + cols[0]

            if(parts[0].startswith('名詞') or parts[0].startswith('接続詞')):
                keywords.append(cols[0])
    skeleton.append(noun)
    if(id == 1):
        sentence_list1.append(sentence)
    else:
        sentence_list2.append(sentence)

    # pdb.set_trace()

    return skeleton
# print(data[i][0] + "\t" + str(skeleton) + "\t" + data[i][12] + "\t" + data[i][13])

def extract_symbol_skeleton(skeleton, conj_list, dir_list):
    ind_vec = [i for i in range(0, len(skeleton))]
    symbol_skeleton = []
    for i in ind_vec[1::2]:
        # symbol_skeleton.append(len(skeleton[i - 1]))
        symbol_skeleton.append('N')
        unk_flag = 1
        for j in range(0, len(conj_list)):
            if(skeleton[i] in conj_list[j]):
                unk_flag = 0
                symbol_skeleton.append(dir_list[j])
        if(unk_flag == 1):
            symbol_skeleton.append(skeleton[i] + ':?')
            pdb.set_trace()
    # symbol_skeleton.append(len(skeleton[-1]))
    symbol_skeleton.append('N')
    return symbol_skeleton

def compile_skeleton(symbol_skeleton):
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

def draw_horizontal_lines(canvas, start_x, start_y, circle_num, L):

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
        canvas.create_line(x1, origin_y, x2, origin_y, fill="black", width=1)
        coord = (x2, origin_y)
        end_coord = (x2, origin_y)
        coords_vec.append(coord)

    return end_coord, coords_vec

def draw_lines(canvas, compiled_skeleton, start_x, start_y, L):

    current_x = start_x
    current_y = start_y
    coords_vec = []

    if(len(compiled_skeleton) == 0):
        coords_vec.append((start_x, start_y))
    else:
        for s in compiled_skeleton:
            if(s.startswith('V')):
                canvas.create_line(current_x, current_y, current_x, current_y + L, fill="black", width=1)
                if((current_x, current_y) not in coords_vec):
                    coords_vec.append((current_x, current_y))
                current_y = current_y + L
            elif(s.startswith('H')):
                _, circle_num = s.split(':')
                circle_num = int(circle_num)
                (current_x, current_y), subcoords_vec = draw_horizontal_lines(canvas, current_x, current_y, circle_num, L)
                coords_vec.extend(subcoords_vec)
        if(compiled_skeleton[-1].startswith('V')):
            coords_vec.append((current_x, current_y))
    return coords_vec

def draw_circles(canvas, canvas_id, skeleton, coords_vec):
    radius_vec = [len(x) for x in skeleton[0::2]]

    for i in range(0, len(coords_vec)):
        coord = coords_vec[i]
        r = radius_vec[i]/4
        # r = 10
        color_vec = cm.jet(radius_vec[i])
        color_offset = 255
        html_color = '#%02X%02X%02X' % (int(color_vec[0]*color_offset), int(color_vec[1]*color_offset), int(color_vec[2]*color_offset))
        # pdb.set_trace()
        tags_id = 'noun_bag' + '_' + str(canvas_id) + '_' + str(i)
        # canvas.create_oval(coord[0] - r, coord[1] - r, coord[0] + r, coord[1] + r, fill=html_color, outline="#777", width=5, tags=tags_id)
        canvas.create_oval(coord[0] - r, coord[1] - r, coord[0] + r, coord[1] + r, fill="#aaa", outline="#777", width=5, tags=tags_id)
        if(canvas_id == 1):
            canvas.tag_bind(tags_id, "<ButtonPress-1>", clicked_canvas1)
        else:
            canvas.tag_bind(tags_id, "<ButtonPress-1>", clicked_canvas2)

def clicked_canvas1(event):
    global pressed_x, pressed_y, item_id

    item_id1 = canvas1.find_closest(event.x, event.y)
    tag1 = canvas1.gettags(item_id1[0])[0]
    item1 = canvas1.type(tag1)
    _, _, canvas_id, bag_id = tag1.split('_')
    bag_id = int(bag_id)
    bags = skeleton1[0::2]
    noun_bag1.delete('1.0', 'end')
    noun_bag1.insert('1.0', '\n(' + str(len(bags[bag_id])) + ' words)')
    noun_bag1.insert('1.0', bags[bag_id])

    sentence1.delete('1.0', tk.END)
    sentence1.tag_configure('RED', foreground = '#ff0000')
    for i in range(0, len(sentence_list1)):
        if(i == bag_id):
            sentence1.insert(tk.END, sentence_list1[i], 'RED')
        else:
            sentence1.insert(tk.END, sentence_list1[i])
            # print("Do nothing...")

    # print(bags[bag_id])

def clicked_canvas2(event):
    global pressed_x, pressed_y, item_id

    item_id2 = canvas2.find_closest(event.x, event.y)
    tag2 = canvas2.gettags(item_id2[0])[0]
    item2 = canvas2.type(tag2)

    _, _, canvas_id, bag_id = tag2.split('_')
    bag_id = int(bag_id)
    bags = skeleton2[0::2]
    noun_bag2.delete('1.0', 'end')
    noun_bag2.insert('1.0', '\n(' + str(len(bags[bag_id])) + ' words)')
    noun_bag2.insert('1.0', bags[bag_id])

    sentence2.delete('1.0', tk.END)
    sentence2.tag_configure('RED', foreground = '#ff0000')
    for i in range(0, len(sentence_list2)):
        if(i == bag_id):
            sentence2.insert(tk.END, sentence_list2[i], 'RED')
        else:
            sentence2.insert(tk.END, sentence_list2[i])
            # print("Do nothing...")

    # print(bags[bag_id])

mecab = MeCab.Tagger("-u /usr/lib/mecab/dic/research_plan_analysis/original_research_plan.dic")

file_name = "conj_symbols.csv"
with open(file_name) as f:
    reader = csv.reader(f)
    symbol_data = [row for row in reader]
conj_list = []
dir_list = []
for i in range(0, len(symbol_data)):
    conj_list.append(symbol_data[i][2].split('、'))
    dir_list.append(symbol_data[i][4])

def load_file():
    file_name = file_name_input.get()
    global data
    # file_name = sys.argv[1]
    with open(file_name) as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    print('File loaded!!')

def draw_skeleton1():
    global skeleton1

    canvas1.delete('all')
    row_count1 = id_input1.get()
    row_count1 = int(row_count1)
    parse_results1 = mecab.parse(data[row_count1][8])
    sentence1.delete('1.0', 'end')
    sentence1.insert('1.0', data[row_count1][8])
    skeleton1 = extract_skeleton(parse_results1, 1)
    symbol_skeleton1 = extract_symbol_skeleton(skeleton1, conj_list, dir_list)
    compiled_skeleton1 = compile_skeleton(symbol_skeleton1)

    max_r1 = int(max([len(x) for x in skeleton1[0::2]])/2)
    L1 = max_r1 + 40

    start_x = 150
    start_y = 100
    coords_vec1 = draw_lines(canvas1, compiled_skeleton1, start_x, start_y, L1)
    draw_circles(canvas1, 1, skeleton1, coords_vec1)

def draw_skeleton2():
    global skeleton2

    canvas2.delete('all')
    row_count2 = id_input2.get()
    row_count2 = int(row_count2)
    parse_results2 = mecab.parse(data[row_count2][8])
    sentence2.delete('1.0', 'end')
    sentence2.insert('1.0', data[row_count2][8])
    skeleton2 = extract_skeleton(parse_results2, 2)
    symbol_skeleton2 = extract_symbol_skeleton(skeleton2, conj_list, dir_list)
    compiled_skeleton2 = compile_skeleton(symbol_skeleton2)

    max_r2 = int(max([len(x) for x in skeleton2[0::2]])/2)
    L2 = max_r2 + 40

    start_x = 150
    start_y = 100
    coords_vec2 = draw_lines(canvas2, compiled_skeleton2, start_x, start_y, L2)
    draw_circles(canvas2, 2, skeleton2, coords_vec2)

def update_skeleton1():
    global skeleton1

    canvas1.delete('all')
    updated_sentence1 = sentence1.get('1.0', 'end -1c')
    parse_results1 = mecab.parse(updated_sentence1)
    skeleton1 = extract_skeleton(parse_results1, 1)
    symbol_skeleton1 = extract_symbol_skeleton(skeleton1, conj_list, dir_list)
    compiled_skeleton1 = compile_skeleton(symbol_skeleton1)

    max_r1 = int(max([len(x) for x in skeleton1[0::2]])/2)
    L1 = max_r1 + 40

    start_x = 150
    start_y = 100
    coords_vec1 = draw_lines(canvas1, compiled_skeleton1, start_x, start_y, L1)
    draw_circles(canvas1, 1, skeleton1, coords_vec1)

def update_skeleton2():
    global skeleton2

    canvas2.delete('all')
    updated_sentence2 = sentence2.get('1.0', 'end -1c')
    parse_results2 = mecab.parse(updated_sentence2)
    skeleton2 = extract_skeleton(parse_results2, 2)
    symbol_skeleton2 = extract_symbol_skeleton(skeleton2, conj_list, dir_list)
    compiled_skeleton2 = compile_skeleton(symbol_skeleton2)

    max_r2 = int(max([len(x) for x in skeleton2[0::2]])/2)
    L2 = max_r2 + 40

    start_x = 150
    start_y = 100
    coords_vec2 = draw_lines(canvas2, compiled_skeleton2, start_x, start_y, L2)
    draw_circles(canvas2, 1, skeleton2, coords_vec2)


root = tk.Tk()
root.title("Skeleton Visualizer")
root.geometry("1280x600")

mainFrame = tk.Frame(root, width = 1280, height = 600, bg = "gray")
mainFrame.pack()

visualFrame = tk.Frame(mainFrame, width = 640, height = 600)
sentenceFrame = tk.Frame(mainFrame, width = 640, height = 600, bg = "blue")
visualFrame.pack(side = "left")
sentenceFrame.pack(side = "left")

skeleton1Frame = tk.Frame(visualFrame, width = 320, height = 600, bg = "gray")
skeleton2Frame = tk.Frame(visualFrame, width = 320, height = 600, bg = "white")
skeleton1Frame.pack(side = "left")
skeleton2Frame.pack(side = "left")

# Skeleton1 Area
button1Frame = tk.Frame(skeleton1Frame, width = 320, height = 50)
display1Frame = tk.Frame(skeleton1Frame, width = 320, height = 420)
noun1Frame = tk.Frame(skeleton1Frame, width = 320, height = 130)
button1Frame.pack()
display1Frame.pack()
noun1Frame.pack()

# Button1 Area
file_name_label = tk.Label(button1Frame, text = 'Input File Name: ')
file_name_input = tk.Entry(button1Frame, text = 'File Name', width = 16)
file_name_button = tk.Button(button1Frame, text = 'Load', width = 4, height = 1, bd = 1, command = load_file)
"""
file_name_label.pack(side = "left")
file_name_input.pack(side = "left")
file_name_button.pack(side = "left")
"""
file_name_label.place(x = 5, y = 2)
file_name_input.place(x = 105, y = 2)
file_name_button.place(x = 245, y = 0)

id_label1 = tk.Label(button1Frame, text = 'Input Plan ID1: ')
id_input1 = tk.Entry(button1Frame, text = 'Plan ID1', width = 16)
id_button1 = tk.Button(button1Frame, text = 'Load', width = 4, height = 1, bd = 1, command = draw_skeleton1)
"""
id_label1.pack(side = "left")
id_input1.pack(side = "left")
id_button1.pack(side = "left")
"""
id_label1.place(x = 15, y = 30)
id_input1.place(x = 105, y = 30)
id_button1.place(x = 245, y = 25)

# Display1 Area
display1Subframe = tk.Frame(display1Frame, width = 320, height = 420)
canvas1 = tk.Canvas(display1Subframe, width = 305, height = 405, bg = "white")
bar_skeleton1_v = tk.Scrollbar(display1Subframe, orient = tk.VERTICAL)
bar_skeleton1_v.config(command = canvas1.yview)
canvas1.config(yscrollcommand = bar_skeleton1_v.set)
canvas1.config(scrollregion=(0, 0, 0, 1500))
canvas1.pack(side = "left")
bar_skeleton1_v.pack(side = "left")
display1Subframe.pack()
bar_skeleton1_h = tk.Scrollbar(display1Frame, orient = tk.HORIZONTAL)
bar_skeleton1_h.config(command = canvas1.xview)
canvas1.config(xscrollcommand = bar_skeleton1_h.set)
canvas1.config(scrollregion=(0, 1500, 0, 0))
bar_skeleton1_h.pack(side = "top")

# Noun1 Area
noun1_label = tk.Label(noun1Frame, text = "Focused Noun-Bag of Plan ID1")
noun_bag1 = tk.Text(noun1Frame, width=50, height=18)
bar_noun1_v = tk.Scrollbar(noun1Frame, orient = tk.VERTICAL)
bar_noun1_v.config(command = noun_bag1.yview)
noun_bag1.config(yscrollcommand = bar_noun1_v.set)
# noun_bag1.config(scrollregion=(0, 0, 0, 150))
noun1_label.pack()
noun_bag1.pack(side = "left")
bar_noun1_v.pack(side = "left")

# Skeleton2 Area
button2Frame = tk.Frame(skeleton2Frame, width = 320, height = 50)
display2Frame = tk.Frame(skeleton2Frame, width = 320, height = 420)
noun2Frame = tk.Frame(skeleton2Frame, width = 320, height = 130)
button2Frame.pack()
display2Frame.pack()
noun2Frame.pack()

# Button2 Area
id_label2 = tk.Label(root, text = 'Input Plan ID2: ')
id_input2 = tk.Entry(root, text = 'Plan ID2', width = 16)
id_button2 = tk.Button(root, text = 'Load', width = 4, height = 1, bd = 1, command = draw_skeleton2)
id_label2.place(x = 335, y = 30)
id_input2.place(x = 425, y = 30)
id_button2.place(x = 565, y = 25)

# Display2 Area
display2Subframe = tk.Frame(display2Frame, width = 320, height = 420)
canvas2 = tk.Canvas(display2Subframe, width = 305, height = 405, bg = "white")
bar_skeleton2_v = tk.Scrollbar(display2Subframe, orient = tk.VERTICAL)
bar_skeleton2_v.config(command = canvas2.yview)
canvas2.config(yscrollcommand = bar_skeleton2_v.set)
canvas2.config(scrollregion=(0, 0, 0, 1500))
canvas2.pack(side = "left")
bar_skeleton2_v.pack(side = "left")
display2Subframe.pack()
bar_skeleton2_h = tk.Scrollbar(display2Frame, orient = tk.HORIZONTAL)
bar_skeleton2_h.config(command = canvas2.xview)
canvas2.config(xscrollcommand = bar_skeleton2_h.set)
canvas2.config(scrollregion=(0, 1500, 0, 0))
bar_skeleton2_h.pack(side = "top")

# Noun2 Area
noun2_label = tk.Label(noun2Frame, text = "Focused Noun-Bag of Plan ID2")
noun_bag2 = tk.Text(noun2Frame, width=50, height=18)
bar_noun2_v = tk.Scrollbar(noun2Frame, orient = tk.VERTICAL)
bar_noun2_v.config(command = noun_bag2.yview)
noun_bag2.config(yscrollcommand = bar_noun2_v.set)
# noun_bag2.config(scrollregion=(0, 0, 0, 150))
noun2_label.pack()
noun_bag2.pack(side = "left")
bar_noun2_v.pack(side = "left")

sentence1Subframe = tk.Frame(sentenceFrame, width = 320, height = 600)
sentence2Subframe = tk.Frame(sentenceFrame, width = 320, height = 600)
sentence1Subframe.pack(side = "left")
sentence2Subframe.pack(side = "left")

sentence1ButtonFrame = tk.Frame(sentence1Subframe, width = 320, height = 50)
sentence1_label = tk.Label(sentence1ButtonFrame, text = "Sentence of Plan ID1")
update_skeleton1_button = tk.Button(sentence1ButtonFrame, text = 'Update', width = 4, height = 1, bd = 1, command = update_skeleton1)
sentence1 = tk.Text(sentence1Subframe, width = 52, height = 50)
sentence1_label.pack(side = "left")
update_skeleton1_button.pack(side = "left")
sentence1ButtonFrame.pack()
sentence1.pack(side = "top")

sentence2ButtonFrame = tk.Frame(sentence2Subframe, width = 320, height = 50)
sentence2_label = tk.Label(sentence2ButtonFrame, text = "Sentence of Plan ID2")
update_skeleton2_button = tk.Button(sentence2ButtonFrame, text = 'Update', width = 4, height = 1, bd = 1, command = update_skeleton2)
sentence2 = tk.Text(sentence2Subframe, width = 52, height = 50)
sentence2_label.pack(side = "left")
update_skeleton2_button.pack(side = "left")
sentence2ButtonFrame.pack()
sentence2.pack(side = "top")

"""
offset_x = 320
offset_y = 0

canvas1 = tk.Canvas(root, width = 320, height = 360, bg="#eee")
canvas2 = tk.Canvas(root, width = 320, height = 360, bg="white")

bar_lv = tk.Scrollbar(root, orient=tk.VERTICAL)
bar_lv.config(command=canvas1.yview)
bar_lv.place(x = 310, y = 30)
canvas1.config(yscrollcommand=bar_lv.set)
canvas1.config(scrollregion=(0, 0, 0, 1500)) #スクロール範囲

bar_lh = tk.Scrollbar(root, orient=tk.HORIZONTAL)
bar_lh.config(command=canvas1.xview)
bar_lh.place(x = 0, y = 360)
canvas1.config(xscrollcommand=bar_lh.set)
canvas1.config(scrollregion=(0, 1500, 0, 0)) #スクロール範囲


bar_rv = tk.Scrollbar(root, orient=tk.VERTICAL)
# bar_rh.pack(side=tk.RIGHT, fill=tk.Y)
bar_rv.config(command=canvas2.yview)


# canvas1.pack(side=tk.LEFT, fill=tk.BOTH)
canvas2.config(yscrollcommand=bar_rv.set)
canvas2.config(scrollregion=(0,0,0,1500)) #スクロール範囲
# canvas2.pack(side=tk.LEFT, fill=tk.BOTH)

noun_bag_label1 = tk.Label(root, text = 'Noun Bag for Plan ID1')
noun_bag_label1.place(x = 640, y = 30)
noun_bag_label2 = tk.Label(root, text = 'Noun Bag for Plan ID2')
noun_bag_label2.place(x = 640, y = 270)

noun_bag1 = tk.Text(root, width=50, height=18)
noun_bag1.place(x = 640, y = 50)
noun_bag2 = tk.Text(root, width=50, height=18)
noun_bag2.place(x = 640, y = 290)

file_name_label = tk.Label(root, text = 'Input File Name: ')
file_name_input = tk.Entry(root, text = 'File Name', width = 16)
file_name_button = tk.Button(root, text = 'Load', width = 4, height = 1, bd = 1, command = load_file)
file_name_label.place(x = 20, y = 2)
file_name_input.place(x = 120, y = 2)
file_name_button.place(x = 260, y = 0)

id_label1 = tk.Label(root, text = 'Input Plan ID1: ')
id_input1 = tk.Entry(root, text = 'Plan ID1', width = 16)
id_button1 = tk.Button(root, text = 'Load', width = 4, height = 1, bd = 1, command = draw_skeleton1)
id_label1.place(x = 20, y = 30)
id_input1.place(x = 120, y = 30)
id_button1.place(x = 260, y = 25)

id_label2 = tk.Label(root, text = 'Input Plan ID2: ')
id_input2 = tk.Entry(root, text = 'Plan ID2', width = 16)
id_button2 = tk.Button(root, text = 'Load', width = 4, height = 1, bd = 1, command = draw_skeleton2)
id_label2.place(x = 320, y = 30)
id_input2.place(x = 420, y = 30)
id_button2.place(x = 560, y = 25)

canvas1.place(x = 0, y = 50)
canvas2.place(x = offset_x, y = offset_y + 50)

"""

# compiled_skeleton2 = compile_skeleton(symbol_skeleton2)
"""
start_x = 150
start_y = 100
coords_vec1 = draw_lines(canvas1, compiled_skeleton1, start_x, start_y, L1)
coords_vec2 = draw_lines(canvas2, compiled_skeleton2, start_x, start_y, L2)
draw_circles(canvas1, 1, skeleton1, coords_vec1)
draw_circles(canvas2, 2, skeleton2, coords_vec2)
"""

# pdb.set_trace()
root.mainloop()
