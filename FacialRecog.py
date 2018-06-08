import cv2
# import os
import numpy as np
from time import sleep


class FacialRecog(object):

    def __init__(self):
        self.name_list = ['']
        self.faces = []
        self.labels = []
        classifiers = ['haarcascade_frontalface_alt.xml', 'lbpcascade_frontalface.xml']
        self.face_cascade = cv2.CascadeClassifier(classifiers[1])
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
            cv2.imshow('Training', img)
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
    facial_recognition.add_new('Michael', cv2.imread('michael.jpg'))
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


# class FacialRecog(object):
#
#     def __init__(self, name, img):
#         self.name = name
#         self.img = img
#         classifier = "haarcascade_frontalface_alt.xml"
#         self.face_cascade = cv2.CascadeClassifier(classifier)
#         self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
#         # dirs = os.listdir('michael-face')
#         # faces_list = []
#         # labels = []
#         # for file_name in dirs:
#         #     image_path = 'michael-face/%s' % file_name
#         #     image = cv2.imread(image_path)
#         #     cv2.imshow('Training on image...', cv2.resize(image, (400, 500)))
#         #     cv2.waitKey(100)
#         #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         #     faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)
#         #     (x, y, w, h) = faces[0]
#         #     faces_list.append(gray[y:y+w, x:x+h])
#         #     labels.append(1)
#         # cv2.destroyAllWindows()
#         # self.face_recognizer.train(faces_list, np.array(labels))
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)
#         (x, y, w, h) = faces[0]
#         self.face = gray[y:y+w, x:x+h]
#         self.rect = faces[0]
#         self.face_recognizer.train([self.face], np.array([1]))
#
#     def identify_face(self, face):
#         label, confidence = self.face_recognizer.predict(face)
#         return label, confidence
#
#     def detect_faces(self, img):
#         new_img = img.copy()
#         gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
#         faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
#         if len(faces) != 0:
#             for face in faces:
#                 (x, y, w, h) = face
#                 to_test = gray[x:x+w, y:y+h]
#                 label, confidence = self.identify_face(to_test)
#                 print(face)
#                 cv2.rectangle(new_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#                 cv2.putText(new_img, str(label) + ' ' + str(confidence), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
#         return new_img
#
#     def get_face(self):
#         # Check if the face of the facial_data is within view, returns a bool
#         is_there = True
#         return is_there
#
#     def get_distance(self):
#         # Get the distance between the bot and the face, returns a float
#         distance = float(1.0)
#         return distance
#
#     def get_angle(self):
#         # Get the angle of position of face, returns a float
#         angle = float(1.0)
#         return angle
#
#
# if __name__ == '__main__':
#     img = cv2.imread('1.jpg')
#     my_face = FacialRecog('Michael', img)
#     video_capture = cv2.VideoCapture(0)
#     while True:
#         if not video_capture.isOpened():
#             print('Unable to load camera')
#             sleep(5)
#             continue
#         ret, frame = video_capture.read()
#         new_frame = my_face.detect_faces(frame)
#         cv2.imshow('Video', new_frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     video_capture.release()
#     cv2.destroyAllWindows()
