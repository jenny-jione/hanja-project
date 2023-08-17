# 부수 추가 version

import tkinter as tk
from modules.load import load_file, load_today_file, load_split_file
from tkinter import font

window = tk.Tk()
# li = load_today_file()
# li = load_file('./data/data_radicals.csv')
li = load_split_file(split_num=1)

def window_geometry():
    window.geometry("{}x{}+{}+{}".format(width, height, pos_x, pos_y))

def setting(type: str):
    global width, height, pos_x, pos_y, \
        large_font_size, normal_font_size, small_font_size, \
        window_title, closing_remark, \
        transparent
    if type == 'linux':
        width = 110
        height = 180
        pos_x = 1900
        pos_y = 1000
        large_font_size = 20
        normal_font_size = 9
        small_font_size = 8
        window_title = 'tk'
        closing_remark = 'End'
        window_geometry()
        transparent = 0.3
        window.wait_visibility(window)
        window.wm_attributes("-alpha", transparent)
    else:
        if type == 'mac':
            width = 900
            height = 600
            large_font_size = 240
            normal_font_size = 40
            small_font_size = 35
        else:
            if 'search' in type:
                width = 400
                height = 700
                large_font_size = 30
                normal_font_size = 15
                small_font_size = 13
            else:
                width = 500
                height = 400
                large_font_size = 120
                normal_font_size = 20
                small_font_size = 15
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        pos_x = (screen_width - width) // 2
        pos_y = (screen_height - height) // 2
        window_title = 'Tkinter: 한자 3급 합격 기원🍀'
        closing_remark = '끝! 수고하셨습니다!!'
        window_geometry()
    
setting('linux')
large_font = font.Font(size=large_font_size)
normal_font = font.Font(size=normal_font_size)
small_font = font.Font(size=small_font_size)
# window.geometry("{}x{}+{}+{}".format(width, height, pos_x, pos_y))
window.title(window_title)


# TODO: gui_study.py, gui_test_*.py에서 공통으로 사용하는 부분이 너무 많은데
# 이것들도 다 이 base 파일에 넣을 수 있게 하기!!

# TODO: 자동으로 100개씩 나눠서 파일 저장해주는 프로그램 만들기.

# TODO: ii, __ refactor