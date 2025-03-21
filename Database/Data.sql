-- Tạo database và sử dụng nó
CREATE DATABASE IF NOT EXISTS FaceRecognition;
USE FaceRecognition;

-- Tạo bảng Students
CREATE TABLE IF NOT EXISTS Students (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    major VARCHAR(255),
    standing VARCHAR(50),
    year INT,
    starting_year INT,
    total_attendance INT DEFAULT 0,
    last_attendance_time DATETIME,
    image LONGBLOB
);

-- Chèn dữ liệu mẫu
-- Chèn dữ liệu mẫu cho 4 sinh viên
# drop table Students;
INSERT INTO Students (id, name, major, standing, year, starting_year, total_attendance, last_attendance_time, image)
VALUES
    (1, 'Nguyen Thanh Hien', 'Computer Science', 'Senior', 2023, 2020, 0, NOW(), NULL),
    (2, 'Nguyen Hoang Anh', 'Data Science', 'Junior', 2024, 2021, 0, NOW(), NULL),
    (3, 'Nguyen Thanh Nhan', 'Artificial Intelligence', 'Sophomore', 2025, 2022, 0, NOW(), NULL),
    (4, 'Huynh Thanh Hai', 'Cybersecurity', 'Freshman', 2026, 2023, 0, NOW(), NULL);


-- Kiểm tra dữ liệu
SELECT * FROM Students;
SELECT * FROM Students WHERE id = '4';
