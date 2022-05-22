# import the necessary packages
import face_recognition
import pickle
import cv2
import os
import base64, io
from PIL import Image
import numpy as np
from set_mongo import criminal_records,candidate_records

class recognise_face:
    def __init__(self):
        # load the known faces and embeddings
        # try:
         print("[INFO] loading encodings...")
         self.data = pickle.loads(open('C:/Users/Priyanka/PycharmProjects/Drishyam(1.0)/face/encoding.txt', "rb").read())
         print("Encodings loaded Successfully")
        # except:
        #     print("There was an error while loading encodings in dataset")

    def rec_frames(self, frame1):
        # detect the (x, y)-coordinates of the bounding boxes corresponding
        # to each face in the input image, then compute the facial embeddings
        # for each face
        try:
            frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame1=frame
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


