import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-ad7d1-default-rtdb.firebaseio.com/",
    # 'storageBucket': ""
})

# bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
# imgStudent = []

current_id = None  # ID của người đang hiển thị
display_info = False  # Cờ báo hiệu hiển thị thông tin

while True:
    success, img = cap.read()
    if not success or img is None:
        print("Không thể lấy khung hình từ camera")
        continue

    # Tiền xử lý ảnh
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Cập nhật background
    imgBackgroundCopy = imgBackground.copy()
    imgBackgroundCopy[162:162 + 480, 55:55 + 640] = img

    # Nếu có khuôn mặt
    if faceCurFrame:
        # Ở đây ta chỉ xét khuôn mặt đầu tiên (hoặc có thể lặp qua tất cả nếu muốn)
        encodeFace = encodeCurFrame[0]
        faceLoc = faceCurFrame[0]

        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            detected_id = studentIds[matchIndex]
            # Nếu người nhận diện khác với người hiện đang hiển thị hoặc chưa có người nào được hiển thị
            if current_id is None or detected_id != current_id:
                current_id = detected_id
                display_info = True
                # Lấy dữ liệu từ Firebase cho người mới
                peopleInfo = db.reference(f'People/{current_id}').get()
                # Cập nhật thông tin điểm danh (nếu cần thiết, ví dụ kiểm tra thời gian)
                datetimeObject = datetime.strptime(peopleInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                if secondsElapsed > 30:
                    ref = db.reference(f'People/{current_id}')
                    peopleInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(peopleInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Vẽ khung khuôn mặt
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackgroundCopy = cvzone.cornerRect(imgBackgroundCopy, bbox, rt=0)

        else:
            # Nếu khuôn mặt không khớp, reset hiển thị
            current_id = None
            display_info = False
    else:
        # Nếu không có khuôn mặt nào, reset
        current_id = None
        display_info = False

    # Hiển thị mode và thông tin người được nhận diện
    if display_info and current_id is not None:
        # Ví dụ: chọn mode hiển thị thông tin (ví dụ: modeType = 1)
        modeType = 1
        imgBackgroundCopy[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        # Hiển thị thông tin (các thông tin có thể tùy chỉnh vị trí và kiểu chữ)
        cv2.putText(imgBackgroundCopy, str(peopleInfo['total_attendance']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(imgBackgroundCopy, str(peopleInfo['major']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackgroundCopy, str(current_id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackgroundCopy, str(peopleInfo['standing']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackgroundCopy, str(peopleInfo['year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackgroundCopy, str(peopleInfo['starting_year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

        (w, h), _ = cv2.getTextSize(peopleInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imgBackgroundCopy, str(peopleInfo['name']), (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
    else:
        # Nếu không có thông tin, có thể hiển thị mode mặc định
        modeType = 0
        imgBackgroundCopy[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    cv2.imshow("Face Attendance", imgBackgroundCopy)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
