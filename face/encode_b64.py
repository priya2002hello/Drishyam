
import cv2
import base64
from PIL import Image
import numpy as np

#encode cv2 image to base64 url
def encodeb64(frame):

        try:
            imgencode = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])[1]

            # base64 encode
            stringData = base64.b64encode(imgencode).decode('utf-8')
            b64_src = 'data:image/jpeg;base64,'
            stringData = b64_src + stringData
            return stringData

        except:
            print("Error:- encodeb64")
