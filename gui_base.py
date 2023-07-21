import tkinter as tk
from modules.load import load_file
from tkinter import font

window = tk.Tk()
li = load_file()

def setting(type: str):
    global width, height, pos_x, pos_y, \
        large_font_size, normal_font_size, \
        window_title, closing_remark
    if type == 'linux':
        width = 100
        height = 140
        pos_x = 1900
        pos_y = 1000
        large_font_size = 15
        normal_font_size = 8
        window_title = 'tk'
        closing_remark = 'End'
    elif type == 'mac':
        width = 500
        height = 300
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        pos_x = (screen_width - width) // 2
        pos_y = (screen_height - height) // 2
        large_font_size = 100
        normal_font_size = 20
        window_title = 'Tkinter: 한자 3급 합격 기원🍀'
        closing_remark = '끝! 수고하셨습니다!!'
    else:
        width = 500
        height = 200
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        pos_x = (screen_width - width) // 2
        pos_y = (screen_height - height) // 2
        large_font_size = 20
        normal_font_size = 5

setting('mac')
large_font = font.Font(size=large_font_size)
normal_font = font.Font(size=normal_font_size)
window.geometry("{}x{}+{}+{}".format(width, height, pos_x, pos_y))
# window.resizable(False, False)
window.title(window_title)

# TODO: gui_study.py, gui_test_*.py에서 공통으로 사용하는 부분이 너무 많은데
# 이것들도 다 이 base 파일에 넣을 수 있게 하기!!
# TODO: End, '끝, 수고하셨습니다!!' linux, mac 따로 설정하기. => 완료.
# TODO: title도! => 완료.