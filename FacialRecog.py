import cv2
# import os
import numpy as np
from time import sleep


class FacialRecog(object):

    def __init__(self):
        self.name_list = ['']
        self.faces = []
        self.labels = []
        classifiers = ['haarcascades/haarcascade_frontalface_alt.xml',      # 0
                       'haarcascades/haarcascade_frontalface_alt2.xml',     # 1
                       'haarcascades/haarcascade_frontalface_default.xml',  # 2
                       'lbpcascades/lbpcascade_frontalface.xml',            # 3
                       'lbpcascades/lbpcascade_frontalface_improved.xml']   # 4
        self.face_cascade = cv2.CascadeClassifier('classifiers/' + classifiers[2])
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    def add_new(self, name, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 1:
            if name not in self.name_list:
                self.name_list.append(name)
            label = self.name_list.index(name)
            (x, y, w, h) = faces[0]
            face = gray[y:y+h, x:x+w]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            h, w, c = img.shape
            cv2.imshow('Training', cv2.resize(img, (int(w / h * 500), 500)))
            cv2.waitKey(1000)
            self.faces.append(face)
            self.labels.append(label)
            self.face_recognizer.train(self.faces, np.array(self.labels))
            print(name + '\'s face added')
        else:
            print('Invalid. %d faces detected.' % len(faces))

    def predict(self, face, gray):
        (x, y, w, h) = face
        test_face = gray[y:y+h, x:x+w]
        label, confidence = self.face_recognizer.predict(test_face)
        return label, confidence

    def detect_faces(self, test_img):
        img = test_img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7)
        if len(faces) > 0:
            return faces, gray
        else:
            return None, None

    def box_face(self, test_img, label, confidence, face):
        img = test_img.copy()
        (x, y, w, h) = face
        print(face)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = '%s %.2f' % (self.name_list[label], confidence)
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
        return img


if __name__ == '__main__':
    facial_recognition = FacialRecog()
    # facial_recognition.add_new('Michael', cv2.imread('michael.jpg'))
    facial_recognition.add_new('Michael', cv2.imread('michael2.jpg'))
    # facial_recognition.add_new('Mei Mei', cv2.imread('meimei.jpg'))
    facial_recognition.add_new('Mei Mei', cv2.imread('meimei2.jpg'))
    facial_recognition.add_new('Xinran', cv2.imread('xinran.jpg'))
    facial_recognition.add_new('Wang Cheng', cv2.imread('wangcheng.jpg'))
    cv2.destroyAllWindows()
    print(facial_recognition.name_list[1:])
    print(facial_recognition.labels)
    video_capture = cv2.VideoCapture(0)
    while True:
        if not video_capture.isOpened():
            print('Unable to load camera')
            sleep(5)
            continue
        ret, frame = video_capture.read()
        faces, gray = facial_recognition.detect_faces(frame)
        new_frame = frame
        if faces is not None:
            for face in faces:
                label, confidence = facial_recognition.predict(face, gray)
                new_frame = facial_recognition.box_face(new_frame, label, confidence, face)
        cv2.imshow('Video', new_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
