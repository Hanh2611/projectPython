from tkinter import *

def dang_nhap():
    lg = Tk()
    lg.geometry("500x200")
    lg.title("Đăng nhập")

    name = Label(lg, text="Tên đăng nhập: ", fg="black", font=("Arial", 18, "bold"),).grid(row=0, column=0, padx=10, pady=10)

    nameEntry = Entry(lg, fg="black", font=("Arial", 15, "bold"), bd=2, relief="ridge").grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=2)

    password = Label(lg, text="Mật khẩu", fg="black", font=("Arial", 18, "bold")).grid(row=1, column=0, padx=10, pady=10)

    passwordEntry = Entry(lg, fg="black", font=("Arial", 15, "bold"), relief="ridge", show='*').grid(row=1, column=1, padx=10, pady=10, ipadx=5, ipady=2)

    signin = Button(lg, text="Đăng nhập", fg="white", bg="green", activebackground="red", font=("Arial", 14, "bold"),width=15).grid(row=2, column=0, columnspan=1)
    lg.mainloop()

dang_nhap()