# face_recog.py
import time
import face_recognition
import cv2
import camera
import os
import numpy as np
from Requester import requestPost

class FaceRecog():
    def __init__(self):
        self.camera = camera.VideoCamera()

        self.known_face_encodings = []
        self.known_face_names = []

        dir_path = '/boot/picture'
        files = os.listdir(dir_path)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.png':
                self.known_face_names.append(name)
                pathname = os.path.join(dir_path, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.prevTime = time.time()

    def __del__(self):
        del self.camera

    def get_frame(self):
        # Grab a single frame of video
        frame = self.camera.get_frame()

        small_frame = cv2.resize(frame, (320, 240))
        # RGBA to RGB
        rgb_small_frame = small_frame[:, :, ::-1]

        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        self.face_names = []
        for face_encoding in self.face_encodings:
            # See if the face is a match for the known face(s)
            distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            min_value = min(distances)

            
            if min_value < 0.4:
                index = np.argmin(distances)
                name = self.known_face_names[index]
                self.face_names.append(name)

                if time.time() - self.prevTime > 10:
                    print(requestPost('http://127.0.0.1:3004', '/open', {'user':self.face_names[0]}))
                    self.prevTime = time.time()
            else:
                self.face_names.append('Unknown')
                print(requestPost('http://127.0.0.1:3004', '/warn', {}))

            print(self.face_names)
        return frame

if __name__ == '__main__':
    face_recog = FaceRecog()
    print(face_recog.known_face_names)
    while True:
        frame = face_recog.get_frame()
#        cv2.imshow('image', frame)
#        key = cv2.waitKey(1) & 0xFF
#        if key == ord("q"):
#            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')
