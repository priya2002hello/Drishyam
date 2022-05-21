from flask import Flask,render_template,Response,url_for,redirect
from recognise_faces_image import rface
from flask_socketio import SocketIO,emit


#creating an instance of flask application along with socketio
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

#Connect Successful
@socketio.on("my event")
def handle_message(data):
    print('received message: ' + str(data))

#Receieving frames from client , processing and sending back to client again.
@socketio.on('detect face')
def image(data_image):
    print("detecting face ...")
    frame =rface.readb64(data_image)
    frame =rface.detect_face(frame)
    stringData=rface.encodeb64(frame)

    emit('response_back', stringData)

@socketio.on('rec face')
def recognise(data_image):
    print("recognising face ....")
    frame = rface.readb64(data_image)
    data= rface.rec_frames(frame)
    frame=data['image']
    names=data['names'][0]
    print("data sent to index: "+names)
    stringData = rface.encodeb64(frame)

    emit('rec_face', stringData)


#run flask app
if __name__ == '__main__':
    socketio.run(app, debug=True)