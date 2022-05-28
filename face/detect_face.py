#detect face and return frame with detected face
import face_recognition
import cv2
import numpy as np

class DetectFace:

  def detect(self,frame1):
    try:
        frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        print("\ndetect_faces.py :- [INFO] detecting faces...")
        boxes = face_recognition.face_locations(frame, model='hog')
        print("\n detect_faces.py face location:- ",boxes)

        for (top, right, bottom, left) in boxes:
            # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom), (13, 36, 97), 4)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        return frame
    except:
        print("\ndetect_face.py :- Error ,face was not detected here")
        #return original frame as it is
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        return frame1
