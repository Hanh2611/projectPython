import cv2
import face_recognition
import pickle
import os

# Đọc ảnh nền (có thể dùng cho giao diện, không ảnh hưởng đến mã hoá khuôn mặt)
imgBackground = cv2.imread('Resources/background.png')
folderPath = 'Images'
pathList = os.listdir(folderPath)
print("Danh sách ảnh:", pathList)
imgList = []
peopleIds = []

for path in pathList:
    img = cv2.imread(os.path.join(folderPath, path))
    if img is not None:
        imgList.append(img)
        peopleIds.append(os.path.splitext(path)[0])

def findEncodings(imagesList):
    encodeList = []
    for i, img in enumerate(imagesList, start=1):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img_rgb)
        print(f"Đang xử lý ảnh thứ {i}")
        if encodes:
            encodeList.append(encodes[0])
    return encodeList

print("Bắt đầu mã hoá khuôn mặt ...")
encodeListKnown = findEncodings(imgList)
encodeListWithIds = [encodeListKnown, peopleIds]
print("Mã hoá hoàn tất!")

# Lưu file mã hoá vào thư mục Encodings
with open("Encodings/EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListWithIds, file)
print("File mã hoá đã được lưu tại Encodings/EncodeFile.p")
