from app import app, Collection
import psycopg2
import pytest

# Initialize the app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Use a test database
    db_connection = psycopg2.connect(
        "dbname='furtographer' user='admin' password='password' host='localhost' port='5431'"
    )
    cursor = db_connection.cursor()
    with app.app_context():
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection (
                id SERIAL PRIMARY KEY,
                content VARCHAR(255),
                breed VARCHAR(255)
            )
        ''')
        db_connection.commit()

    client = app.test_client()

    yield client

    with app.app_context():
        # Drop tables
        cursor.execute('DROP TABLE IF EXISTS collection')
        db_connection.commit()
        cursor.close()
        db_connection.close()
        
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


# Sample test for adding a new item to the collection
def test_add_to_collection(client):
    response = client.post(
        '/collection', data={'content': 'Test Item', 'breed': 'Test Breed'})
    assert b'Task added!' in response.data


# Sample test for updating a collection item
def test_update_collection_item(client):
    response = client.post(
        '/collection', data={'content': 'Initial Content', 'breed': 'Initial Breed'})
    assert b'Task added!' in response.data

    item_id = Collection.query.first().id

    response = client.post(
        f'/update/{item_id}', data={'content': 'Updated Content', 'breed': 'Updated Breed'})
    assert b'Task updated!' in response.data


# Sample test for deleting a collection item
def test_delete_collection_item(client):
    response = client.post(
        '/collection', data={'content': 'Item to Delete', 'breed': 'Breed to Delete'})
    assert b'Task added!' in response.data

    item_id = Collection.query.first().id

    response = client.get(f'/delete/{item_id}')
    assert b'Task deleted!' in response.data
    assert Collection.query.get(item_id) is None