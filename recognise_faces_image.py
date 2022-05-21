# import the necessary packages
import face_recognition
import pickle
import cv2
import os
import base64, io
from PIL import Image
import numpy as np


class recognise_face:
    def __init__(self):
        # load the known faces and embeddings
        try:
            print("[INFO] loading encodings...")
            self.data = pickle.loads(open('encoding.txt', "rb").read())
            print("Encodings loaded Successfully")
        except:
            print("There was an error while loading encodings in dataset")

    def rec_frames(self, frame1):
        # detect the (x, y)-coordinates of the bounding boxes corresponding
        # to each face in the input image, then compute the facial embeddings
        # for each face
        try:
            frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            print("[INFO] recognizing faces...")
            boxes = face_recognition.face_locations(frame, model='hog')
            encodings = face_recognition.face_encodings(frame, boxes)
            names = []

            # attempt to match each face in the input image to our known
            # encodings
            for encoding in encodings:
                matches = face_recognition.compare_faces(self.data["encodings"],
                                                         encoding)
                name = "Unknown"

                # check to see if we have found a match
                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = self.data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    name = max(counts, key=counts.get)
                names.append(name)

            for ((top, right, bottom, left), name) in zip(boxes, names):
                # draw the predicted face name on the image
                cv2.rectangle(frame, (left, top), (right, bottom), (202, 232, 7),4)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_COMPLEX,
                            4, (202, 232, 7), 5)

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            print(names)
            data={"image":frame,"names":names}
            return data

        except:
            print("There was an error in recognising face")
            return frame1

    # decoding base64 url
    def readb64(self, base64_string):
        try:
            idx = base64_string.find('base64,')
            base64_string = base64_string[idx + 7:]

            sbuf = io.BytesIO()

            sbuf.write(base64.b64decode(base64_string, ' /'))
            pimg = Image.open(sbuf)

            return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
        except:
            print("There was an issue in reading b64 readings")

    # encode b64
    def encodeb64(self, frame):

        try:
            imgencode = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])[1]

            # base64 encode
            stringData = base64.b64encode(imgencode).decode('utf-8')
            b64_src = 'data:image/jpeg;base64,'
            stringData = b64_src + stringData
            return stringData

        except:
            print("there was an error while encoding  image")

    def detect_face(self,frame1):
        #try:
            frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            print("[INFO] detecting faces...")
            boxes = face_recognition.face_locations(frame, model='hog')
            print(boxes)

            for (top, right, bottom, left) in boxes:
                 # draw the predicted face name on the image
                   cv2.rectangle(frame, (left, top), (right, bottom), (13,36,97), 2)
                   frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            return frame
        # except:
        #     print("face was not detected here")
        #     return frame1

rface=recognise_face()
