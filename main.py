import cv2
import numpy as np
from threading import Thread
from flask import Flask, render_template, Response

app = Flask(__name__)

class VideoThread:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True


def threadVideoGet(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Main thread shows video frames.
    """

    video_getter = VideoThread(source).start()

    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break

        frame = video_getter.frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/1')
def index1():
    return Response(threadVideoGet(0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/2')
def index2():
    return Response(threadVideoGet(1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/3')
def index3():
    return Response(threadVideoGet(1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/4')
def index4():
    return Response(threadVideoGet(1), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)


