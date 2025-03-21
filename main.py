import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
from datetime import datetime
from database import get_student_info, update_attendance, get_student_image

# Thiết lập camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Tải ảnh nền và các mode giao diện
imgBackground = cv2.imread('Resources/background.png')
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# Tải file mã hoá khuôn mặt từ thư mục Encodings
print("Đang tải file mã hoá khuôn mặt ...")
with open('Encodings/EncodeFile.p', 'rb') as file:
    encodeListKnown, studentIds = pickle.load(file)
print("File mã hoá đã được tải.")

modeType = 0
current_id = None  # ID người được nhận diện
display_info = False
studentInfo = None  # Thông tin sinh viên lấy từ MySQL

while True:
    success, img = cap.read()
    if not success or img is None:
        print("Không lấy được khung hình từ camera.")
        continue

    # Tiền xử lý ảnh: resize để tăng tốc xử lý
    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Phát hiện khuôn mặt và mã hoá
    faceLocations = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS, faceLocations)

    # Cập nhật background
    imgBackgroundCopy = imgBackground.copy()
    imgBackgroundCopy[162:162+480, 55:55+640] = img

    if faceLocations:
        encodeFace = encodeCurrentFrame[0]
        faceLoc = faceLocations[0]

        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDistances = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDistances)

        if matches[matchIndex]:
            detected_id = studentIds[matchIndex]


            # Nếu phát hiện được khuôn mặt mới
            if current_id != detected_id:
                current_id = detected_id
                display_info = True
                # Lấy thông tin sinh viên từ MySQL
                studentInfo = get_student_info(current_id)

                if studentInfo:
                    update_attendance(current_id)
                else:
                    print(f"Không tìm thấy thông tin cho ID {current_id}")
            # Vẽ khung quanh khuôn mặt
            y1, x2, y2, x1 = [v*4 for v in faceLoc]
            bbox = (55 + x1, 162 + y1, x2 - x1, y2 - y1)
            imgBackgroundCopy = cvzone.cornerRect(imgBackgroundCopy, bbox, rt=0)
        else:
            current_id = None
            display_info = False
    else:
        current_id = None
        display_info = False

    # Hiển thị thông tin sinh viên nếu có
    if display_info and current_id is not None and studentInfo:
        modeType = 1
        imgBackgroundCopy[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        # Hiển thị thông tin sinh viên
        cv2.putText(imgBackgroundCopy, str(studentInfo['total_attendance']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(imgBackgroundCopy, str(studentInfo['major']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(imgBackgroundCopy, str(current_id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(imgBackgroundCopy, str(studentInfo['standing']), (905, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (100, 100, 100), 1)
        cv2.putText(imgBackgroundCopy, str(studentInfo['year']), (1020, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 100, 100), 1)
        cv2.putText(imgBackgroundCopy, str(studentInfo['starting_year']), (1120, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (100, 100, 100), 1)

        # Canh giữa tên sinh viên
        (w, _), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imgBackgroundCopy, studentInfo['name'], (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        # 🎯 Hiển thị ảnh sinh viên từ MySQL nếu có
        student_img = get_student_image(current_id)  # Lấy ảnh từ database
        if student_img is not None:
            student_img_resized = cv2.resize(student_img, (216, 216))  # Resize ảnh về đúng kích thước
            imgBackgroundCopy[175:175 + 216, 909:909 + 216] = student_img_resized
        else:
            # Nếu không có ảnh, hiển thị placeholder hoặc thông báo
            cv2.putText(imgBackgroundCopy, "No Image", (960, 290),
                        cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    else:
        modeType = 0
        imgBackgroundCopy[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    cv2.imshow("Face Attendance", imgBackgroundCopy)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
