from flask import Flask, render_template, Response, request
import cv2

app = Flask(__name__)

def generate_frames():
    while True:
        camera = cv2.VideoCapture(0)
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
            frame = buffer.tobytes()
            if not ret:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_photo')
def take_photo():
    return render_template('take_photo.html', title='Take Photo')

@app.route('/upload_photo')
def upload_photo():
    return render_template('upload_photo.html', title='Upload Photo')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # for now, the file isjust going to this directory, but we will need to connect this to our db/image storage system
        file.save("uploads/" + file.filename)
        return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)