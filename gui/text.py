"""
텍스트(Text)
여러 줄의 문자열을 처리 할 수 있다.
그 외에는 엔트리 컴포넌트와 거의 같다.
"""

import tkinter as tk

root = tk.Tk()
text = tk.Text(root)
text.pack()

data = '''Life is too short
You need python'''

text.insert(1.0, data)
"""
텍스트 컴포넌트의 insert() 함수 첫 번째 매개변수는
마치 실수처럼 구성된다.
소수점을 기준으로 왼쪽은 행(row), 오른쪽은 열(column)을 뜻한다.
텍스트의 특정 위치에 값을 삽입하고자 이런 방식을 사용한다.
"""