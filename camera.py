import cv2
import base64,io
from PIL import Image
import numpy as np
# including classifier used to identify face. returns co-ordinates of rectangle where face is found.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class video:

    def get_frames(self,frame):

        # apply face classifier to a frame
        faces = face_cascade.detectMultiScale(frame, 1.1, 3)

        for (x, y, z, w) in faces:
            cv2.rectangle(frame, (x, y), (x + z, y + w), (255, 0, 0), 2)

        # resizing image.
        res = cv2.resize(frame, None, fx=0.5, fy=0.5)

        return frame

   #decoding base64 url
    def readb64(self,base64_string):
        idx = base64_string.find('base64,')
        base64_string = base64_string[idx + 7:]

        sbuf = io.BytesIO()

        sbuf.write(base64.b64decode(base64_string, ' /'))
        pimg = Image.open(sbuf)

        return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

   #encoding base64 url.
    def encodeb64(self,frame):
        imgencode = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])[1]

        # base64 encode
        stringData = base64.b64encode(imgencode).decode('utf-8')
        b64_src = 'data:image/jpeg;base64,'
        stringData = b64_src + stringData

        return stringData
    
c1=video()

