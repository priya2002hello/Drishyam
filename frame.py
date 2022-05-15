import base64,cv2

# including classifier used to identify face. returns co-ordinates of rectangle where face is found.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class video:
    def __init__(frame,self):
        self.f1=frame
    def get_frames(self):
        faces = face_cascade.detectMultiScale(self.f1, 1.1, 3)

        for (x, y, z, w) in faces:
            cv2.rectangle(self.f1, (x, y), (x + z, y + w), (255, 0, 0), 2)

        # resizing image.
        res = cv2.resize(self.f1, None, fx=0.5, fy=0.5)

        return self.f1

def gen_cframes(frame):
    c1 = video(frame)
    f1= c1.get_frames()

    imgencode = cv2.imencode('.jpg', f1)

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpeg;base64,'
    stringData = b64_src + stringData

    return stringData