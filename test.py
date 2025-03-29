import customtkinter as ctk
from PIL import Image, ImageTk
import os

# Nếu muốn, bạn có thể import COLORS từ file colors.py
# from src.GUI.colors import COLORS

# Tạo 1 màu tím ví dụ (bạn có thể thay bằng COLORS["navy"] hay COLORS["teal"] tuỳ ý)
PURPLE = "#9b59b6"
WHITE = "#ffffff"
LIGHT_GRAY = "#f4f4f4"

class AttendanceUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Attendance System")
        self.geometry("1000x600")
        self.resizable(False, False)

        # Toàn bộ cửa sổ nền trắng
        self.configure(fg_color=WHITE)

        # 1) Thanh trên (chứa icon + text "ATTENDANCE SYSTEM")
        self.create_top_bar()

        # 2) Khung bên trái (hiển thị ảnh)
        self.create_left_frame()

        # 3) Khung bên phải (thông tin)
        self.create_right_frame()

    def create_top_bar(self):
        """Thanh trên cùng, màu tím, chứa icon và text."""
        # Frame trên cùng
        self.top_bar = ctk.CTkFrame(self, width=1000, height=80, corner_radius=0, fg_color=PURPLE)
        self.top_bar.place(x=0, y=0)

        # Icon (nếu có file icon, bạn có thể load -> CTkImage -> Label)
        # Tạm thời demo 1 khung tròn:
        self.icon_label = ctk.CTkLabel(self.top_bar, text="", width=50, height=50,
                                       corner_radius=25, fg_color=WHITE)
        self.icon_label.place(x=20, y=15)

        # Label "ATTENDANCE SYSTEM"
        self.title_label = ctk.CTkLabel(self.top_bar, text="ATTENDANCE SYSTEM",
                                        font=("Arial", 20, "bold"),
                                        text_color=WHITE)
        self.title_label.place(x=80, y=20)

    def create_left_frame(self):
        """Khung bên trái, màu tím, hiển thị ảnh (hoặc camera)."""
        self.left_frame = ctk.CTkFrame(self, width=600, height=520,
                                       corner_radius=20, fg_color=PURPLE)
        self.left_frame.place(x=20, y=90)

        # Ở đây bạn có thể hiển thị 1 ảnh background.png
        # Demo load ảnh (nếu bạn có background.png)
        img_path = os.path.join(os.path.dirname(__file__), "background.png")
        if os.path.exists(img_path):
            from customtkinter import CTkImage
            from PIL import Image
            bg_img = Image.open(img_path).resize((600, 520))
            ctk_bg_img = CTkImage(light_image=bg_img, size=(600, 520))
            self.bg_label = ctk.CTkLabel(self.left_frame, text="", image=ctk_bg_img)
            self.bg_label.place(x=0, y=0)
        else:
            # Nếu không có ảnh, tạo label placeholder
            self.bg_label = ctk.CTkLabel(self.left_frame, text="IMAGE HERE",
                                         text_color=WHITE,
                                         font=("Arial", 18, "bold"))
            self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

    def create_right_frame(self):
        """Khung bên phải (trắng), có thể hiển thị thông tin."""
        self.right_frame = ctk.CTkFrame(self, width=300, height=520,
                                        corner_radius=20, fg_color=LIGHT_GRAY)
        self.right_frame.place(x=640, y=90)

        # Demo: label placeholder
        placeholder_label = ctk.CTkLabel(self.right_frame, text="Thông tin\nsinh viên\n...",
                                         font=("Arial", 18),
                                         text_color="black")
        placeholder_label.place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    app = AttendanceUI()
    app.mainloop()
