import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="FaceRecognition"
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Các bảng trong database:", tables)
except mysql.connector.Error as err:
    print("Lỗi kết nối:", err)
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
