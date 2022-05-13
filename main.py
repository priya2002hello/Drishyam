from flask import Flask,render_template,Response,url_for
from camera import gen_frames
import cv2

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#working
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)