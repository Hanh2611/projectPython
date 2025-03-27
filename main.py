import configparser
import customtkinter as ctk # tụi m tải thư viện này do cái này code nhìn đẹp đỡ tật
from tkinter import messagebox # cái này nữa
from PIL import Image
import cv2
import pickle
import face_recognition
import numpy as np
import sys
import os

from src.DAO.database import get_student_image, update_attendance, get_student_info
from customtkinter import CTkImage  # Sử dụng để tạo đối tượng ảnh tương thích HighDPI

# -------------------------------
# 1) ĐỊNH NGHĨA BẢNG MÀU (THEME)
# -------------------------------

COLORS = {
    "dark": "#1F1F1F",       # Màu tối
    "navy": "#1F314F",       # Màu xanh navy
    "teal": "#129E9B",       # Màu teal
    "mint": "#9BE3D9",       # Màu mint
    "white_gray": "#F4F4F4", # Màu xám trắng
    # Màu cho nút
    "btn_normal": "#2ecc71",   # Xanh lá (bình thường)
    "btn_hover": "#27ae60",    # Xanh lá đậm hơn khi hover
    "btn_active": "#000000",   # Đen khi nhấn
    # Khung khuôn mặt (OpenCV sử dụng BGR)
    "face_main": (0, 255, 0),    # Xanh lá (dùng cho mặt đứa nào vào chính giữa cái cam)
    "face_other": (200, 200, 200)  # Xám (cho nhân vật phụ )
}

# -------------------------------
# 2) ĐỊNH NGHĨA ĐƯỜNG DẪN FILE MÃ HÓA
# -------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
encoding_file_path = os.path.join(base_dir, "Encodings", "EncodeFile.p")
if not os.path.exists(encoding_file_path):
    raise FileNotFoundError(f"Không tìm thấy file mã hóa tại: {encoding_file_path}")
with open(encoding_file_path, 'rb') as file:
    encodedListKnown, studentIds = pickle.load(file)

# -------------------------------
# 3) LỚP ỨNG DỤNG CUSTOMTKINTER
# -------------------------------
class FaceAttendanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Attendance")
        self.geometry("1100x600")
        self.resizable(False, False)

        # Biến kiểm soát
        self.running = False
        self.current_id = None
        self.studentInfo = None
        self.confirmation_shown = False

        # -------------------------------
        # Frame bên trái: hiển thị video từ camera
        # -------------------------------
        self.left_frame = ctk.CTkFrame(self, width=640, height=480, fg_color=COLORS["dark"])
        self.left_frame.pack(side="left", padx=10, pady=10)
        self.left_frame.pack_propagate(False) # Ngăn frame tự động điều chỉnhh

        # Frame bên phải: hiển thị thông tin sinh viên
        self.right_frame = ctk.CTkFrame(self, width=400, height=480, fg_color=COLORS["white_gray"])
        self.right_frame.pack(side="right", padx=10, pady=10)
        self.right_frame.pack_propagate(False)

        # -------------------------------
        # Nút "Tiến hành nhận diện khuôn mặt" (bên trái)
        # -------------------------------
        self.start_button = ctk.CTkButton(
            self.left_frame,
            text="Tiến hành nhận diện khuôn mặt",
            font=("Arial", 14),
            fg_color=COLORS["teal"],
            text_color="black",
            hover_color=COLORS["btn_hover"],
            corner_radius=5,
            command=self.start_recognition
        )
        self.start_button.pack(pady=10)

        # Label hiển thị video (bên trái)
        self.video_label = ctk.CTkLabel(self.left_frame, text="", fg_color=COLORS["dark"])
        self.video_label.pack()

        # -------------------------------
        # PANEL XÁC NHẬN (ẩn ban đầu) – sẽ xuất hiện với hiệu ứng animation
        # -------------------------------
        self.confirmation_frame = ctk.CTkFrame(
            self.left_frame,
            width=300,
            height=100,
            fg_color=COLORS["white_gray"],
            corner_radius=5
        )
        self.question_label = ctk.CTkLabel(
            self.confirmation_frame,
            text="Thông tin này có phải của bạn không?",
            font=("Arial", 14),
            text_color="black",
            fg_color=COLORS["white_gray"]
        )
        self.question_label.pack(pady=5)
        self.yes_button = ctk.CTkButton(
            self.confirmation_frame,
            text="ĐÚNG",
            font=("Arial", 14),
            fg_color=COLORS["btn_normal"],
            text_color="white",
            hover_color=COLORS["btn_hover"],
            corner_radius=10,
            command=self.on_yes_clicked
        )
        self.yes_button.pack(side="left", padx=10, pady=10)
        self.no_button = ctk.CTkButton(
            self.confirmation_frame,
            text="KHÔNG",
            font=("Arial", 14),
            fg_color=COLORS["white_gray"],
            text_color="black",
            hover_color=COLORS["mint"],
            corner_radius=10,
            command=self.on_no_clicked
        )
        self.no_button.pack(side="left", padx=10, pady=10)
        # Ban đầu, panel xác nhận không hiển thị

        # -------------------------------
        # Các widget thông tin sinh viên (bên phải)
        # -------------------------------
        self.info_label = ctk.CTkLabel(
            self.right_frame,
            text="Thông tin nhận diện",
            font=("Arial", 20, "bold"),
            fg_color=COLORS["white_gray"],
            text_color="black"
        )
        self.info_label.pack(pady=5)

        # Sử dụng CTkTextbox thay cho tk.Text để hiển thị thông tin (không dùng bg)
        self.details_text = ctk.CTkTextbox(
            self.right_frame,
            width=400,
            height=180,
            font=("Courier New", 16, "bold"),
            text_color="black",
            fg_color=COLORS["teal"],
            corner_radius=10
        )
        self.details_text.pack(pady=5)
        self.details_text.configure(state="disabled") # Chỉ được đọc

        self.student_img_label = ctk.CTkLabel(self.right_frame, text="", fg_color=COLORS["white_gray"])
        self.student_img_label.pack(pady=5)

        # Khởi tạo camera
        self.cap = None

    # ================================
    # HÀM XỬ LÝ NHẬN DIỆN & CAMERA
    # ================================
    def start_recognition(self):
        """Ẩn nút Start, mở camera và bắt đầu nhận diện."""
        self.start_button.pack_forget()
        self.confirmation_shown = False
        self.running = True
        self.cap = cv2.VideoCapture(0) #
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.update_frame()

    def update_frame(self):
        """Cập nhật video và thực hiện nhận diện khuôn mặt."""
        if self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # Vì làm nhỏ hình làm tăng thời gian chạy nên giảm xuống 1/4
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                match_index = None
                matches = []
                if face_locations and encodings:
                    encode_face = encodings[0]
                    matches = face_recognition.compare_faces(encodedListKnown, encode_face)
                    face_distances = face_recognition.face_distance(encodedListKnown, encode_face)
                    match_index = np.argmin(face_distances)

                    if matches[match_index]:
                        detected_id = studentIds[match_index]
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

                # Vẽ khung cho tất cả các khuôn mặt
                for i, (top, right, bottom, left) in enumerate(face_locations):
                    top, right, bottom, left = top*4, right*4, bottom*4, left*4 # Tăng lại 1/4 do lúc nãy giảm
                    if match_index is not None and i == match_index and matches[match_index]:
                        color = COLORS["face_main"]
                    else:
                        color = COLORS["face_other"]
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                # Hiển thị khung hình trên label sử dụng CTkImage
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                ctk_img = CTkImage(light_image=img, size=(640, 480))
                self.video_label.configure(image=ctk_img) # hiển thị ảnh lên widget(widget là các thành phần giao diện mà người dùng tương tác, chẳng hạn như nút bấm, ô nhập liệu, nhãn, ...)
                self.video_label.image = ctk_img  # Lưu tham chiếu để tránh bị thu gom rác (python có cơ chế dọn rác gì đó nên cài này để giữ ảnh hiển thị )

            self.after(10, self.update_frame)
        else:
            if self.cap:
                self.cap.release()

    def display_student_info(self):
        """Hiển thị thông tin sinh viên (bên phải) và kích hoạt panel xác nhận với animation."""
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", ctk.END) #sẽ xóa sạch toàn bộ văn bản có trong self.details_text trước khi chèn nội dung mới.

        if not self.studentInfo:
            # Nếu self.studentInfo là None hoặc rỗng
            text_content = "Không có thông tin"
        else:
            # Tạo list cặp (key, value) mục đích là để căn giữa như khi chạy chứ ko bị căn lề trái
            info_data = [
                ("ID:", str(self.current_id) if self.current_id else "Unknown"),
                ("Name:", self.studentInfo.get("name", "Unknown")),
                ("Major:", self.studentInfo.get("major", "Unknown")),
                ("Attendance:", str(self.studentInfo.get("total_attendance", 0))),
                ("Year:", str(self.studentInfo.get("year", ""))),
                ("Starting Year:", str(self.studentInfo.get("starting_year", ""))),
                ("Standing:", self.studentInfo.get("standing", ""))
            ]

            # Tính độ dài cột key
            max_key_len = max(len(key) for key, value in info_data)

            # Định dạng
            formatted_lines = []
            for key, value in info_data:
                line = f"{key:<{max_key_len}}  {value}"
                formatted_lines.append(line)

            text_content = "\n".join(formatted_lines)
            # Chèn vào CTkTextbox
        self.details_text.insert(ctk.END, text_content)
        self.details_text.configure(state="disabled")

        stu_img = get_student_image(self.current_id) if self.current_id else None
        if stu_img is not None:
            stu_img = cv2.cvtColor(stu_img, cv2.COLOR_BGR2RGB)
            stu_img = cv2.resize(stu_img, (200, 200))
            img_pil = Image.fromarray(stu_img) # do cv2 với cái Tkinter (PhotoImage) hoặc CustomTkinter (CTkImage) thể hiện hình ảnh khac nhau nên có câu lệnh này để chuyển giống như đổi dữ liệu của biến
            ctk_img_student = CTkImage(light_image=img_pil, size=(200, 200))
            self.student_img_label.configure(image=ctk_img_student)
            self.student_img_label.image = ctk_img_student
        else:
            self.student_img_label.configure(image="", text="No Image")

        # Kích hoạt panel xác nhận với hiệu ứng animation từ dưới lên
        if not self.confirmation_shown:
            self.confirmation_shown = True
            self.show_confirmation_animated()

    # ================================
    # ANIMATION CHO PANEL XÁC NHẬN
    # ================================
    def show_confirmation_animated(self):
        """Panel xác nhận 'trượt' từ dưới lên trong 1 giây.(nút đúng ko của cái xác nhận )"""
        start_y = 600
        target_y = 390
        steps = 50 # cái này càng lớn thì chạy càng mượt mà bù lại nó chậm
        delta = (target_y - start_y) / steps
        delay = (1000 // steps)

        self.confirmation_frame.place(in_=self.left_frame, x=170, y=start_y)

        def animate(step=0, current_y=start_y): # Khi hàm được gọi lại, step sẽ tăng dần và current_y sẽ cập nhật theo vị trí mới.
            if step < steps:
                new_y = current_y + delta
                self.confirmation_frame.place_configure(y=new_y)
                self.after(delay, lambda: animate(step+1, new_y))
            else:
                self.confirmation_frame.place_configure(y=target_y)

        animate()

    def on_yes_clicked(self):
        """Khi người dùng chọn 'ĐÚNG': cập nhật điểm danh và reset giao diện."""
        if self.current_id:
            update_attendance(self.current_id)
            messagebox.showinfo("Thông báo", f"Điểm danh thành công cho ID {self.current_id}!")
        else:
            messagebox.showwarning("Cảnh báo", "Không có thông tin nhận diện.")
        self.reset_ui()

    def on_no_clicked(self):
        """Khi người dùng chọn 'KHÔNG': chỉ reset giao diện."""
        self.reset_ui()

    # ================================
    # RESET GIAO DIỆN
    # ================================
    def reset_ui(self):
        """Reset giao diện: dừng camera, ẩn panel xác nhận, xóa thông tin hiển thị và hiển thị lại nút Start."""
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.video_label.configure(image="", text="")
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", ctk.END)
        self.details_text.configure(state="disabled")
        self.student_img_label.configure(image="", text="")
        self.confirmation_frame.place_forget()
        self.current_id = None
        self.studentInfo = None
        self.confirmation_shown = False
        self.start_button.pack(pady=10)

if __name__ == '__main__':
    app = FaceAttendanceApp()
    app.mainloop()
