from flask import Flask,render_template,url_for,request,redirect
from face.recognise_faces_image import recognise_face
from flask_socketio import SocketIO,emit
from face.gen_encodings import encoding
from face.detect_face import DetectFace
from face.read_b64 import readb64
from face.encode_b64 import encodeb64
import cv2
import os
import numpy as np
from set_mongo import criminal_records,candidate_records
from face.store_encodings import store
from werkzeug.utils import secure_filename

#creating an instance of flask application along with socketio
app=Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins='*' )


#render index.html file on route "/"
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

#render details.html .
@app.route('/details/<int:seatno>',methods=['GET'])
def details(seatno):
    #get candidate info from database
    data=candidate_records.find_one({"seatno":str(seatno)})
    if(data==None):
        return render_template('details.html',info="Candidate not present in Records")
    info={
        "name":data["name"],
        "img_url":data["url"],
         "seatno":data["seatno"],
        "email": data["email"],
        "gender": data["gender"],
        "age": data["age"],
        "bio": data["bio"],
        "place":data["place"]

    }

    print("\n details.html :- ",info)
    return render_template('details.html',info=info)

#Find candidate by using his/her seat.No
@app.route('/application',methods=['GET','POST'])
def application():

    return render_template('application.html')

#update criminal records route
@app.route('/add_criminal_record',methods=['GET'])
def add():
    return render_template('criminal_records.html')

#candidate registration route
@app.route('/candidate_registration',methods=['GET','POST'])
def register():
    #post request
    if request.method=='POST':
        #get form content
        name=request.form["name"]
        seatno=request.form["seatno"]
        email=request.form["email"]
        gender=request.form["gender"]
        age=request.form["age"]
        bio=request.form["bio"]
        place=request.form["place"]
        if request.files:
           file=request.files["file"]
           filename=secure_filename(file.filename)
           #save image
           file.save(os.path.join("static","image",filename))
           frame=cv2.imread(os.path.join("static","image",filename))
           encodings=encoding.gen_encodings(frame)
           url = encodeb64(frame)

           #add candidate_info  to database
           for single_encoding in encodings:
               single_encoding = single_encoding.tolist()
               data={
               "name":name,
               "seatno":seatno,
               "url":url,
               "encodings":single_encoding,
                "email":email,
                "gender":gender,
                "age":age,
                 "bio":bio,
                "place":place

               }
               candidate_records.insert_one(data)
               print("\n main.py :- candidate_registration route :image saved")
        print("\nmain.py :- candiate_registration route",name,seatno)
        return redirect('/candidate_registration')
    else:
        #get request
        return render_template('candidate_registration.html')

#Connect Successful
@socketio.on("my event")
def handle_message(data):
    print('received message: ' + str(data))

#Receieving frames from client , processing and sending back to client again.
@socketio.on('detect face')
def image(data_image):
    try:
       print("\nMain.py :- Detect Face Event")
       #initialize detect face object
       detect_face=DetectFace()

       frame =readb64(data_image)
       frame =detect_face.detect(frame)
       stringData=encodeb64(frame)
       emit('response_back', stringData)
    except:
        print("\nMain.py :- detect face event Error")

@socketio.on('rec face')
def recognise(data_image):
    try:
        rface = recognise_face()
        print("\nmain.py :- rec face event")
        frame_url=data_image["frame"]
        seat_no=data_image['seat_no']

        frame =readb64(frame_url)
        data= rface.rec_frames(frame,seat_no)
        if data['status']=="unavailable":
            print("\n main.py :- candidate is unavailable")
            emit('rec_face', {
                "status":"unavailable"
            })
        elif data['status']=="seatno not found":
            print("\n main.py :- candidate seat no not present in database")
            emit('rec_face', {
                "status": "seat no not found"
            })
        elif data["status"]=="error":
            print("\n main.py :- error occured in recognise_face_images.py")
            emit('rec_face', {
                "status": "error"
            })
        else:
            print("\n main.py :- data returned",data)
            frame=data['image']
            name=data['name']
            status=data['status']

            stringData =encodeb64(frame)

            emit('rec_face', {
                    "img_url":stringData,
                     "names":name,
                     "status":status
                   })
    except:
        print("\n main.py :- there was an issue in rec face event in main.py")

@socketio.on('update criminal record')
def update(data):
    #rface=recognise_face()
    name=data['name']
    image_url=data['image_url']
    count=data['count']
    age=data['age']
    gender= data['gender']
    place= data['place']
    case_info=data['case_info']
    frame = readb64(image_url)
    encodings=encoding.gen_encodings(frame)
    print("Criminal Records updated " + name +age +gender +place +case_info )
    for single_encoding in encodings:
        single_encoding= single_encoding.tolist()
        record={
            "name":name,
            "age": age,
            "gender": gender,
            "case_info": case_info,
            "place": place,
            "image_url":image_url,
            "encodings": single_encoding,
            "count":count

        }
        criminal_records.insert_one(record)
    print("\n count is :",count)
    if(count==15):
        store()
    #cv2.imwrite("C:/Users/Priyanka/PycharmProjects/Drishyam(1.0)/static/image_dataset/priyanka_nikam/{}.jpg".format(str(count)+name),frame)




#run flask app
if __name__ == '__main__':
    socketio.run(app, debug=True)