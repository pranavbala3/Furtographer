from app import app, Collection, conn, User
import psycopg2
import pytest
from flask import url_for

# Initialize the app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True

    # Now create the test client
    client = app.test_client()

    yield client

# Replace the following placeholders with your actual database 
TEST_DB_HOST = 'localhost'
TEST_DB_NAME = 'furtographer'
TEST_DB_USER = 'admin'
TEST_DB_PASSWORD = 'password'
TEST_DB_PORT = 5431

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


# Create a connection to the test database
@pytest.fixture
def test_conn():
    conn = psycopg2.connect(host=TEST_DB_HOST, dbname=TEST_DB_NAME, user=TEST_DB_USER, password=TEST_DB_PASSWORD, port=TEST_DB_PORT)
    yield conn
    conn.close()

# Test checking password for a valid user
def test_check_password_valid_user(test_conn):
    # Clear the users table before the test
    cursor = test_conn.cursor()
    cursor.execute("DELETE FROM users")
    test_conn.commit()
    
    # Your test username and password
    test_username = 'test_user'
    test_password = 'test_password'

    # Add a test user to the database
    cursor = test_conn.cursor()
    cursor.execute("INSERT INTO users (user_name, pwd) VALUES (%s, %s)", (test_username, test_password))
    test_conn.commit()

    # Call the check_password method
    result = User.check_password(test_username, test_password)

    # Check if the result is True (valid user)
    assert result is True

# Test checking password for an invalid user
def test_check_password_invalid_user(test_conn):
    # Clear the users table before the test
    cursor = test_conn.cursor()
    cursor.execute("DELETE FROM users")
    test_conn.commit()

    # Your test username and password
    test_username = 'test_user'
    test_password = 'test_password'

    # Call the check_password method without adding the user to the database
    result = User.check_password(test_username, test_password)

    # Check if the result is False (invalid user)
    assert result is False

def test_get_all_from_collection(client, test_conn):
    # Clear the collections and users tables before the test
    cursor = test_conn.cursor()
    cursor.execute("DELETE FROM collections")
    cursor.execute("DELETE FROM users")
    test_conn.commit()
    
    # Create a test user
    test_user_name = 'test_user'
    test_pwd = 'test_password'
    cursor.execute("INSERT INTO users (user_name, pwd) VALUES (%s, %s) RETURNING id", (test_user_name, test_pwd))
    test_conn.commit()
    user_id = cursor.fetchone()[0]

    # Your test content and breed
    test_content = 'Test Content'
    test_breed = 'Test Breed'

    # Add a test item to the collection with the user_id
    cursor.execute("INSERT INTO collections (content, breed, user_id) VALUES (%s, %s, %s)", (test_content, test_breed, user_id))
    test_conn.commit()

    # Call the get_all method
    result = Collection.get_all_by_date(user_id)

    # Check if the test item is in the result
    assert len(result) == 1
    assert result[0][1] == test_content
    assert result[0][2] == test_breed

# Test deleting an item from the collection
def test_delete_from_collection(client, test_conn):
    # Your test content and breed
    test_content = 'Test Content'
    test_breed = 'Test Breed'

    # Add a test item to the collection
    cursor = test_conn.cursor()
    cursor.execute("INSERT INTO collections (content, breed) VALUES (%s, %s)", (test_content, test_breed))
    test_conn.commit()

    # Get the ID of the test item
    cursor.execute("SELECT id FROM collections WHERE content = %s", (test_content,))
    result = cursor.fetchone()
    test_id = result[0]

    # Call the delete method
    Collection.delete(test_id)

    # Check if the item is deleted from the database
    cursor.execute("SELECT * FROM collections WHERE id = %s", (test_id,))
    result = cursor.fetchone()

    assert result is None

# Test that the website works
def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200


# Sample test for the index page
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'What breed is this dog?' in response.data

# Sample test for logout
def test_logout(client):
    # simulate logging in
    response = client.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
    assert response.status_code == 200

    # Go to the home page
    response = client.get('/')
    assert response.status_code == 200

    # Simulate logging out
    response = client.get('/logout', follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the user is redirected to the home page
    assert b'What breed is this dog?' in response.data


# Sample test for logining in with correct credentials
def test_login(client):
    # simulate clearing the users table
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
    
    # Simulate registering a new user
    response = client.post('/register', data=dict(username='admin', password='admin', confirm_password='admin'), follow_redirects=True)
    
    # Simulate logging in
    response = client.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

   # Check if the user is redirected to the home page
    assert b'Welcome, admin!' in response.data

#Sample test for logining in with wrong credentials
def test_login_wrong_credentials(client):
    # simulate clearing the users table
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
    
    # Simulate registering a new user
    response = client.post('/register', data=dict(username='admin', password='admin', confirm_password='admin'), follow_redirects=True)
    
    # Simulate logging in
    response = client.post('/login', data=dict(username='admin', password='wrong'), follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that it gives the user an error message for wrong credentials
    assert b'Login failed. Please check your username and password.' in response.data


# Sample test for the going to register page
def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

# Sample test for registering a new user in the database
def test_register(client):
    # Clear the users table before the test
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()

    # Simulate registering a new user
    response = client.post('/register', data=dict(username='test', password='test', confirm_password='test'), follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the user is redirected to the home page
    assert b'What breed is this dog?' in response.data

    # Check if the user is present in the database
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        assert len(users) == 1
        assert users[0][1] == 'test'
    

# Sample test for registering a new user with an existing username
def test_register_existing_username(client):
    # Clear the users table before the test
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()

    # Simulate registering a new user
    response = client.post('/register', data=dict(username='test', password='test', confirm_password='test'), follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the user is redirected to the home page
    assert b'What breed is this dog?' in response.data

    # Check if the user is present in the database
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        assert len(users) == 1
        assert users[0][1] == 'test'

    # Simulate registering a new user with the same username
    response = client.post('/register', data=dict(username='test', password='test', confirm_password='test'), follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check that it gives the user an error message for existing username
    assert b'Registration failed. Please try again.' in response.data

    # Check if the user is still present in the database
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        assert len(users) == 1
        assert users[0][1] == 'test'

# Sample test for adding a new item to the collection
def test_add_to_collection(client, test_conn):

    # Clear the collections and users tables before the test
    with app.app_context():
        cursor = test_conn.cursor()
        cursor.execute("DELETE FROM collections")
        cursor.execute("DELETE FROM users")
        test_conn.commit()

    # Create a test user
    test_user_name = 'test_user'
    test_pwd = 'test_password'
    cursor.execute("INSERT INTO users (user_name, pwd) VALUES (%s, %s) RETURNING id", (test_user_name, test_pwd))
    test_conn.commit()
    user_id = cursor.fetchone()[0]

    # Your test content and breed
    test_content = 'Test Content'
    test_breed = 'Test Breed'

    # Add a test item to the collection with the user_id
    cursor.execute("INSERT INTO collections (content, breed, user_id) VALUES (%s, %s, %s)", (test_content, test_breed, user_id))
    test_conn.commit()

    # Call the get_all method
    result = Collection.get_all_by_date(user_id)

    # Check if the test item is in the result
    assert len(result) == 1
    assert result[0][1] == test_content
    assert result[0][2] == test_breed

# Sample test for updating a collection item
def test_update_collection_item(client, test_conn):
    # Clear the collections table and user table before the test
    with app.app_context():
        cursor = test_conn.cursor()
        cursor.execute("DELETE FROM collections")
        cursor.execute("DELETE FROM users")
        test_conn.commit()

    # Create a test user
    test_user_name = 'test_user'
    test_pwd = 'test_password'
    cursor.execute("INSERT INTO users (user_name, pwd) VALUES (%s, %s) RETURNING id", (test_user_name, test_pwd))
    test_conn.commit()
    user_id = cursor.fetchone()[0]

    # Your test content and breed
    test_content = 'Test Content'
    test_breed = 'Test Breed'

    # Add a test item to the collection with the user_id
    cursor.execute("INSERT INTO collections (content, breed, user_id) VALUES (%s, %s, %s)", (test_content, test_breed, user_id))
    test_conn.commit()

    # Check if the item is present in the collection
    cursor.execute("SELECT * FROM collections WHERE user_id = %s", (user_id,))
    items = cursor.fetchall()
    assert len(items) == 1

    # Get the ID of the added item
    item_id = items[0][0]

    # Simulate updating the item
    cursor.execute("UPDATE collections SET content = %s, breed = %s WHERE id = %s", ('Updated Item', 'Updated Breed', item_id))

    # Check if the item is present in the collection and is updated
    cursor.execute("SELECT * FROM collections WHERE user_id = %s", (user_id,))
    items = cursor.fetchall()
    assert len(items) == 1
    assert items[0][1] == 'Updated Item'
    assert items[0][2] == 'Updated Breed'


def test_delete_collection_item(client, test_conn):
    # Clear the collections table and user table before the test
    with app.app_context():
        cursor = test_conn.cursor()
        cursor.execute("DELETE FROM collections")
        cursor.execute("DELETE FROM users")
        test_conn.commit()

    # Create a test user
    test_user_name = 'test_user'
    test_pwd = 'test_password'
    cursor.execute("INSERT INTO users (user_name, pwd) VALUES (%s, %s) RETURNING id", (test_user_name, test_pwd))
    test_conn.commit()
    user_id = cursor.fetchone()[0]

    # Your test content and breed
    test_content = 'Test Content'
    test_breed = 'Test Breed'

    # Add a test item to the collection with the user_id
    cursor.execute("INSERT INTO collections (content, breed, user_id) VALUES (%s, %s, %s)", (test_content, test_breed, user_id))
    test_conn.commit()

    # Check if the item is present in the collection
    cursor.execute("SELECT * FROM collections WHERE user_id = %s", (user_id,))
    items = cursor.fetchall()
    assert len(items) == 1

    # Get the ID of the added item
    item_id = items[0][0]

    # Simulate deleting the item
    Collection.delete(item_id)

    # Check if the item is no longer present in the collection
    cursor.execute("SELECT * FROM collections WHERE user_id = %s", (user_id,))
    items = cursor.fetchall()
    assert len(items) == 0


# Sample test for upload photo page
def test_upload_photo_page(client):
    response = client.get('/upload_photo')
    assert response.status_code == 200
    assert b'Upload' in response.data

# Sample test for uploading a photo


# Sample test for 

# Sample test to check the response when clicking 'Capture'
def test_tasks_capture(client):
    response = client.post('/tasks', data={'click': 'Capture'})
    assert response.status_code == 200
    assert b'Take Photo' in response.data  # Adjust this line based on your expected response

# Sample test to check the response when clicking 'Retake'
def test_tasks_retake(client):
    response = client.post('/tasks', data={'click': 'Retake'})
    assert response.status_code == 200
    # assert b'Take Photo' not in response.data # figure the best way to check assertion later

# Sample test to check the response when an invalid action is provided
def test_tasks_invalid_action(client):
    response = client.post('/tasks', data={'click': 'InvalidAction'})
    assert response.status_code == 200
    assert b'fail' in response.data  # Adjust this line based on your expected response

# Sample test for retaking a photo
def test_tasks_retake(client):
    response = client.post('/tasks', data={'click': 'Retake'})
    assert response.status_code == 200
    assert b'Take Photo' in response.data  # Adjust this line based on your expected response

def test_upload_photo(client):
    # Simulate uploading a photo (replace 'file' with your actual file path)
    response = client.post('/upload', data={'file': (open('static/uploads/chihuahua.jpg', 'rb'), 'photo.jpg')}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Upload Photo' in response.data  # Adjust this line based on your expected response

# Sample test for handling GET request to '/' route
def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'What breed is this dog?' in response.data

# Sample test for handling GET request to '/login' route
def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

# Sample test for handling GET request to '/logout' route
def test_logout_get(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'What breed is this dog?' in response.data

# Sample test for handling GET request to '/register' route
def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

# Sample test for handling POST request to '/upload' route without a file
def test_upload_no_file(client):
    response = client.post('/upload', data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Upload Photo' in response.data

# Sample test for logout with logged-in user
def test_logout_logged_in(client):
    # Simulate logging in
    response = client.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
    assert response.status_code == 200

    # Simulate logging out
    response = client.get('/logout', follow_redirects=True)

    # Check if the user is redirected to the home page
    assert response.status_code == 200
    assert b'What breed is this dog?' in response.data

# Sample test for upload photo page with logged-in user
def test_upload_photo_page_logged_in(client):
    # Simulate logging in
    response = client.post('/login', data=dict(username='admin', password='admin'), follow_redirects=True)
    assert response.status_code == 200

    # Visit the upload photo page
    response = client.get('/upload_photo')
    assert response.status_code == 200

    # Check if the user can upload a photo
    assert b'Upload' in response.data

def test_capture_frame_endpoint(client):
    response = client.post('/tasks', data={'click': 'Capture'}, follow_redirects=True)

    # Assertions for the expected behavior
    assert response.status_code == 200

def test_take_photo_endpoint(client):
    response = client.get('/take_photo')

    # Assertions for the expected behavior
    assert response.status_code == 200

def test_collection_endpoint(client):
    response = client.get('/collection')

    # Assertions for the expected behavior
    assert response.status_code == 302

def test_register_endpoint(client):
    response = client.post('/register', data={'username': 'newuser', 'password': 'newpassword', 'confirm_password': 'newpassword'})

    # Assertions for the expected behavior
    assert response.status_code == 302

def test_login_endpoint(client):
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})

    # Assertions for the expected behavior
    assert response.status_code == 200