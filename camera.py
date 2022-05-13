import cv2

#including classifier used to identify face. returns co-ordinates of rectangle where face is found.
face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class video:
    def __init__(self):
       self.camera = cv2.VideoCapture(0)  # camera turns on

    def get_frames(self):
           success, frame = self.camera.read()  # read the camera frame
           if not success:
               return "error"

           #apply face classifier to a frame
           faces=face_cascade.detectMultiScale(frame,1.1,4)

           for (x, y, z, w) in faces:
               cv2.rectangle(frame, (x, y), (x + z, y + w), (255, 0, 0), 2)

            # resizing image.
           res = cv2.resize(frame, None, fx=0.5, fy=0.5)

           return frame
    def __del__(self):
        self.camera.release()

def gen_frames():
    c1=video()
    while True:
            frame=c1.get_frames()
            if frame=="error":
                print("camera not open")
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result