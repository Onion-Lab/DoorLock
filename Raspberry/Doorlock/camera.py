import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0) # Use PI-Camera : 0
        # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # set new dimensionns to cam object (not cap)
        # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        return frame

if __name__ == '__main__':
    cam = VideoCamera()
    while True:
        frame = cam.get_frame()

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    print('finish')
