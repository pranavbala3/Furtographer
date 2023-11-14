from app import app, Collection, conn
import psycopg2
import pytest

# Initialize the app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True

    # Now create the test client
    client = app.test_client()

    yield client

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

    # delete every item in the collection table
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("DELETE FROM collections")
        conn.commit()

    # Simulate adding an item to the collection
    response = client.post('/collection', data=dict(content='New Furto', breed='Test Breed'), follow_redirects=True)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the new item is present in the collection
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections")
        tasks = cursor.fetchall()
        assert len(tasks) == 1
        assert tasks[0][1] == 'New Furto'
        assert tasks[0][2] == 'Test Breed'


# Sample test for updating a collection item
def test_update_collection_item(client):
    # Clear the collections table before the test
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("DELETE FROM collections")
        conn.commit()

    # Add an item to the collection
    response = client.post('/collection', data=dict(content='Item to Update', breed='Breed to Update'), follow_redirects=True)
    assert response.status_code == 200

    # Check if the item is present in the collection
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections")
        tasks = cursor.fetchall()
        assert len(tasks) == 1

        # Get the ID of the added item
        item_id = tasks[0][0]

    # Simulate updating the item
    response = client.post(f'/update/{item_id}', data=dict(content='Updated Item', breed='Updated Breed'), follow_redirects=True)
    assert response.status_code == 200

    # Check if the item is present in the collection and is updated
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections")
        tasks = cursor.fetchall()
        assert len(tasks) == 1
        assert tasks[0][1] == 'Updated Item'
        assert tasks[0][2] == 'Updated Breed'

# Sample test for deleting a collection item
def test_delete_collection_item(client):
    # Clear the collections table before the test
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("DELETE FROM collections")
        conn.commit()

    # Add an item to the collection
    response = client.post('/collection', data=dict(content='Item to Delete', breed='Breed to Delete'), follow_redirects=True)
    assert response.status_code == 200

    # Check if the item is present in the collection
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections")
        tasks = cursor.fetchall()
        assert len(tasks) == 1

        # Get the ID of the added item
        item_id = tasks[0][0]

    # Simulate deleting the item
    response = client.get(f'/delete/{item_id}', follow_redirects=True)
    assert response.status_code == 200

    # Check if the item is no longer present in the collection
    with app.app_context():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM collections")
        tasks = cursor.fetchall()
        assert len(tasks) == 0
