from customtkinter import *
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from PIL import Image
import os

# Biến màu tối
primaryClr = "#6D54B5"
secondaryCrl = "#3C364C"  # Nền btn
accentClr = "#757283"  # Placeholder btn
bgClr = "#2c2736"
textClr = "#FFFFFF"
borderClr = "#000000"

imgReferences = {}

# Hàm crop theo bottom ảnh
def bottomCrop(img, tempWidth, tempHeight, bias=0.7):
    w, h = img.size
    left = (w - tempWidth) // 2
    top = int((h - tempHeight) * bias)
    right = left + tempWidth
    bottom = top + tempHeight
    return img.crop((left, top, right, bottom))

# Scale ảnh
def resizeImg(frame, imgLabel, imgPath):
    w = frame.winfo_width()
    h = frame.winfo_height()

    if w > 1 and h > 1:
        img = Image.open(imgPath)
        ratio = w / h
        img_ratio = img.width / img.height

        if img_ratio > ratio:
            crop_w = int(img.height * ratio)
            crop_h = img.height
        else:
            crop_w = img.width
            crop_h = int(img.width / ratio)

        img = bottomCrop(img, crop_w, crop_h)
        frameId = str(frame)
        imgReferences[frameId] = CTkImage(light_image=img, size=(w, h))
        imgLabel.configure(image=imgReferences[frameId])


# Kiểm tra trường nhập có null hay không
def checknull(entries):
    nullEntry = [entry for entry in entries if not entry.get().strip()]
    if nullEntry:
        CTkMessagebox(title="Lỗi", message="Bạn cần phải điền đầy đủ thông tin")
    else:
        CTkMessagebox(title="Thành công", message="Bạn đã đăng nhập thành công")


def loginFrame():
    loginPanel = CTk()
    loginPanel.geometry("1120x630")
    loginPanel._set_appearance_mode("light")
    loginPanel.configure(fg_color=textClr)

    body = CTkFrame(loginPanel, fg_color=bgClr)
    body.place(relwidth=1, relheight=1)
    body.grid_rowconfigure(0, weight=1)
    body.grid_columnconfigure(0, weight=1)
    body.grid_columnconfigure(1, weight=1)

    left = CTkFrame(body)
    left.grid(row=0, column=0, sticky="nsew")

    right = CTkFrame(body, fg_color="transparent")
    right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    right.grid_rowconfigure(0, weight=1)
    right.grid_columnconfigure(0, weight=1)

    innerRight = CTkFrame(right, fg_color=bgClr)
    innerRight.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    innerRight.grid_columnconfigure(0, weight=1)
    innerRight.grid_rowconfigure(0, weight=0)
    innerRight.grid_rowconfigure(1, weight=1)

    headRight = CTkFrame(innerRight, fg_color=bgClr)
    headRight.grid(row=0, column=0, padx=80, pady=10, sticky="w")

    title = CTkLabel(headRight,
                     text="Đàn em anh hải",
                     text_color=textClr,
                     font=("San Serif", 36, "bold"))
    title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    slogan = CTkLabel(headRight,
                      text=f'Hôm nay là {datetime.now().strftime("%d/%m/%Y")}, bạn đã điểm danh chưa !!!',
                      text_color=accentClr,
                      font=("San Serif", 14, "bold"))
    slogan.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    footRight = CTkFrame(innerRight, fg_color=bgClr)
    footRight.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    footRightFrame = CTkFrame(footRight, fg_color=bgClr)
    footRightFrame.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8, relheight=0.3)
    footRightFrame.grid_rowconfigure(0, weight=1, minsize=40)
    footRightFrame.grid_rowconfigure(1, weight=1, minsize=40)
    footRightFrame.grid_rowconfigure(2, weight=1)
    footRightFrame.grid_columnconfigure(0, weight=1)

    usernameTxt = CTkEntry(footRightFrame,
                           placeholder_text="Nhập email hoặc username ....",
                           font=("San Serif", 14, "bold"),
                           border_width=0,
                           fg_color=secondaryCrl,
                           text_color=accentClr)
    usernameTxt.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    passwordTxt = CTkEntry(footRightFrame,
                           placeholder_text="Nhập mật khẩu .....",
                           font=("San Serif", 14, "bold"),
                           border_width=0,
                           fg_color=secondaryCrl,
                           text_color=accentClr)
    passwordTxt.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    loginBtn = CTkButton(footRightFrame,
                         text="Đăng nhập",
                         font=("San Serif", 18, "bold"),
                         fg_color=primaryClr,
                         border_spacing=5,
                         command=lambda: checknull([usernameTxt, passwordTxt]))
    loginBtn.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    imgLabel = CTkLabel(left,
                        text="",
                        image=None)
    imgLabel.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    # Get absolute path to the background image
    base_dir = os.path.dirname(os.path.abspath(__file__))
    imgPath = os.path.join(base_dir, "..", "..", "Resources", "photo", "background.jpg")

    def on_resize(event):
        resizeImg(left, imgLabel, imgPath)

    left.bind("<Configure>", on_resize)
    loginPanel.update()
    resizeImg(left, imgLabel, imgPath)
    return loginPanel

a = loginFrame().mainloop()