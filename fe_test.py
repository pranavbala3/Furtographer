# Front End Testing using PyTest FrameWork
from app import app, db, Collection
import pytest
# Initialize the app for testing

# Test that the website works
def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db.db'  # Use a test database
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client
    with app.app_context():
        db.drop_all()

# Sample test for the index page
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'What breed is this dog?' in response.data


# Sample test for the login page
def test_logins(client):
    client.post('/register', data={'username': 'testuser', 'password': 'testpassword', 'confirm_password': 'testpassword'})
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    print("HERE")
    print(response.data)
    assert response.location == '/'

def test_login_failure(client):
    response = client.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'})
    print("HERE")
    print(response.data)
    assert response.status_code == 200  # Check for a non-redirect
    assert b'Login failed' in response.data  # Check for specific content in the response

# Sample test for adding a new item to the collection
def test_add_to_collection(client):
    response = client.post('/collection', data={'content': 'Test Item', 'breed': 'Test Breed'})
    assert b'Task added!' in response.data
    print("HERE")
    print(response.data)
    assert Collection.query.count() == 1

# Sample test for capturing a photo
def test_capture_photo(client):
    response = client.post('/tasks', data={'click': 'Capture'})
    assert b'photo captured' in response.data

# Sample test for uploading a photo
def test_upload_photo(client):
    response = client.post('/upload', data={'file': (open('test_image.jpg', 'rb'), 'test_image.jpg')})
    assert b'File uploaded successfully' in response.data

# Sample test for updating a collection item
def test_update_collection_item(client):
    new_item = Collection(content='Initial Content', breed='Initial Breed')
    db.session.add(new_item)
    db.session.commit()
    
    response = client.post(f'/update/{new_item.id}', data={'content': 'Updated Content', 'breed': 'Updated Breed'})
    assert b'Task updated!' in response.data
    updated_item = Collection.query.get(new_item.id)
    assert updated_item.content == 'Updated Content'
    assert updated_item.breed == 'Updated Breed'

# Sample test for deleting a collection item
def test_delete_collection_item(client):
    new_item = Collection(content='Item to Delete', breed='Breed to Delete')
    db.session.add(new_item)
    db.session.commit()

    response = client.get(f'/delete/{new_item.id}')
    assert b'Task deleted!' in response.data
    assert Collection.query.get(new_item.id) is None

if __name__ == '__main__':
    pytest.main()