import face_recognition
import pickle
import cv2
import os
import base64, io
from PIL import Image
import numpy as np


def encodeb64(frame):

        try:
            imgencode = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])[1]

            # base64 encode
            stringData = base64.b64encode(imgencode).decode('utf-8')
            b64_src = 'data:image/jpeg;base64,'
            stringData = b64_src + stringData
            return stringData

        except:
            print("there was an error while encoding  image")
