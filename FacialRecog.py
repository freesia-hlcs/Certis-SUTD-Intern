import tensorflow as tf
import numpy as np
import facenet
from align import detect_face
import cv2
from time import sleep

# some constants kept as default from facenet
minsize = 20
threshold = [0.6, 0.7, 0.7]
factor = 0.709
margin = 44
input_image_size = 160

sess = tf.Session()

# read pnet, rnet, onet models from align directory and files are det1.npy, det2.npy, det3.npy
pnet, rnet, onet = detect_face.create_mtcnn(sess, 'align')

# read 20170512-110547 model file downloaded from https://drive.google.com/file/d/0B5MzpY9kBtDVZ2RpVDYwWmxoSUk
facenet.load_model("20170512-110547/20170512-110547.pb")

# Get input and output tensors
images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
embedding_size = embeddings.get_shape()[1]


def getEmbedding(resized):
    reshaped = resized.reshape(-1, input_image_size, input_image_size, 3)
    feed_dict = {images_placeholder: reshaped, phase_train_placeholder: False}
    embedding = sess.run(embeddings, feed_dict=feed_dict)
    return embedding


def getFace(img):
    faces = []
    img_size = np.asarray(img.shape)[0:2]
    bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
    if not len(bounding_boxes) == 0:
        for face in bounding_boxes:
            if face[4] > 0.50:
                det = np.squeeze(face[0:4])
                bb = np.zeros(4, dtype=np.int32)
                bb[0] = np.maximum(det[0] - margin / 2, 0)
                bb[1] = np.maximum(det[1] - margin / 2, 0)
                bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
                bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
                cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
                resized = cv2.resize(cropped, (input_image_size, input_image_size), interpolation=cv2.INTER_CUBIC)
                prewhitened = facenet.prewhiten(resized)
                faces.append({
                    'face': resized,
                    'rect': [bb[0], bb[1], bb[2], bb[3]],
                    'embedding': getEmbedding(prewhitened)
                })
    return faces


def compare2face(face1, face2):
    if face1 and face2:
        # calculate Euclidean distance
        dist = np.sqrt(np.sum(np.square(np.subtract(face1['embedding'], face2['embedding']))))
        return dist
    return -1


def identify(face, face_dic):
    best_dist = 100
    best_name = 'Visitor'
    for name in face_dic:
        dist = compare2face(face, face_dic[name])
        if dist <= max_dist and dist <= best_dist:
            best_name = name
            best_dist = dist
    return best_name, best_dist if best_dist != 100 else -1


def get_position(face):
    x = face['rect'][0]
    size = 0.5*(face['rect'][2]-face['rect'][0]+face['rect'][3]-face['rect'][1])
    r = 0.25*size
    theta = (x-200)*0.25
    return r, theta


def find_face(test_face, img):
    max_dist = 0.75
    faces = getFace(img)
    for face in faces:
        dist = compare2face(test_face, face)
        if dist < max_dist and dist != -1:
            return True
    return False


if __name__ == '__main__':
    video_capture = cv2.VideoCapture(0)
    face_dic = {
        'Michael': getFace(cv2.imread('michael2.jpg'))[0],
        'Mei Mei': getFace(cv2.imread('meimei2.jpg'))[0],
        'Xinran': getFace(cv2.imread('xinran.jpg'))[0],
        'Wang Cheng': getFace(cv2.imread('wangcheng.jpg'))[0]
    }
    max_dist = 0.75
    while True:
        if not video_capture.isOpened():
            print('Unable to load camera')
            sleep(5)
            continue
        ret, frame = video_capture.read()
        faces = getFace(frame)
        new_frame = frame
        if faces is not None:
            for face in faces:
                name, dist = identify(face, face_dic)
                cv2.rectangle(new_frame, (face['rect'][0], face['rect'][1]), (face['rect'][2], face['rect'][3]),
                              (0, 255, 0), 2)
                text = name + ' %.4f' % dist
                cv2.putText(new_frame, text, (face['rect'][0], face['rect'][1]), cv2.FONT_HERSHEY_PLAIN, 1.5,
                            (0, 255, 0), 2)
                print(get_position(face))
        cv2.imshow('Video', new_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
