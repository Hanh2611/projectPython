import cv2
import face_recognition
import face_recognition_models
import pickle
import os

# Importing people images
imgBackground = cv2.imread('Resources/background.png')
folderPath = 'Images'
pathList = os.listdir(folderPath)
print (pathList)
imgList = []
peopleIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    peopleIds.append(os.path.splitext(path)[0])
# print(len(imgList))


def findEncodings(imagesList):
    enCodeList = []
    i = 0
    for img in imagesList:
        image = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        i += 1
        print(i)
        if len(encode) > 0:

            enCodeList.append(encode[0])

    return enCodeList
print("Encoding started ... ")
encodeListKnown = findEncodings(imgList)
encodeListWithIds = [encodeListKnown, peopleIds]
print("Encoding complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListWithIds, file)
file.close()
print("File saved")