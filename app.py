import cv2
import datetime as dt
import psycopg2
from flask import (
    Flask, render_template, Response,
    request, redirect, session
    )
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
global latest_breedname
global photo_path

capture = 0
save = 0
retake = 0
latest_frame = None
latest_breedname = None
photo_path = None

static_dir = 'static'
photos_dir = os.path.join(static_dir, 'photos')
uploads_dir = os.path.join(static_dir, 'uploads')

try:
    os.mkdir(photos_dir)
except OSError as error:
    pass

try:
    os.mkdir(uploads_dir)
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

app = Flask(__name__, static_url_path='/' + static_dir)
app.config['SECRET_KEY'] = 'your_secret_key'


class Collection:
    @staticmethod
    def add(content, breed, user_id):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO collections (content, breed, user_id) VALUES (%s, %s, %s)", (content, breed, user_id))
        conn.commit()

    @staticmethod
    def get_all_by_date(user_id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections WHERE user_id = %s ORDER BY date_created DESC", (user_id,))
        return cursor.fetchall()
    
    @staticmethod
    def get_all_by_breed(user_id):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections WHERE user_id = %s ORDER BY breed", (user_id,))
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
    global latest_breedname

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
                p = os.path.sep.join([photos_dir, "photo_{}.jpg".format(str(now).replace(":", ''))])
                cv2.imwrite(p, frame_np)
                breed = model.predict_path(p)
                breedname = str(breed).replace('_', ' ')
                latest_breedname = breedname
                photo_path = p
                print(photo_path)
                Collection.add(p, latest_breedname, session.get('user_id'))
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
                session['user_id'] = user[0]  # Set user_id in the session
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
    session.pop('user_id', None)
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

            cursor.execute("SELECT * FROM users WHERE user_name = %s AND pwd = %s", (new_username, new_password))
            user = cursor.fetchone()

            session['username'] = new_username
            session['user_id'] = user[0]  # Set user_id in the session

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
    logged_in = 'username' in session
    return render_template('take_photo.html', logged_in=logged_in, current_user=session.get('username'), title='Take Photo', breedname = latest_breedname)


@app.route('/tasks', methods=['POST', 'GET'])
def tasks():
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
            generate_frames()
            # Trigger the display message
            return render_template('take_photo.html', title='Take Photo' , show_modal=True, upload=False, breed=latest_breedname)
        elif request.form.get('click') == 'Save':
            global save
            save = 1
            return render_template('take_photo.html', title='Take Photo', show_modal=False, upload=True, breed=latest_breedname, uploaded_image_url=photo_path)
        elif request.form.get('click') == 'Retake':
            global retake
            retake = 1
            return render_template('take_photo.html', title='Take Photo', show_modal=False, upload=False, breed=latest_breedname)
        else:
            return "fail"
    return render_template('take_photo.html', show_modal=False, upload=False, breed=latest_breedname)


@app.route('/upload_photo')
def upload_photo():
    logged_in = 'username' in session
    return render_template('upload_photo.html', logged_in=logged_in, current_user=session.get('username'), title='Upload Photo')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if 'file' not in request.files:
        return render_template('upload_photo.html', title='Upload Photo', upload_error=True, breed=None)
    file = request.files['file']
    if file.filename == '':
        return render_template('upload_photo.html', title='Upload Photo', upload_error=True, breed=None)

    if file:
        # for now, the file is just going to this directory, but we will need to connect this to our db/image storage system
        file_path = os.path.join(uploads_dir,file.filename)
        file.save(file_path)

        ### Classifying the File
        breed = model.predict_path(file_path)
        if breed is None:
            breedname = "picture without dawgs :("
        else:
            breedname = str(breed).replace('_', ' ')
        return render_template('upload_photo.html', title='Upload Photo', upload_error=False, upload=True, breed=breedname, \
            uploaded_image_url=file_path)


@app.route('/collection', methods=['POST', 'GET'])
def collection():
    logged_in = 'username' in session
    if logged_in:
        # Get the user_id from the database using a sql query
        user_id = session.get('user_id')
        if request.method == 'POST':
            task_content = request.form['content']
            task_breed = request.form['breed']
            try:
                Collection.add(task_content, task_breed, user_id)
                return redirect('/collection')
            except Exception as e:
                print(f"Error: {e}")
                return 'There was an issue adding your furto! Sorry!'
        else:
            try:
                # Retrieve the sort value from the form
                sort_value = request.args.get('sort', 'date')
                print(sort_value)
                if (sort_value == 'date'):
                    tasks = Collection.get_all_by_date(user_id)
                elif(sort_value == 'breed'):
                    tasks = Collection.get_all_by_breed(user_id)
                else:
                    tasks = Collection.get_all_by_date(user_id)
                
                # Add counts of total furtos tracking
                total_furtos = len(tasks)
                print(total_furtos)
                tasks_with_headers = [{'id': row[0], 'content': row[1], 'breed': row[2], 'completed': row[3], 'date_created': row[4]} for row in tasks]
                return render_template('collection.html', title='View Collection', noff=total_furtos, tasks=tasks_with_headers, logged_in=logged_in, current_user=session.get('username'), sort_value=sort_value)
            except Exception as e:
                print(f"Error: {e}")
                return 'There was an issue fetching furto data! Sorry!'
    else:
        return redirect('/login')

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