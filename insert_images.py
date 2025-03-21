import mysql.connector

# Kết nối đến MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="FaceRecognition"
)
cursor = conn.cursor()

# Danh sách sinh viên và ảnh tương ứng
students = [
    (1, "Images/1.png"),
    (2, "Images/2.png"),
    (3, "Images/3.png"),
    (4, "Images/4.png"),
]

for student_id, image_path in students:
    try:
        with open(image_path, "rb") as file:
            binary_data = file.read()
            cursor.execute("UPDATE Students SET image = %s WHERE id = %s", (binary_data, student_id))
            print(f"Đã chèn ảnh cho sinh viên ID {student_id}")
    except FileNotFoundError:
        print(f"Không tìm thấy ảnh: {image_path}")

# Lưu thay đổi và đóng kết nối
conn.commit()
cursor.close()
conn.close()
print(" Hoàn tất chèn ảnh vào database!")
