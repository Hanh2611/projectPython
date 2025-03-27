import os.path
import tkinter as tk
from PIL import ImageTk, Image

def northPanel(root):
    northPanel = tk.Frame(root, bg="gray", width=800, height=100)
    northPanel.grid(row=0,padx=10, pady=10,sticky=tk.NSEW)

    imgIcon_add = Image.open("icon/add.png")
    resize_icon_add = imgIcon_add.resize((20, 20),Image.Resampling.LANCZOS)
    icon_add = ImageTk.PhotoImage(resize_icon_add)

    imgIcon_delete = Image.open("icon/delete.png")
    resize_icon_delete = imgIcon_delete.resize((20, 20),Image.Resampling.LANCZOS)
    icon_delete = ImageTk.PhotoImage(resize_icon_delete)

    imgIcon_detail = Image.open("icon/detail.png")
    resize_icon_detail = imgIcon_detail.resize((20, 20),Image.Resampling.LANCZOS)
    icon_detail = ImageTk.PhotoImage(resize_icon_detail)

    imgIcon_info = Image.open("icon/add.png")
    resize_icon_info = imgIcon_info.resize((20, 20),Image.Resampling.LANCZOS)
    icon_info = ImageTk.PhotoImage(resize_icon_info)

    northPanel.icon_add = icon_add
    northPanel.icon_delete = icon_delete
    northPanel.icon_detail = icon_detail
    northPanel.icon_info = icon_info

    them = tk.Button(northPanel, text="Thêm", image=northPanel.icon_add, compound=tk.LEFT,fg= "gray")
    them.pack(side=tk.LEFT, padx=10, pady=10)

    xoa = tk.Button(northPanel, text="Xóa", image=northPanel.icon_delete, compound=tk.LEFT,fg= "gray")
    xoa.pack(side=tk.LEFT, padx=10, pady=10)

    sua = tk.Button(northPanel, text="Sửa", image=northPanel.icon_detail, compound=tk.LEFT,fg = 'gray')
    sua.pack(side=tk.LEFT, padx=10, pady=10)

    chitiet = tk.Button(northPanel, text="Chi tiết", image=northPanel.icon_info, compound=tk.LEFT,fg = 'gray')
    chitiet.pack(side=tk.LEFT, padx=10, pady=10)
    return northPanel

def centerPanel(root):
    centerPanel = tk.Frame(root, bg="pink", width=800, height=500)
    centerPanel.grid(row=1, padx=10, pady=10)
    return centerPanel

def infor():
    root = tk.Tk()
    root.title("QUAN LI THONG TIN")
    root.geometry("800x600")
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    north = northPanel(root)
    center = centerPanel(root)
    root.mainloop()
infor()
