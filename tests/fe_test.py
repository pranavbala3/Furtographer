# Front End Testing using PyTest FrameWork
from app import app

# Test that the website works
def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200