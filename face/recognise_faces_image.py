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
     try:
         print("\n recognise_faces_image.py :- [INFO] loading encodings...")
         self.data = pickle.loads(open('encoding.txt', "rb").read())
         print("\n recognise_faces_image.py :- Encodings loaded Successfully")
     except:
        print("\n recognise_faces_images.py Error:-There was an error while loading encodings in dataset ")

    def rec_frames(self, frame1,seatno):
        # detect the (x, y)-coordinates of the bounding boxes corresponding
        # to each face in the input image, then compute the facial embeddings
        # for each face
         try:
            #find candidate with seat no given
            candidate_info=candidate_records.find_one({"seatno":seatno})
            if candidate_info ==None:
               print("\n recognise_faces_image.py :- seat no not found,there is some error")
               data={
                   "status" : "seatno not found"
               }
               return data

            #get candidate encoding
            candidate_encoding=np.array(candidate_info["encodings"])

            frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame1=frame
            print("\n recognise_faces_image.py :- [INFO] recognizing faces...")
            boxes = face_recognition.face_locations(frame, model='hog')
            encodings = face_recognition.face_encodings(frame, boxes)

            matches_candidate=face_recognition.compare_faces(encodings,candidate_encoding)
            if True in matches_candidate:
                print("candidate is present, checking for criminal records")
                matchedIndex_candidate=[i for (i,b) in enumerate(matches_candidate) if b]

                index=matchedIndex_candidate[0]
                single_encoding=encodings[index]
                single_box=boxes[index]
                matches = face_recognition.compare_faces(self.data["encodings"],
                                                         single_encoding)
                name="Unknown"

                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = self.data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    name = max(counts, key=counts.get)

                # for ((top, right, bottom, left), name) in (single_box,name):
                    # draw the predicted face name on the image
                [top,right,bottom,left]=single_box

                cv2.rectangle(frame, (left, top), (right, bottom), (202, 232, 7), 4)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_COMPLEX,
                                4, (202, 232, 7), 5)

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                if(name=="Unknown"):
                   status="eligible"
                else:
                   status="not eligible"

                data = {"image": frame,
                        "name": name,
                        "status":status}
                return data
            elif not True in matches_candidate:
                print("\n recognise_faces_image.py :- Candidate is unavailable")
                data={
                    "status": "unavailable"
                }
                return data


         except:
             print("\n recognise_faces_image.py :- RECOGNISE_FACES_IMAGE.py Error.")
             data={
                 "status" : "error"
             }
             return data
