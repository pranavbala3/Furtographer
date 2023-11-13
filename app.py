import cv2
import datetime as dt
import psycopg2
from flask import Flask, render_template, Response, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import os
from model.model import (
    Model,
)

model = Model()

global capture
global save
global retake
global latest_frame
capture = 0
save = 0
retake = 0
latest_frame = None

try:
    os.mkdir('./photos')
except OSError as error:
    pass

try:
    os.mkdir('./uploads')
except OSError as error:
    pass

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password@localhost:5431/furtographer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Add a secret key for session management
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)


class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    breed = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=dt.datetime.utcnow)

    def __repr__(self):
        return '<Collection %r>' % self.id


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True, name='user_name')
    password = db.Column(db.String(200), nullable=False, name='pwd')

    def __repr__(self):
        return '<User %r>' % self.id

    def check_password(self, password):
        return self.password == password


def generate_frames():
    global capture
    global save
    global retake
    global latest_frame

    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
            frame_buffer = buffer.tobytes()
            if not ret:
                continue
            latest_frame = frame_buffer
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_buffer + b'\r\n')
        if (capture):
            capture = 0
            while (not save and not retake):
                pass
            if (save):
                frame_np = np.asarray(frame)
                now = dt.datetime.now()
                p = os.path.sep.join(
                    ['photos', "photo_{}.jpg".format(str(now).replace(":", ''))])
                cv2.imwrite(p, frame_np)
                save = 0
            elif (retake):
                retake = 0
    camera.release()

@app.route('/captured_frame')
def captured_frame():
    global latest_frame
    return Response(latest_frame, mimetype='image/jpeg')

@app.route('/')
def index():
    logged_in = 'username' in session
    return render_template('index.html', logged_in=logged_in, current_user=session.get('username'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        # Assuming you have a check_password method in your User model
        if user and user.check_password(password):
            session['username'] = user.username
            return redirect('/')
        else:
            return render_template('login.html', login_failed=True)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        new_confirm_password = request.form['confirm_password']

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            return render_template('register.html', registration_failed=True)

        # Check if the password and confirm_password match
        if new_password != new_confirm_password:
            return render_template('register.html', registration_failed=True)

        # Create a new user
        new_user = User(username=new_username, password=new_password)

        try:
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_username

            # Redirect to the main page after registration
            return redirect('/')
        except Exception as e:
            print(str(e))
            return 'There was an issue with registration. Please try again.'

    return render_template('register.html')



@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/take_photo', methods=['POST', 'GET'])
def take_photo():
    return render_template('take_photo.html', title='Take Photo')


@app.route('/tasks', methods=['POST', 'GET'])
def tasks():
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
            generate_frames()
            # Trigger the display message
            return render_template('take_photo.html', show_modal=True)
        elif request.form.get('click') == 'Save':
            global save
            save = 1
            return render_template('take_photo.html', show_modal=False)
        elif request.form.get('click') == 'Retake':
            global retake
            retake = 1
            return render_template('take_photo.html', show_modal=False)
        else:
            return "fail"
    return render_template('take_photo.html', show_modal=False)


@app.route('/upload_photo')
def upload_photo():
    return render_template('upload_photo.html', title='Upload Photo')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if 'file' not in request.files:
        return render_template('upload_photo.html', title='Upload Photo', upload_error=True, breed=None)
    file = request.files['file']
    if file.filename == '':
        return render_template('upload_photo.html', title='Upload Photo', upload_error=True, breed=None)

    if file:
        # for now, the file is just going to this directory, but we will need to connect this to our db/image storage system
        file.save("./static/uploads/" + file.filename)

        ### Classifying the File
        breed = model.predict_path(f"static/uploads/{file.filename}")
        breedname = str(breed).replace('_', ' ')
        return render_template('upload_photo.html', title='Upload Photo', upload_error=False, upload=True, breed=breedname, \
            uploaded_image_url=url_for('static', filename=f'uploads/{file.filename}'))


@app.route('/collection', methods=['POST', 'GET'])
def collection():
    logged_in = 'username' in session
    if request.method == 'POST':
        task_content = request.form['content']
        task_breed = request.form['breed']
        new_furto = Collection(content=task_content, breed=task_breed)
        try:
            db.session.add(new_furto)
            db.session.commit()
            return redirect('/collection')
        except Exception as e:
            print(f"Error: {e}")
            return 'There was an issue adding your furto! Sorry!'

    else:
        tasks = Collection.query.order_by(Collection.date_created).all()
        return render_template('collection.html', title='View Collection', tasks=tasks, logged_in=logged_in, current_user=session.get('username'))


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
        furto.breed = request.form['breed']

        try:
            db.session.commit()
            return redirect('/collection')
        except:
            return 'There was an issue updating your furto, so sorry!'
    else:
        return render_template('update.html', task=furto)


if __name__ == '__main__':
    app.run(debug=True)
