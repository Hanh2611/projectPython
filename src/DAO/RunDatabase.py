import mysql.connector
import configparser

# Đọc file config
config = configparser.ConfigParser()
config.read("Resources/config.properties")

try:
    conn = mysql.connector.connect(
        host = config.get("DEFAULT", "host"),
        user=config.get("DEFAULT", "user"),
        password=config.get("DEFAULT", "password"),
        database=config.get("DEFAULT", "database")
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    print("Các bảng trong database:", tables)
except mysql.connector.Error as err:
    print("Lỗi kết nối:", err)
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
