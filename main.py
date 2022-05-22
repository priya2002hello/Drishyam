from flask import Flask,render_template,url_for
from face.recognise_faces_image import recognise_face
from flask_socketio import SocketIO,emit
from face.gen_encodings import encoding
from face.detect_face import DetectFace
from face.read_b64 import readb64
from face.encode_b64 import encodeb64
import cv2
import numpy as np
from set_mongo import criminal_records,candidate_records
from face.store_encodings import store

#creating an instance of flask application along with socketio
gencoding=[]
app=Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins='*' )

#render index.html file on route "/"
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/details',methods=['GET'])
def details():
    return render_template('details.html')

@app.route('/application',methods=['GET'])
def application():
    return render_template('application.html')

@app.route('/update_records',methods=['GET'])
def update():
    return render_template('criminal_records.html')

#Connect Successful
@socketio.on("my event")
def handle_message(data):
    print('received message: ' + str(data))

#Receieving frames from client , processing and sending back to client again.
@socketio.on('detect face')
def image(data_image):
    print("detecting face ...")
    detect_face=DetectFace()

    frame =readb64(data_image)
    frame =detect_face.detect(frame)
    stringData=encodeb64(frame)

    emit('response_back', stringData)

@socketio.on('rec face')
def recognise(data_image):
    rface=recognise_face()
    print("recognising face ....")
    frame =readb64(data_image)
    data= rface.rec_frames(frame)
    frame=data['image']
    names=data['names']

    stringData =encodeb64(frame)

    emit('rec_face', {
        "img_url":stringData,
         "names":names
    })

@socketio.on('update criminal record')
def update(data):
    rface=recognise_face()
    name=data['name']
    image_url=data['image_url']
    count=data['count']
    frame = readb64(image_url)
    encodings=encoding.gen_encodings(frame)
    print("Criminal Records updated " + name )
    for single_encoding in encodings:
        single_encoding= single_encoding.tolist()
        record={
            "name":name,
            "image_url":image_url,
            "encodings": single_encoding,
            "count":count
        }
        criminal_records.insert_one(record)
    print("\n count is :",count)
    if(count==15):
        store()
    cv2.imwrite("C:/Users/Priyanka/PycharmProjects/Drishyam(1.0)/static/image_dataset/priyanka_nikam/{}.jpg".format(str(count)+name),frame)
    #criminal_records.insert_one(Crecords)



#run flask app
if __name__ == '__main__':
    socketio.run(app, debug=True)