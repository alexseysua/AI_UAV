import cv2


class CaptureImage:
    video_cap = None

    def __init__(self):
        self.video_cap = cv2.VideoCapture(0)

    def get_frame(self):
        res, frame = self.video_cap.read()
        if res:
            return frame

    def __del__(self):
        self.video_cap.release()
