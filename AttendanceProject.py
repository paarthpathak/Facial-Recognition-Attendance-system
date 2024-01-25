import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

video_capture = cv2.VideoCapture(0)

path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print("Total Students Detected:", len(myList))
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            today = datetime.now().strftime("%d/%m/%Y")
        if name not in nameList and entry[0] == today:
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y, %I:%M:%S")
            f.writelines(f'\n{name},{date_time}')
            #import firebase
            #print("Attendance has been uploaded to database")
        elif name in nameList and entry[0] != today:
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y, %I:%M:%S")
            f.writelines(f'\n{name},{date_time}')

        #import firebase
        #print("Attendance has been uploaded to database")


encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #Lowest Distance will be our best match
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)

        cv2.imshow("Webcam", img)
        ch = cv2.waitKey(100)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print("Your face has been recognised!!!")
            break

        elif ch == 27 or ch == ord('q') or ch == ord('Q'):
            cv2.waitKey(300)
            print('Quitting')
            print("Face not recognised!!")
            break
# All done, release device
    #cap.release()
    #cv2.destroyAllWindows()




