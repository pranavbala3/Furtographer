import cv2
import datetime as dt
import psycopg2
from flask import Flask, render_template, Response, request, redirect, session, flash, url_for
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

# Initialize psycopg2 connection
conn = psycopg2.connect(
    dbname='furtographer',
    user='admin',
    password='password',
    host='localhost',
    port='5431'
)

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'your_secret_key'


class Collection:
    @staticmethod
    def add(content, breed):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO collections (content, breed) VALUES (%s, %s)", (content, breed))
        conn.commit()

    @staticmethod
    def get_all():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections ORDER BY date_created")
        return cursor.fetchall()

    @staticmethod
    def delete(id):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM collections WHERE id = %s", (id,))
        conn.commit()


class User:
    @staticmethod
    def check_password(username, password):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = %s AND pwd = %s", (username, password))
        return cursor.fetchone() is not None


def generate_frames():
    global capture
    global save
    global retake
    global latest_frame

    camera = cv2.VideoCapture(0)
    while camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
            frame_buffer = buffer.tobytes()
            if not ret:
                continue
            latest_frame = frame_buffer
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_buffer + b'\r\n'
            )
        if capture:
            capture = 0
            while not save and not retake:
                pass
            if save:
                frame_np = np.asarray(frame)
                now = dt.datetime.now()
                p = os.path.sep.join(['static/photos', "photo_{}.jpg".format(str(now).replace(":", ''))])
                cv2.imwrite(p, frame_np)
                Collection.add(p, "breed_placeholder")  # Replace "breed_placeholder" with the actual breed
                save = 0
            elif retake:
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

        try:
            # Retrieve the user with the specified username and password from the database
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_name = %s AND pwd = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()

            if user:
                session['username'] = user[1]
                return redirect('/')
            else:
                return render_template('login.html', login_failed=True)
        except Exception as e:
            print(f"Error: {e}")
            return 'There was an issue with login. Please try again.'

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
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = %s", (new_username,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            return render_template('register.html', registration_failed=True)

        # Check if the password and confirm_password match
        if new_password != new_confirm_password:
            cursor.close()
            return render_template('register.html', registration_failed=True)

        try:
            # Insert the new user into the database 
            cursor.execute("INSERT INTO users (user_name, pwd) VALUES (%s, %s)", (new_username, new_password))
            conn.commit()

            session['username'] = new_username

            # Redirect to the main page after registration
            cursor.close()
            return redirect('/')
        except Exception as e:
            cursor.close()
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
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO collections (content, breed) VALUES (%s, %s)", (task_content, task_breed))
            conn.commit()
            return redirect('/collection')
        except Exception as e:
            print(f"Error: {e}")
            return 'There was an issue adding your furto! Sorry!'
        finally:
            cursor.close()
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM collections ORDER BY date_created")
            tasks = cursor.fetchall()
            # Assuming the tuple structure is (id, content, breed, completed, date_created)
            tasks_with_headers = [{'id': row[0], 'content': row[1], 'breed': row[2], 'completed': row[3], 'date_created': row[4]} for row in tasks]
            return render_template('collection.html', title='View Collection', tasks=tasks_with_headers, logged_in=logged_in, current_user=session.get('username'))
        except Exception as e:
            print(f"Error: {e}")
            return 'There was an issue fetching furto data! Sorry!'
        finally:
            cursor.close()

@app.route('/delete/<int:id>')
def delete(id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM collections WHERE id = %s", (id,))
        conn.commit()
        return redirect('/collection')
    except Exception as e:
        print(f"Error: {e}")
        return 'There was a problem deleting that task'
    finally:
        cursor.close()

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections WHERE id = %s", (id,))
        furto = cursor.fetchone()

        if request.method == 'POST':
            new_content = request.form['content']
            new_breed = request.form['breed']
            cursor.execute("UPDATE collections SET content = %s, breed = %s WHERE id = %s", (new_content, new_breed, id))
            conn.commit()
            return redirect('/collection')
        else:
            return render_template('update.html', task=furto)
    except Exception as e:
        print(f"Error: {e}")
        return 'There was an issue updating your furto, so sorry!'
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
