import tkinter as tk
import os


def northPanel(root):
    northPanel = tk.Frame(root, bg="gray", width=800, height=100)
    northPanel.grid(row=0,padx=10, pady=10,sticky=tk.NSEW)

    icon_add = tk.PhotoImage(file="src/icon/add.png")
    icon_delete = tk.PhotoImage(file="src/icon/delete.png")
    icon_detail = tk.PhotoImage(file="src/icon/detail.png")
    icon_info = tk.PhotoImage(file="src/icon/info.png")


    them = tk.Button(northPanel,text= "them",image=icon_add)
    them.pack(side=tk.LEFT,padx=10, pady=10)

    xoa = tk.Button(northPanel,text= "xoa",image=icon_delete)
    xoa.pack(side=tk.LEFT,padx=10, pady=10)

    sua = tk.Button(northPanel,text= "sua",image=icon_detail)
    sua.pack(side=tk.LEFT,padx=10, pady=10)

    chitiet = tk.Button(northPanel,text= "chi tiet",image=icon_info)
    chitiet.pack(side=tk.LEFT,padx=10, pady=10)
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
# infor()

print(os.path.abspath("src/icon/add.png"))