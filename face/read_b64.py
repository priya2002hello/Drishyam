import face_recognition
import pickle
import cv2
import os
import base64, io
from PIL import Image
import numpy as np


    # decoding base64 url
def readb64(base64_string):
        try:
            idx = base64_string.find('base64,')
            base64_string = base64_string[idx + 7:]

            sbuf = io.BytesIO()

            sbuf.write(base64.b64decode(base64_string, ' /'))
            pimg = Image.open(sbuf)

            return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
        except:
            print("read_b64.py:- Error")

