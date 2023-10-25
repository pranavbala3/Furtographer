from flask import Flask, render_template, Response, request, redirect
import cv2
import datetime
import os

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

global capture
capture = 0

try:
    os.mkdir('./photos')
except OSError as error:
    pass

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


def generate_frames():
    global capture
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
        if(capture):
            capture=0
            now = datetime.datetime.now()
            p = os.path.sep.join(['photos', "photo_{}.png".format(str(now).replace(":",''))])
            cv2.imwrite(p, frame)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_photo', methods=['POST','GET'])
def take_photo():
    return render_template('take_photo.html', title='Take Photo')

@app.route('/tasks', methods=['POST','GET'])
def tasks():
    if request.method == 'POST':
            if request.form.get('click') == 'Capture':
                global capture
                capture=1
                return "photo captured"
            else:
                return "fail"

@app.route('/upload_photo')
def upload_photo():
    return render_template('upload_photo.html', title='Upload Photo')

@app.route('/upload', methods=['POST', 'GET'])
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
    
@app.route('/collection', methods=['POST', 'GET'])
def collection():
    if request.method == 'POST':
        task_content = request.form['content']
        new_furto = Collection(content=task_content)

        try:
            db.session.add(new_furto)
            db.session.commit()
            return redirect('/collection')
        except:
            return 'There was an issue adding your furto! Sorry!'
    else:
        tasks = Collection.query.order_by(Collection.date_created).all()
        return render_template('collection.html', title='View Collection', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    furto_to_delete = Collection.query.get_or_404(id)

    try:
        db.session.delete(furto_to_delete)
        db.session.commit()
        return redirect('/collection')
    except:
        return 'There was a problem deleting that task'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    furto = Collection.query.get_or_404(id)

    if request.method == 'POST':
        furto.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/collection')
        except:
            return 'There was an issue updating your furto, so sorry!'
    else:
        return render_template('update.html', task=furto)

if __name__ == '__main__':
    app.run(debug=True)