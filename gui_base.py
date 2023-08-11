import tkinter as tk
# from modules.load import load_file_today
from modules.load import load_split_file
from tkinter import font

window = tk.Tk()
# li = load_file_today()
li = load_split_file(split_num=3)

def window_geometry():
    window.geometry("{}x{}+{}+{}".format(width, height, pos_x, pos_y))

def setting(type: str):
    global width, height, pos_x, pos_y, \
        large_font_size, normal_font_size, \
        window_title, closing_remark, \
        transparent
    if type == 'linux':
        width = 100
        height = 150
        pos_x = 1900
        pos_y = 1000
        large_font_size = 18
        normal_font_size = 8
        window_title = 'tk'
        closing_remark = 'End'
        window_geometry()
        transparent = 0.3
        window.wait_visibility(window)
        window.wm_attributes("-alpha", transparent)
    elif type=='linuxsearch':
        width = 150
        height = 400
        pos_x = 1900
        pos_y = 950
        large_font_size = 16
        normal_font_size = 8
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
        else:
            width = 500
            height = 400
            large_font_size = 120
            normal_font_size = 20
            if 'search' in type:
                large_font_size = 20
                normal_font_size = 15
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
# window.geometry("{}x{}+{}+{}".format(width, height, pos_x, pos_y))
window.title(window_title)


# TODO: gui_study.py, gui_test_*.py에서 공통으로 사용하는 부분이 너무 많은데
# 이것들도 다 이 base 파일에 넣을 수 있게 하기!!

# TODO: 자동으로 100개씩 나눠서 파일 저장해주는 프로그램 만들기.

# TODO: ii, __ refactor