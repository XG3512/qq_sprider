# 导入模块

import tkinter

from PIL import ImageGrab

# 获取当前分辨率下的屏幕尺寸

win = tkinter.Tk()

width = win.winfo_screenwidth()

height = win.winfo_screenheight()

# 全屏幕截图

img = ImageGrab.grab(bbox=(0, 0, width, height))

# 保存截图
print(type(img))
img.save('a.jpg')
