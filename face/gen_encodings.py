import cv2
import face_recognition
class Encoding:
    def gen_encodings(self,frame):
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model='hog')
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            return encodings
        except:
             print("there was an issue in generating encodings")
             return None

encoding=Encoding()
