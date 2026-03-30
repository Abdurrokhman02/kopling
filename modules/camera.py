import cv2

class Camera:
    def __init__(self, cam_index=0):
        self.cam_index = cam_index
        
    def capture(self):
        cap = cv2.VideoCapture(self.cam_index)
        if not cap.isOpened():
            raise Exception("Camera tidak bisa dibuka")
        
        time.sleep(0.5)
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise Exception("Gagal ambil gambar")
        
        return frame