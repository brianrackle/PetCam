from flask import Flask, request, send_file, json, Response, render_template

app = Flask(__name__)
# server determines which client to communicate with using credentials
# and then uses this api to provide functionality

# local video stream
@app.route('/')
def index():
    return render_template('index.html')

# save an image from the live video
@app.route('/image')
def image():
    error = None
    if request.method == 'GET':
        return send_file('resources/cat.jpg')

# save the last {seconds} seconds of video
@app.route('/capture_video')
def capture_video():
    error = None
    if request.method == 'GET':
        seconds = request.args['seconds']
        return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# view live video stream
@app.route('/live_video')
def live_video():   
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_video():
    catdog = False
    while True:
        if catdog:
            frame = open('resources/cat.jpg').read()
        else:
            frame = open('resources/dog.jpg').read()

        catdog = not catdog
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' 
            + frame
            + b'\r\n')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)