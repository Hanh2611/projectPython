import mysql.connector
import numpy as np
import cv2
from datetime import datetime
import configparser

import os

config = configparser.ConfigParser()

# Xác định đường dẫn tuyệt đối
config_path = os.path.join(os.path.dirname(__file__), "..", "..", "Resources", "config.properties")
config_path = os.path.abspath(config_path)

if not os.path.exists(config_path):
    raise FileNotFoundError(f"Không tìm thấy file cấu hình tại: {config_path}")

config.read(config_path)


# In ra các sections có trong file
print("Sections:", config.sections())

# Kiểm tra nếu 'host' không tồn tại
if not config.has_option("DEFAULT", "host"):
    raise KeyError("Không tìm thấy 'host' trong file cấu hình!")

conn = mysql.connector.connect(
    host=config.get("DEFAULT", "host"),
    user=config.get("DEFAULT", "user"),
    password=config.get("DEFAULT", "password"),
    database=config.get("DEFAULT", "database"),
)

cursor = conn.cursor(dictionary=True)


def get_student_info(student_id):
    """Lấy thông tin sinh viên từ MySQL"""
    cursor.execute("SELECT * FROM Students WHERE id = %s", (student_id,))
    return cursor.fetchone()

def get_student_image(student_id):
    """Lấy ảnh sinh viên từ MySQL (nếu có)"""
    cursor.execute("SELECT image FROM Students WHERE id = %s", (student_id,))
    result = cursor.fetchone()
    if result and result["image"]:
        img_array = np.frombuffer(result["image"], np.uint8)
        return cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return None


def update_attendance(student_id):
    """Cập nhật số lần điểm danh và thời gian điểm danh mới vào MySQL"""
    cursor.execute("SELECT last_attendance_time FROM Students WHERE id = %s", (student_id,))
    result = cursor.fetchone()
    if result and result["last_attendance_time"]:
        last_time = result["last_attendance_time"]
        seconds_elapsed = (datetime.now() - last_time).total_seconds()
    else:
        seconds_elapsed = float('inf')

    if seconds_elapsed > 30:  # Giới hạn cập nhật mỗi 30 giây
        cursor.execute(
            "UPDATE Students SET total_attendance = total_attendance + 1, last_attendance_time = %s WHERE id = %s",
            (datetime.now(), student_id)
        )
        conn.commit()



