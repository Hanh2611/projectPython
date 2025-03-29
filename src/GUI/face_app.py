import os
import pickle
import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageDraw
import customtkinter as ctk
from tkinter import messagebox
from customtkinter import CTkImage
from src.DAO.database import get_student_image, update_attendance, get_student_info

# COLORS lấy từ file colors.py
COLORS = {
    "dark": "#1F1F1F",
    "navy": "#1F314F",
    "teal": "#129E9B",
    "mint": "#9BE3D9",
    "white_gray": "#F4F4F4",
    "btn_normal": "#2ecc71",
    "btn_hover": "#27ae60",
    "btn_active": "#000000",
    "face_main": (0, 255, 0),
    "face_other": (200, 200, 200)
}


class ModernFaceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern Face Attendance")
        self.geometry("1000x600")
        self.resizable(False, False)

        # Biến kiểm soát
        self.running = False
        self.current_id = None
        self.studentInfo = None
        self.confirmation_shown = False

        # Đọc file mã hóa
        base_dir = os.path.dirname(os.path.abspath(__file__))
        encoding_file_path = os.path.join(base_dir, "..", "..", "Encodings", "EncodeFile.p")
        if not os.path.exists(encoding_file_path):
            raise FileNotFoundError(f"Không tìm thấy file mã hóa tại: {encoding_file_path}")
        with open(encoding_file_path, 'rb') as file:
            self.encodedListKnown, self.studentIds = pickle.load(file)

        # Nền tổng thể
        self.configure(fg_color=COLORS["white_gray"])

        # Khởi tạo camera
        self.cap = None

        # Tạo layout
        self.create_top_bar()
        self.create_left_area()
        self.create_right_area()
    def create_top_bar(self):
        """Thanh trên cùng."""
        self.top_bar = ctk.CTkFrame(self, width=1000, height=80, corner_radius=0,
                                    fg_color=COLORS["navy"])
        self.top_bar.place(x=0, y=0)

        self.title_label = ctk.CTkLabel(self.top_bar,
                                        text="ATTENDANCE SYSTEM",
                                        font=("Arial", 22, "bold"),
                                        text_color="white")
        self.title_label.place(x=20, y=20)

    # ================================
    # PHẦN BÊN TRÁI (CAMERA)
    # ================================
    def create_left_area(self):
        """Khu vực bên trái: frame + camera + panel xác nhận."""
        # Frame nền cho camera
        self.left_frame = ctk.CTkFrame(self, width=640, height=480,
                                       corner_radius=10,
                                       fg_color=COLORS["teal"])
        self.left_frame.place(x=20, y=100)

        # Nút start
        self.start_button = ctk.CTkButton(
            self.left_frame,
            text="START RECOGNITION",
            font=("Arial", 14, "bold"),
            fg_color=COLORS["btn_normal"],
            width=100, height=20,
            text_color="white",
            hover_color=COLORS["btn_hover"],
            corner_radius=20,
            command=self.start_recognition
        )
        # Đặt nút ở phía trên khung
        self.start_button.place(x=240, y=10)

        # Label hiển thị camera (mặc định nền tối)
        self.video_label = ctk.CTkLabel(self.left_frame,
                                        text="No Camera",
                                        width=600, height=400,
                                        fg_color="black")  # Mặc định tối
        self.video_label.place(x=20, y=60)

        # Panel xác nhận (ẩn ban đầu)
        self.confirmation_frame = ctk.CTkFrame(self.left_frame,
                                               width=300, height=100,
                                               corner_radius=10,
                                               fg_color=COLORS["white_gray"])
        self.question_label = ctk.CTkLabel(self.confirmation_frame,
                                           text="Thông tin này có phải của bạn không?",
                                           font=("Arial", 14),
                                           text_color="black")
        self.question_label.pack(pady=5)

        self.yes_button = ctk.CTkButton(self.confirmation_frame,
                                        text="ĐÚNG",
                                        font=("Arial", 14),
                                        fg_color=COLORS["btn_normal"],
                                        text_color="white",
                                        hover_color=COLORS["btn_hover"],
                                        corner_radius=10,
                                        command=self.on_yes_clicked)
        self.yes_button.pack(side="left", padx=10, pady=10)

        self.no_button = ctk.CTkButton(self.confirmation_frame,
                                       text="KHÔNG",
                                       font=("Arial", 14),
                                       fg_color=COLORS["white_gray"],
                                       text_color="black",
                                       hover_color=COLORS["mint"],
                                       corner_radius=10,
                                       command=self.on_no_clicked)
        self.no_button.pack(side="left", padx=10, pady=10)

    # ================================
    # CHỈNH SỬA BÊN PHẢI
    # ================================
    def create_right_area(self):

        self.right_frame = ctk.CTkFrame(self, width=300, height=480, fg_color=COLORS["white_gray"])
        self.right_frame.pack(side="left", padx=20, pady=10)
        self.right_frame.pack_propagate(False)
        self.right_frame.place(x=680, y=100)

        self.student_img_label = ctk.CTkLabel(
            self.right_frame,
            text="No Image",
            fg_color=COLORS["mint"],
            width=220,
            height=220,
            corner_radius=10
        )
        self.student_img_label.place(relx=0.5, y=10, anchor="n")

        # Nút ID
        self.id_button = ctk.CTkLabel(
            self.right_frame,
            text="ID:",
            font=("Arial", 16, "bold"),
            fg_color=COLORS["teal"],
            text_color="black",
            corner_radius=30,
            width=200,
            height=40
        )
        self.id_button.place(relx=0.5, y=260, anchor="center")

        # Nút Major
        self.major_button = ctk.CTkLabel(
            self.right_frame,
            text="Major:",
            font=("Arial", 16, "bold"),
            fg_color=COLORS["teal"],
            text_color="black",
            corner_radius=30,
            width=200,
            height=40
        )
        self.major_button.place(relx=0.5, y=310, anchor="center")

        # Textbox hiển thị thêm thông tin (Attendance, Year, Standing...)
        self.info_text = ctk.CTkTextbox(
            self.right_frame,
            width=300,
            height=120,
            font=("Courier New", 14),
            fg_color=COLORS["mint"],
            text_color="black",
            corner_radius=10
        )
        self.info_text.place(relx=0.5, y=360, anchor="n")
        self.info_text.configure(state="disabled")

    # ================================
    # CAMERA & NHẬN DIỆN
    # ================================
    def start_recognition(self):
        self.start_button.place_forget()
        self.confirmation_shown = False
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.update_frame()

    def update_frame(self):
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("Không thể đọc frame từ camera.")
                self.video_label.configure(text="CAMERA ERROR")
            else:
                frame = cv2.flip(frame, 1)
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                match_index = None
                matches = []

                threshold = 0.5

                if face_locations and encodings:
                    encode_face = encodings[0]
                    matches = face_recognition.compare_faces(self.encodedListKnown, encode_face)
                    face_distances = face_recognition.face_distance(self.encodedListKnown, encode_face)
                    match_index = np.argmin(face_distances)


                    if matches[match_index] and face_distances[match_index] < threshold:
                        detected_id = self.studentIds[match_index]
                        if self.current_id != detected_id:
                            self.current_id = detected_id
                            self.studentInfo = get_student_info(self.current_id)
                            if self.studentInfo is None:
                                self.studentInfo = {
                                    "name": "Unknown",
                                    "major": "Unknown",
                                    "total_attendance": 0,
                                    "standing": "",
                                    "year": "",
                                    "starting_year": ""
                                }
                            self.display_student_info()
                    else:
                        # Nếu không đạt ngưỡng, coi như không nhận diện được khuôn mặt
                        self.current_id = None
                        self.studentInfo = {
                            "name": "Unknown",
                            "major": "Unknown",
                            "total_attendance": 0,
                            "standing": "",
                            "year": "",
                            "starting_year": ""
                        }
                        self.display_student_info()

                # Vẽ khung cho các khuôn mặt
                for i, (top, right, bottom, left) in enumerate(face_locations):
                    top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
                    if match_index is not None and i == match_index and matches[match_index]:
                        color = COLORS["face_main"]
                    else:
                        color = COLORS["face_other"]
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                # Hiển thị camera
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(rgb_frame)
                ctk_img = CTkImage(light_image=img_pil, size=(600, 400))
                self.video_label.configure(image=ctk_img, text="")
                self.video_label.image = ctk_img

            self.after(10, self.update_frame)
        else:
            if self.cap:
                self.cap.release()

    # ================================
    # HIỂN THỊ THÔNG TIN
    # ================================
    def display_student_info(self):

        # 1) Cập nhật ID, Major
        if self.studentInfo:
            self.id_button.configure(text=f"ID: {self.current_id}")
            self.major_button.configure(text=f"Major: {self.studentInfo.get('major','Unknown')}")
        else:
            self.id_button.configure(text="ID: ???")
            self.major_button.configure(text="Major: ???")

        # 2) Ảnh
        stu_img = get_student_image(self.current_id) if self.current_id else None
        if stu_img is not None:
            stu_img = cv2.cvtColor(stu_img, cv2.COLOR_BGR2RGB)
            stu_img = cv2.resize(stu_img, (210, 210), interpolation=cv2.INTER_AREA)
            img_pil = Image.fromarray(stu_img)

            size = (210, 210)
            corner_radius = 20
            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, size[0], size[1]), radius=corner_radius, fill=255)

            # Thêm kênh alpha vào ảnh
            img_pil.putalpha(mask)
            ctk_img_student = CTkImage(light_image=img_pil, size=size)
            self.student_img_label.configure(image=ctk_img_student, text="")
            self.student_img_label.image = ctk_img_student
        else:
            self.student_img_label.configure(image=None, text="No Image")

        # 3) Thêm thông tin vào info_text
        info_lines = []
        if not self.studentInfo:
            info_lines.append("Không có thông tin")
        else:
            # Danh sách key-value của thông tin sinh viên
            info_data = [
                ("Name:", self.studentInfo.get("name", "Unknown")),
                ("Attendance:", str(self.studentInfo.get("total_attendance", 0))),
                ("Standing:", self.studentInfo.get("standing", "")),
                ("Year:", self.studentInfo.get("year", "")),
                ("Starting Year:", self.studentInfo.get("starting_year", ""))
            ]
            max_key_len = max(len(key) for key, _ in info_data)

            formatted_lines = [f"{key:<{max_key_len}} {value}" for key, value in info_data]

            info_lines = "\n".join(formatted_lines)

        # Xóa nội dung cũ trước khi chèn nội dung mới
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", ctk.END)
        self.info_text.insert(ctk.END, info_lines)
        self.info_text.configure(state="disabled")

        # Hiển thị panel xác nhận (nếu chưa hiện)
        if not self.confirmation_shown:
            self.confirmation_shown = True
            self.show_confirmation_animated()

    # ================================
    # ANIMATION
    # ================================
    def show_confirmation_animated(self):
        start_y = 480
        target_y = 400
        steps = 50
        delta = (target_y - start_y) / steps
        delay = 50 // steps

        self.confirmation_frame.place(x=160, y=start_y)

        def animate(step=0, current_y=start_y):
            if step < steps:
                new_y = current_y + delta
                self.confirmation_frame.place_configure(y=new_y)
                self.after(delay, lambda: animate(step+1, new_y))
            else:
                self.confirmation_frame.place_configure(y=target_y)

        animate()

    def on_yes_clicked(self):
        if self.current_id:
            update_attendance(self.current_id)
            messagebox.showinfo("Thông báo", f"Điểm danh thành công cho ID {self.current_id}!")
        else:
            messagebox.showwarning("Cảnh báo", "Không có thông tin nhận diện.")
        self.reset_ui()

    def on_no_clicked(self):
        self.reset_ui()

    # ================================
    # RESET GIAO DIỆN
    # ================================
    def reset_ui(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        # Nền tối camera
        self.video_label.configure(image="", text="")
        # Reset info
        self.student_img_label.configure(image="", text="")
        self.id_button.configure(text="ID:")
        self.major_button.configure(text="Major:")
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", ctk.END)
        self.info_text.configure(state="disabled")
        # Ẩn panel
        self.confirmation_frame.place_forget()
        self.current_id = None
        self.studentInfo = None
        self.confirmation_shown = False
        self.start_button.place(x=240, y=10)  # Cho nút quay lại

if __name__ == "__main__":
    app = ModernFaceApp()
    app.mainloop()
