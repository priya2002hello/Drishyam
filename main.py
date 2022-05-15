from flask import Flask,render_template,Response,url_for
from camera import c1
from flask_socketio import SocketIO,emit
import base64,cv2
import imutils
import dlib
from engineio.payload import Payload
#Payload.max_decode_packets = 2048

app=Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins='*' )

#render index.html file
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

#check if socket  connection is successfull
@socketio.on("my event")
def handle_message(data):
    print('received message: ' + str(data))

#Receieving frames from client , processing and sending back to client again.
@socketio.on('image')
def image(data_image):
    print("img url connected")
    frame =c1.readb64(data_image)
    frame =c1.get_frames(frame)
    stringData=c1.encodeb64(frame)

    emit('response_back', stringData)

#run flask app
if __name__ == '__main__':
    socketio.run(app, debug=True)